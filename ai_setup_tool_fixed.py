#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 AI 객체 분석기 설정 도구 (Google 우선순위)
API 키 설정 및 테스트 도구
"""

import os
import sys

def create_sample_env_file():
    """Google 우선순위 샘플 .env 파일 생성"""
    env_content = """# AI 객체 분석기 API 설정
# Google Gemini를 최우선으로 사용합니다 (무료!)

# Google API 키 (Gemini Pro Vision) - 최우선 추천!
# https://ai.google.dev/
# 무료로 월 1,500회 요청 가능, 신용카드 불필요
GOOGLE_API_KEY=your_actual_google_api_key_here

# OpenAI API 키 (GPT-4 Vision) - 유료이지만 고품질
# https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-openai-key-here

# Anthropic API 키 (Claude 3) - 안전성 중시
# https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# 사용법:
# 1. 위 키들 중 하나 이상을 실제 API 키로 교체
# 2. PowerShell에서 다음 명령으로 환경변수 설정:
#    $env:GOOGLE_API_KEY="your-actual-key" (추천: 무료)
#    $env:OPENAI_API_KEY="your-actual-key"
#    $env:ANTHROPIC_API_KEY="your-actual-key"
# 3. 또는 이 파일을 .env로 저장하고 python-dotenv 사용
"""
    
    with open('sample.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ Google 우선순위 샘플 환경변수 파일 생성: sample.env")
    return True

def test_api_keys():
    """API 키 테스트 (Google 우선순위)"""
    print("🔍 API 키 테스트 중... (Google 우선순위)")
    
    # 환경변수 확인 (Google 최우선)
    apis = {
        'Google Gemini': os.getenv('GOOGLE_API_KEY'),
        'OpenAI GPT-4': os.getenv('OPENAI_API_KEY'),
        'Anthropic Claude': os.getenv('ANTHROPIC_API_KEY')
    }
    
    # GitHub Copilot 확인
    try:
        from github_copilot_integration import GitHubCopilotIntegration
        copilot = GitHubCopilotIntegration()
        copilot_available = copilot.is_available()
        apis['GitHub Copilot'] = 'available' if copilot_available else None
    except ImportError:
        apis['GitHub Copilot'] = None
    
    available = []
    for name, key in apis.items():
        if name == 'GitHub Copilot':
            if key == 'available':
                available.append(name)
                print(f"✅ {name}: VS Code/GitHub CLI 연동 가능")
            else:
                print(f"❌ {name}: VS Code 또는 GitHub CLI 필요")
        elif key and key != 'your-key-here' and len(key) > 10:
            available.append(name)
            print(f"✅ {name}: API 키 설정됨 ({key[:8]}...)")
        else:
            print(f"❌ {name}: API 키 없음")
    
    if available:
        print(f"\n🎉 사용 가능한 AI API: {', '.join(available)}")
        print("\n🥇 현재 AI 분석 우선순위:")
        print("   1. 🌟 Google Gemini (무료, 우수한 성능)")
        print("   2. 🚀 GitHub Copilot (빠름, API 키 불필요)")
        print("   3. 🧠 OpenAI GPT-4 (고정밀)")
        print("   4. 🎯 Anthropic Claude (상세)")
        return True
    else:
        print("\n⚠️ 설정된 API가 없습니다.")
        print("\n📝 Google Gemini API 설정 방법 (추천):")
        print("1. https://ai.google.dev/ 접속")
        print("2. Google 계정 로그인")
        print("3. 'Get API Key' → 'Create API key in new project'")
        print("4. PowerShell에서 설정:")
        print('   $env:GOOGLE_API_KEY="your_actual_google_key"')
        print("\n💡 Google Gemini는 완전 무료로 시작할 수 있습니다!")
        return False

def test_ai_analysis():
    """AI 분석 테스트"""
    if not test_api_keys():
        return False
    
    try:
        print("\n🤖 AI 분석기 초기화 중...")
        from ai_object_analyzer import AIObjectAnalyzer
        analyzer = AIObjectAnalyzer()
        
        print("✅ Google 우선순위 AI 분석기 초기화 완료!")
        print("🌟 Google Gemini가 최우선으로 사용됩니다.")
        return True
            
    except Exception as e:
        print(f"❌ AI 분석 테스트 실패: {e}")
        return False

def show_usage_guide():
    """Google 우선순위 사용법 가이드"""
    print("🎯" + "="*60)
    print("🤖 AI 객체 상세 분석 시스템 사용법 (Google 우선순위)")
    print("="*60)
    print()
    print("1️⃣ Google Gemini API 설정 (최우선 추천):")
    print("   🌟 완전 무료로 시작 가능!")
    print("   • https://ai.google.dev/ 접속")
    print("   • Google 계정으로 로그인")
    print("   • 'Get API Key' 클릭")
    print("   • API 키 복사 후 환경변수 설정:")
    print('   $env:GOOGLE_API_KEY="your_actual_key"')
    print()
    print("2️⃣ 기타 AI API (선택사항):")
    print("   🧠 OpenAI: https://platform.openai.com/api-keys")
    print("   🎯 Anthropic: https://console.anthropic.com/")
    print("   🚀 GitHub Copilot: VS Code 확장 설치")
    print()
    print("3️⃣ 기능 확인:")
    print("   python ai_setup_tool_fixed.py test")
    print()
    print("4️⃣ 실제 사용:")
    print("   python run_system.py")
    print("   → Google Gemini로 고품질 AI 분석!")
    print()
    print("🥇 AI 분석 우선순위:")
    print("   1. 🌟 Google Gemini (무료, 우수한 성능)")
    print("   2. 🚀 GitHub Copilot (빠름, API 키 불필요)")
    print("   3. 🧠 OpenAI GPT-4 (고정밀)")
    print("   4. 🎯 Anthropic Claude (상세)")
    print()
    print("🎯 분석 예시:")
    print("   • 스마트폰 → iPhone 14 Pro, Galaxy S23 등")
    print("   • 자동차 → BMW X5, Tesla Model 3 등")
    print("   • 노트북 → MacBook Pro, ThinkPad 등")
    print("="*60)

def main():
    if len(sys.argv) < 2:
        print("🔧 AI 객체 분석기 설정 도구 (Google 우선순위)")
        print()
        print("사용법:")
        print("  python ai_setup_tool_fixed.py env       # Google 우선순위 샘플 파일 생성")
        print("  python ai_setup_tool_fixed.py test      # API 키 테스트")
        print("  python ai_setup_tool_fixed.py guide     # 사용법 가이드")
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
        print("\n사용 가능한 명령어: env, test, guide")

if __name__ == "__main__":
    main()
