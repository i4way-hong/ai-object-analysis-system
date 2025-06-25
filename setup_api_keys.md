# AI API 키 설정 가이드

## 🔑 지원하는 AI API 서비스

### 1. OpenAI API (권장)
- **서비스**: ChatGPT API (GPT-4, GPT-3.5)
- **가입**: https://platform.openai.com/
- **특징**: 가장 정확한 객체 분석, 한국어 지원 우수

### 2. Anthropic API
- **서비스**: Claude API
- **가입**: https://console.anthropic.com/
- **특징**: 안전성과 정확성이 뛰어남

### 3. Google Gemini API (무료 시작 추천)
- **서비스**: Gemini API (Gemini Pro, Gemini Pro Vision)
- **가입**: https://ai.google.dev/
- **특징**: 무료 할당량 제공 (월 60 요청/분, 일 1500 요청)
- **장점**: 
  - ✅ **완전 무료** 시작 (신용카드 불필요)
  - ✅ 이미지 분석 지원
  - ✅ 한국어 지원 우수
  - ✅ 빠른 응답 속도

## 🛠️ 환경변수 설정 방법

### Windows PowerShell에서 임시 설정:
```powershell
$env:OPENAI_API_KEY="your_actual_api_key_here"
$env:ANTHROPIC_API_KEY="your_actual_api_key_here"  
$env:GOOGLE_API_KEY="your_actual_api_key_here"
```

### Windows에서 영구 설정:
1. 시스템 속성 → 고급 → 환경 변수
2. 새로 만들기 클릭
3. 변수 이름: `OPENAI_API_KEY`
4. 변수 값: 실제 API 키 입력

### .env 파일 사용 (권장):
1. `sample.env` 파일을 `.env`로 복사
2. 실제 API 키 값으로 수정

## 🚀 추천 설정 순서

### 🥇 **Google Gemini API** (무료 시작 - 추천!)
1. **완전 무료**로 시작 가능
2. 이미지 분석 기능 포함
3. 객체 분석 성능 우수
4. 신용카드 등록 불필요

### 🥈 **OpenAI API** (최고 품질)
- GPT-4는 객체 분석에 매우 정확함
- 유료이지만 품질이 우수함

### 🥉 **Anthropic Claude** (안전성 중시)
- 더 안전하고 신중한 분석

---

## 📋 Google Gemini API 키 얻는 방법 (상세 가이드)

### 1단계: Google AI Studio 접속
1. 웹브라우저에서 https://ai.google.dev/ 접속
2. **"Get started"** 또는 **"Get API Key"** 버튼 클릭
3. Google 계정으로 로그인 (Gmail 계정 사용)

### 2단계: API 키 생성
1. **"Get API key"** 버튼 클릭
2. **"Create API key in new project"** 선택
   - 또는 기존 Google Cloud 프로젝트가 있다면 선택
3. 프로젝트 이름 입력 (예: "CAR_TRACE_AI")
4. **"Create API key"** 버튼 클릭

### 3단계: API 키 복사 및 보관
1. 생성된 API 키를 **안전한 곳에 복사 저장**
2. 형식: `AIzaSy...` (39자리 문자열)
3. ⚠️ **중요**: 이 키는 다시 확인할 수 없으므로 반드시 저장!

### 4단계: 환경변수 설정
```powershell
# PowerShell에서 임시 설정 (즉시 테스트용)
$env:GOOGLE_API_KEY="AIzaSy여기에실제키입력"

# 영구 설정을 원한다면 .env 파일 사용
```

### 5단계: 즉시 테스트
```powershell
# API 키 설정 후 테스트
python test_real_ai.py
```

---

## 🎯 Google Gemini API 무료 한도

- **요청 제한**: 분당 60회, 일일 1,500회
- **토큰 제한**: 분당 32,000 토큰
- **이미지 분석**: 지원 (JPG, PNG, WebP)
- **비용**: **완전 무료** (신용카드 불필요)

## 💡 문제 해결

### Q: "API key not valid" 오류가 발생한다면?
A: 
1. API 키 복사 시 공백이 포함되지 않았는지 확인
2. 따옴표 안에 정확히 입력했는지 확인
3. Google AI Studio에서 API 키가 활성화되었는지 확인

### Q: 요청 한도를 초과했다면?
A: 
1. 잠시 기다린 후 재시도 (분당 제한)
2. 다음 날 재시도 (일일 제한)
3. 필요시 Google Cloud Platform에서 유료 플랜 고려

## ⚡ 즉시 테스트 방법

API 키 설정 후 다음 명령으로 테스트:

```powershell
python test_real_ai.py
```

또는 메인 시스템 실행:

```powershell
python run_system.py
```
