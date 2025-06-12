#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 AI 객체 분석기 설정 도구
API 키 설정 및 테스트 도구
"""

import os
import sys
import cv2
import numpy as np
from ai_object_analyzer import AIObjectAnalyzer

def create_sample_env_file():
    """샘플 .env 파일 생성"""
    env_content = """# AI 객체 분석기 API 설정
# 아래 API 키 중 하나 이상을 실제 값으로 교체하세요

# OpenAI API 키 (GPT-4 Vision) - 추천
# https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-openai-key-here

# Anthropic API 키 (Claude 3)
# https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# Google API 키 (Gemini Pro Vision)
# https://ai.google.dev/
GOOGLE_API_KEY=yAIzaSyCXM_2sUIp215NVKAZi4dIJ15O9LkjoGpU

# 사용법:
# 1. 위 키들 중 하나 이상을 실제 API 키로 교체
# 2. PowerShell에서 다음 명령으로 환경변수 설정:
#    $env:OPENAI_API_KEY="your-actual-key"
#    $env:ANTHROPIC_API_KEY="your-actual-key"  
#    $env:GOOGLE_API_KEY="your-actual-key"
# 3. 또는 이 파일을 .env로 저장하고 python-dotenv 사용
"""
    
    with open('sample.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ 샘플 환경변수 파일 생성: sample.env")
    return True

def test_api_keys():
    """API 키 테스트"""
    print("🔍 API 키 테스트 중...")
    
    # 환경변수 확인
    apis = {
        'OpenAI': os.getenv('OPENAI_API_KEY'),
        'Anthropic': os.getenv('ANTHROPIC_API_KEY'),
        'Google': os.getenv('GOOGLE_API_KEY')
    }
    
    available = []
    for name, key in apis.items():
        if key and key != 'your-key-here' and len(key) > 10:
            available.append(name)
            print(f"✅ {name}: API 키 설정됨 ({key[:8]}...)")
        else:
            print(f"❌ {name}: API 키 없음")
    
    if available:
        print(f"\n🎉 사용 가능한 AI API: {', '.join(available)}")
        return True
    else:
        print("\n⚠️ 설정된 API 키가 없습니다.")
        print("\n📝 API 키 설정 방법:")
        print("1. PowerShell에서 환경변수 설정:")
        print('   $env:OPENAI_API_KEY="sk-your-actual-openai-key"')
        print('   $env:ANTHROPIC_API_KEY="sk-ant-your-actual-anthropic-key"')
        print('   $env:GOOGLE_API_KEY="your-actual-google-key"')
        print("\n2. 또는 sample.env 파일을 편집하여 실제 키 입력")
        return False

def create_test_image():
    """테스트용 이미지 생성 (스마트폰 모형)"""
    # 640x480 검은 배경
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # 스마트폰 모양 그리기
    phone_x, phone_y = 250, 150
    phone_w, phone_h = 140, 180
    
    # 폰 본체 (어두운 회색)
    cv2.rectangle(img, (phone_x, phone_y), (phone_x + phone_w, phone_y + phone_h), (60, 60, 60), -1)
    
    # 화면 (검은색)
    screen_margin = 15
    cv2.rectangle(img, 
                 (phone_x + screen_margin, phone_y + screen_margin), 
                 (phone_x + phone_w - screen_margin, phone_y + phone_h - screen_margin), 
                 (20, 20, 20), -1)
    
    # 홈버튼 (iPhone 스타일)
    button_x = phone_x + phone_w // 2
    button_y = phone_y + phone_h - 25
    cv2.circle(img, (button_x, button_y), 8, (40, 40, 40), -1)
    cv2.circle(img, (button_x, button_y), 8, (100, 100, 100), 2)
    
    # 카메라 (상단 중앙)
    camera_x = phone_x + phone_w // 2
    camera_y = phone_y + 25
    cv2.circle(img, (camera_x, camera_y), 5, (30, 30, 30), -1)
    
    # 스피커 (상단)
    speaker_x = phone_x + phone_w // 2 - 20
    speaker_y = phone_y + 10
    cv2.rectangle(img, (speaker_x, speaker_y), (speaker_x + 40, speaker_y + 3), (40, 40, 40), -1)
    
    return img

def test_ai_analysis():
    """AI 분석 테스트"""
    if not test_api_keys():
        return False
    
    try:
        print("\n🤖 AI 분석기 초기화 중...")
        analyzer = AIObjectAnalyzer()
        
        print("📱 테스트 이미지 생성 중...")
        test_img = create_test_image()
        
        # 테스트 이미지 저장
        cv2.imwrite('test_phone_image.jpg', test_img)
        print("✅ 테스트 이미지 저장: test_phone_image.jpg")
        
        print("🔍 AI 분석 테스트 중...")
        # 스마트폰 영역 [x1, y1, x2, y2]
        phone_box = [250, 150, 390, 330]
        
        result = analyzer.analyze_object_detailed(
            test_img, phone_box, 'cell phone', 0.85
        )
        
        if result:
            print("🎉 AI 분석 성공!")
            print(f"   Provider: {result.get('provider', 'Unknown')}")
            print(f"   Brand: {result.get('brand', 'Unknown')}")
            print(f"   Model: {result.get('model', 'Unknown')}")
            print(f"   Type: {result.get('type', 'Unknown')}")
            print(f"   Color: {result.get('color', 'Unknown')}")
            print(f"   Confidence: {result.get('confidence', 0):.2f}")
            
            detailed_name = analyzer.get_detailed_object_name(result, 'cell phone')
            print(f"   Detailed Name: {detailed_name}")
            
            return True
        else:
            print("❌ AI 분석 실패")
            return False
            
    except Exception as e:
        print(f"❌ AI 분석 테스트 실패: {e}")
        return False

def show_usage_guide():
    """사용법 가이드 표시"""
    print("🎯" + "="*60)
    print("🤖 AI 객체 상세 분석 시스템 사용법")
    print("="*60)
    print()
    print("1️⃣ API 키 준비:")
    print("   • OpenAI (추천): https://platform.openai.com/api-keys")
    print("   • Anthropic: https://console.anthropic.com/")
    print("   • Google: https://ai.google.dev/")
    print()
    print("2️⃣ 환경변수 설정 (PowerShell):")
    print('   $env:OPENAI_API_KEY="sk-your-actual-key"')
    print()
    print("3️⃣ 기능 확인:")
    print("   python ai_setup_tool.py test")
    print()
    print("4️⃣ 실제 사용:")
    print("   python yolo11_tracker.py 0")
    print("   → 웹캠으로 AI 상세 분석 테스트")
    print()
    print("💡 기능:")
    print("   • 스마트폰 → iPhone 14 Pro, Galaxy S23 등")
    print("   • 자동차 → BMW X5, Tesla Model 3 등")
    print("   • 노트북 → MacBook Pro, ThinkPad 등")
    print("="*60)

def main():
    if len(sys.argv) < 2:
        print("🔧 AI 객체 분석기 설정 도구")
        print()
        print("사용법:")
        print("  python ai_setup_tool.py env     # 샘플 환경변수 파일 생성")
        print("  python ai_setup_tool.py test    # API 키 테스트")
        print("  python ai_setup_tool.py guide   # 사용법 가이드")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'env':
        create_sample_env_file()
    elif command == 'test':
        test_ai_analysis()
    elif command == 'guide':
        show_usage_guide()
    else:
        print(f"❌ 알 수 없는 명령어: {command}")

if __name__ == "__main__":
    main()
