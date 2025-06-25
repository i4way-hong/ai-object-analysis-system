#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 Google Gemini API 키 설정 및 테스트 도구
실제 API 키를 얻고 설정하는 전체 과정을 안내합니다.
"""

import os
import webbrowser
import requests
import json
import time

def open_gemini_signup():
    """Google AI Studio 웹사이트 열기"""
    url = "https://ai.google.dev/"
    print(f"🌐 Google AI Studio 웹사이트를 엽니다: {url}")
    try:
        webbrowser.open(url)
        print("✅ 브라우저에서 Google AI Studio가 열렸습니다.")
        return True
    except Exception as e:
        print(f"❌ 브라우저 열기 실패: {e}")
        print(f"🔗 수동으로 다음 링크를 열어주세요: {url}")
        return False

def guide_api_key_creation():
    """API 키 생성 가이드"""
    print("\n📋 Google Gemini API 키 생성 단계별 가이드:")
    print("=" * 60)
    
    steps = [
        "1️⃣ Google 계정으로 로그인 (Gmail 계정 사용)",
        "2️⃣ 'Get API key' 버튼 클릭",
        "3️⃣ 'Create API key in new project' 선택",
        "4️⃣ 프로젝트 이름 입력 (예: 'CAR_TRACE_AI')",
        "5️⃣ 'Create API key' 버튼 클릭",
        "6️⃣ 생성된 API 키 복사 (AIzaSy로 시작하는 39자리)",
        "7️⃣ 아래에서 API 키 입력 및 테스트"
    ]
    
    for step in steps:
        print(f"   {step}")
        time.sleep(1)
    
    print("\n⚠️  중요사항:")
    print("   • API 키는 다시 확인할 수 없으므로 반드시 안전하게 보관")
    print("   • 무료 한도: 분당 60회, 일일 1,500회 요청")
    print("   • 신용카드 등록 불필요 (완전 무료)")

def test_api_key(api_key):
    """API 키 유효성 테스트"""
    if not api_key or len(api_key) < 30:
        print("❌ API 키가 너무 짧습니다. 올바른 키를 입력해주세요.")
        return False
    
    if not api_key.startswith('AIzaSy'):
        print("❌ Google API 키는 'AIzaSy'로 시작해야 합니다.")
        return False
    
    print(f"🔄 API 키 테스트 중: {api_key[:20]}...")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": "Hello! Please respond with exactly this JSON: {\"status\": \"success\", \"message\": \"API working\"}"
            }]
        }],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 50
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            
            if 'candidates' in result and result['candidates']:
                candidate = result['candidates'][0]
                if 'content' in candidate:
                    content = candidate['content']['parts'][0]['text'].strip()
                    print(f"✅ API 응답 성공: {content}")
                    print("✅ Google Gemini API 키가 정상 작동합니다!")
                    return True
                    
        elif response.status_code == 400:
            error_data = response.json()
            if 'API_KEY_INVALID' in str(error_data):
                print("❌ API 키가 유효하지 않습니다. 다시 확인해주세요.")
            else:
                print(f"❌ API 오류: {error_data}")
        else:
            print(f"❌ HTTP 오류 {response.status_code}: {response.text}")
            
        return False
        
    except Exception as e:
        print(f"❌ 연결 오류: {e}")
        return False

def save_api_key_to_env(api_key):
    """API 키를 .env 파일에 저장"""
    try:
        env_content = f"""# Google Gemini API 설정
# 생성일: {time.strftime('%Y-%m-%d %H:%M:%S')}
GOOGLE_API_KEY={api_key}

# 다른 AI API 키들 (선택사항)
# OPENAI_API_KEY=your_openai_key_here
# ANTHROPIC_API_KEY=your_anthropic_key_here
"""
        
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("✅ API 키가 .env 파일에 저장되었습니다!")
        print("💡 이제 다음 명령으로 시스템을 실행할 수 있습니다:")
        print("   python run_system.py")
        return True
        
    except Exception as e:
        print(f"❌ .env 파일 저장 실패: {e}")
        return False

def set_environment_variable(api_key):
    """환경변수로 API 키 설정"""
    try:
        os.environ['GOOGLE_API_KEY'] = api_key
        print("✅ 현재 세션에 환경변수가 설정되었습니다!")
        print("💡 즉시 테스트를 실행할 수 있습니다.")
        return True
    except Exception as e:
        print(f"❌ 환경변수 설정 실패: {e}")
        return False

def main():
    """메인 실행 함수"""
    print("🚀 Google Gemini API 키 설정 도구")
    print("=" * 50)
    
    # 1. Google AI Studio 열기
    print("\n🌐 1단계: Google AI Studio 웹사이트 접속")
    open_gemini_signup()
    
    # 2. API 키 생성 가이드
    print("\n📋 2단계: API 키 생성 가이드")
    guide_api_key_creation()
    
    # 3. API 키 입력 받기
    print("\n🔑 3단계: API 키 입력 및 테스트")
    print("-" * 40)
    
    while True:
        print("\n📝 생성한 Google API 키를 입력해주세요:")
        print("   (AIzaSy로 시작하는 39자리 문자열)")
        api_key = input("API Key: ").strip()
        
        if not api_key:
            print("❌ API 키를 입력해주세요.")
            continue
        
        if api_key.lower() in ['quit', 'exit', 'q']:
            print("👋 설정을 취소합니다.")
            return
        
        # API 키 테스트
        if test_api_key(api_key):
            # 성공 시 저장
            print("\n💾 4단계: API 키 저장")
            
            # 환경변수 설정
            set_environment_variable(api_key)
            
            # .env 파일 저장
            save_api_key_to_env(api_key)
            
            print("\n🎉 설정 완료!")
            print("✅ Google Gemini API 키가 성공적으로 설정되었습니다.")
            print("\n🚀 다음 단계:")
            print("   1. python run_system.py (메인 시스템 실행)")
            print("   2. python test_real_ai.py (AI 분석 테스트)")
            break
        else:
            print("\n❌ API 키 테스트 실패. 다시 시도해주세요.")
            retry = input("다시 시도하시겠습니까? (y/n): ").lower()
            if retry not in ['y', 'yes', '']:
                print("👋 설정을 종료합니다.")
                break

if __name__ == "__main__":
    main()
