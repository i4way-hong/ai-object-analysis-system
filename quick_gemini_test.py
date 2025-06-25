import os
import requests
import json

# API 키 설정
os.environ['GOOGLE_API_KEY'] = 'AIzaSyCtfKgjPwC6gQa2XoooypDZrPVPT_H6UhY'
api_key = os.getenv('GOOGLE_API_KEY')
print(f'✅ API Key: {api_key[:20]}...')

url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}'

payload = {
    "contents": [{
        "parts": [{
            "text": "Return only this JSON format: {\"test\": \"success\", \"status\": \"ok\"}"
        }]
    }],
    "generationConfig": {
        "temperature": 0.1,
        "maxOutputTokens": 100
    }
}

try:
    print("🔄 Testing Gemini API...")
    response = requests.post(url, json=payload, timeout=10)
    print(f"📡 Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ API Response received")
        
        if 'candidates' in result and result['candidates']:
            candidate = result['candidates'][0]
            finish_reason = candidate.get('finishReason', 'UNKNOWN')
            print(f"🏁 Finish reason: {finish_reason}")
            
            if 'content' in candidate:
                content = candidate['content']['parts'][0]['text'].strip()
                print(f"📄 Content: {content}")
                
                # JSON 파싱 테스트
                try:
                    # 마크다운 코드 블록 제거
                    if content.startswith('```json'):
                        content = content.replace('```json', '').replace('```', '').strip()
                    elif content.startswith('```'):
                        content = content.replace('```', '').strip()
                    
                    parsed = json.loads(content)
                    print("✅ JSON parsing: SUCCESS")
                    print(f"🎯 Parsed: {parsed}")
                except json.JSONDecodeError as e:
                    print(f"❌ JSON parsing: FAILED - {e}")
                    print(f"🔍 Raw content: {repr(content)}")
            else:
                print("❌ No content in candidate")
        else:
            print("❌ No candidates in response")
            print(f"Full response: {json.dumps(result, indent=2, ensure_ascii=False)}")
    else:
        print(f"❌ API Error: {response.text}")
        
except Exception as e:
    print(f"❌ Exception: {e}")
