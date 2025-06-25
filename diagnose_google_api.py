#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google API 400 오류 진단 도구
API 키 유효성과 요청 형식을 상세히 테스트합니다.
"""

import os
import requests
import json

def test_google_api_detailed():
    """Google API 상세 진단"""
    
    # API 키 설정
    api_key = "AIzaSyCtfKgjPwC6gQa2XoooypDZrPVPT_H6UhY"
    os.environ['GOOGLE_API_KEY'] = api_key
    
    print("🔍 Google Gemini API 400 오류 진단")
    print("=" * 50)
    print(f"🔑 API 키: {api_key[:20]}...")
    
    # 1. 기본 API 키 유효성 테스트
    print("\n1️⃣ API 키 유효성 테스트")
    test_basic_api_key(api_key)
    
    # 2. 모델 엔드포인트 테스트
    print("\n2️⃣ 모델 엔드포인트 테스트")
    test_model_endpoints(api_key)
    
    # 3. 요청 형식 테스트
    print("\n3️⃣ 요청 형식 테스트")
    test_request_format(api_key)

def test_basic_api_key(api_key):
    """기본 API 키 유효성 테스트"""
    
    # 가장 단순한 텍스트 요청
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": "Hello"
            }]
        }]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"📡 상태 코드: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API 키 유효함")
        elif response.status_code == 400:
            error_data = response.json()
            print("❌ 400 오류 상세:")
            print(json.dumps(error_data, indent=2, ensure_ascii=False))
        elif response.status_code == 403:
            print("❌ API 키 권한 없음 또는 API 비활성화")
        else:
            print(f"❌ 기타 오류: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ 요청 실패: {e}")

def test_model_endpoints(api_key):
    """다양한 모델 엔드포인트 테스트"""
    
    models = [
        "gemini-1.5-flash",
        "gemini-1.5-pro", 
        "gemini-2.0-flash",
        "gemini-pro-vision"
    ]
    
    for model in models:
        print(f"\n🧪 모델 테스트: {model}")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": "Test"
                }]
            }]
        }
        
        try:
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {model}: 정상 작동")
            elif response.status_code == 404:
                print(f"   ❌ {model}: 모델 없음")
            elif response.status_code == 400:
                print(f"   ❌ {model}: 400 오류")
            else:
                print(f"   ⚠️ {model}: 상태 {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ {model}: 연결 실패")

def test_request_format(api_key):
    """요청 형식별 테스트"""
    
    # 정상적인 모델로 다양한 요청 형식 테스트
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    # 테스트 1: 최소 요청
    print("\n🧪 최소 요청 테스트")
    test_minimal_request(url)
    
    # 테스트 2: 생성 설정 포함
    print("\n🧪 생성 설정 포함 테스트")
    test_with_generation_config(url)
    
    # 테스트 3: 안전 설정 포함
    print("\n🧪 안전 설정 포함 테스트")
    test_with_safety_settings(url)

def test_minimal_request(url):
    """최소한의 요청 테스트"""
    
    payload = {
        "contents": [{
            "parts": [{
                "text": "Say hello"
            }]
        }]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"   상태: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result['candidates'][0]['content']['parts'][0]['text']
            print(f"   ✅ 응답: {content[:50]}...")
        else:
            error_data = response.json()
            print(f"   ❌ 오류: {error_data}")
            
    except Exception as e:
        print(f"   ❌ 실패: {e}")

def test_with_generation_config(url):
    """생성 설정 포함 테스트"""
    
    payload = {
        "contents": [{
            "parts": [{
                "text": "Return JSON: {\"test\": \"ok\"}"
            }]
        }],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 100
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"   상태: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ 생성 설정 정상")
        else:
            error_data = response.json()
            print(f"   ❌ 오류: {error_data}")
            
    except Exception as e:
        print(f"   ❌ 실패: {e}")

def test_with_safety_settings(url):
    """안전 설정 포함 테스트"""
    
    payload = {
        "contents": [{
            "parts": [{
                "text": "Hello world"
            }]
        }],
        "safetySettings": [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            }
        ]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"   상태: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ 안전 설정 정상")
        else:
            error_data = response.json()
            print(f"   ❌ 오류: {error_data}")
            
    except Exception as e:
        print(f"   ❌ 실패: {e}")

def provide_solutions():
    """400 오류 해결 방안 제시"""
    
    print("\n" + "=" * 50)
    print("🛠️ Google API 400 오류 해결 방안")
    print("=" * 50)
    
    print("\n📋 일반적인 400 오류 원인:")
    print("1. 잘못된 API 키 형식")
    print("2. 비활성화된 API 키")
    print("3. 잘못된 모델명 (gemini-2.0-flash → gemini-1.5-flash)")
    print("4. 잘못된 요청 형식")
    print("5. API 할당량 초과")
    
    print("\n🔧 해결 방법:")
    print("1. 새로운 API 키 생성:")
    print("   • https://ai.google.dev/ 접속")
    print("   • 새 프로젝트에서 API 키 생성")
    print("   • Generative AI API 활성화 확인")
    
    print("\n2. 올바른 모델명 사용:")
    print("   • gemini-1.5-flash (추천)")
    print("   • gemini-1.5-pro")
    print("   • gemini-pro-vision")
    
    print("\n3. 요청 형식 확인:")
    print("   • contents 배열 형식")
    print("   • parts 배열 형식")
    print("   • 올바른 JSON 구조")

if __name__ == "__main__":
    test_google_api_detailed()
    provide_solutions()
