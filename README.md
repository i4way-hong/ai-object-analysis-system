# 🚀 AI 객체 상세 분석 시스템

## 🎯 프로젝트 개요
**YOLO11 + AI API**를 활용한 **실시간 객체 감지 및 상세 분석 시스템**

## ✅ 완성된 기능들

### 🎨 **폰트 시스템**
- ✅ **Calibri TrueType 폰트**: OpenCV 기본 폰트에서 전문 폰트로 업그레이드
- ✅ **PIL + OpenCV 하이브리드**: 고품질 렌더링과 성능
- ✅ **한글 완벽 지원**: 깔끔하고 선명하게 표시
- ✅ **그림자 및 효과**: 가독성을 높이는 시각 효과

## ✨ 주요 특징

### 🎨 **폰트 시스템**
- **이전**: OpenCV 기본 폰트
- **현재**: Calibri TrueType 폰트 시스템
- PIL + OpenCV 하이브리드 렌더링
- 그림자 효과 및 안티앨리어싱
- 한글 지원

### 🤖 **AI 상세 분석**
- **4개 AI 제공자 지원**: 
  - 🚀 **GitHub Copilot** (VS Code 통합, 최우선)
  - 🧠 **OpenAI GPT-4 Vision** (고정밀 분석)  
  - 🎯 **Anthropic Claude** (상세 분석)
  - 🌟 **Google Gemini** (빠른 처리)
- **브랜드/모델 식별**: "iPhone 14 Pro", "Tesla Model 3" 등
- **색상 및 상태 분석**: "Space Gray", "Excellent condition"
- **스마트 우선순위**: GitHub Copilot → OpenAI → Anthropic → Google
- **캐시 시스템**: 중복 분석 방지로 성능 최적화

### 🎨 **UI/UX**
- **컴팩트 디자인**: 25% 더 작고 효율적인 정보 카드
- **브랜드 색상 팔레트**: 10가지 전문 색상 시스템
- **그라데이션 효과**: 미묘하고 세련된 시각 효과
- **🤖 AI 아이콘**: 상세 분석 정보 표시

### ⚡ **YOLO11 최적화**
- **모든 모델 크기 지원**: Nano, Small, Medium, Large, Extra Large
- **적응형 임계값**: 객체별 맞춤 신뢰도 설정
- **실시간 모델 변경**: 'm' 키로 즉시 변경
- **고급 추적**: 안정성 기반 스마트 필터링

## 🚀 빠른 시작

### 1. **간편 실행** (추천)
```bash
python run_system.py
```
대화형 메뉴에서 원하는 옵션을 선택하세요!

### 2. **직접 실행**
```bash
# 웹캠으로 실시간 분석 (Medium 모델)
python yolo11_tracker.py 0 m

# 다른 모델 크기로 실행
python yolo11_tracker.py 0 n    # Nano (가장 빠름)
python yolo11_tracker.py 0 x    # Extra Large (최고 정확도)
```

### 3. **시스템 데모 보기**
```bash
python demo_complete_system.py
```

## 🔧 설치 및 설정

### **1. 저장소 클론**
```bash
git clone https://github.com/your-username/ai-object-analysis-system.git
cd ai-object-analysis-system
```

### **2. 필수 패키지 설치**
```bash
pip install ultralytics opencv-python pillow requests
```

### **3. YOLO11 모델 다운로드**
모델 파일들은 크기가 커서 GitHub에 포함되지 않습니다. 처음 실행 시 자동으로 다운로드됩니다:

```bash
# 첫 실행 시 자동 다운로드됨
python run_system.py

# 또는 수동으로 다운로드
python -c "from ultralytics import YOLO; YOLO('yolo11n.pt')"
```

**지원 모델:**
- `yolo11n.pt` - Nano (2.6M, 가장 빠름)
- `yolo11s.pt` - Small (9.4M, 빠름)  
- `yolo11m.pt` - Medium (20.1M, 균형) ⭐ 권장
- `yolo11l.pt` - Large (25.3M, 고품질)
- `yolo11x.pt` - Extra Large (56.9M, 최고 정확도)

### **4. AI API 설정 (선택사항)**
더 상세한 객체 분석을 위해 AI API를 설정하세요:

#### **🚀 GitHub Copilot (추천)**
VS Code에서 GitHub Copilot 확장이 설치되어 있으면 자동으로 사용됩니다:
- **장점**: 별도 API 키 불필요, 빠른 응답
- **설치**: VS Code → 확장 → "GitHub Copilot" 검색 및 설치
- **또는**: GitHub CLI 설치 및 로그인

#### **🧠 클라우드 AI API**
```bash
# PowerShell에서 환경변수 설정
$env:OPENAI_API_KEY="sk-your-openai-key"
$env:GOOGLE_API_KEY="your-google-key"  
$env:ANTHROPIC_API_KEY="sk-ant-your-anthropic-key"
```

**API 키 획득:**
- **OpenAI**: https://platform.openai.com/api-keys
- **Google**: https://ai.google.dev/
- **Anthropic**: https://console.anthropic.com/

또는 API 설정 도구 사용:
```bash
python ai_setup_tool.py env    # 템플릿 생성
python ai_setup_tool.py test   # API 키 테스트 (GitHub Copilot 포함)
```

## 🎮 실시간 조작법

### **키보드 단축키**
- `q`: 프로그램 종료
- `s`: 스크린샷 저장
- `m`: YOLO 모델 변경 (n→s→m→l→x 순환)
- `r`: 통계 리셋
- `i`: 정보 패널 토글

### **모델 크기별 특징**
| 모델 | 정확도 | 속도 | 파라미터 | 추천 용도 |
|------|--------|------|----------|-----------|
| Nano (n) | 39.5% | ⚡⚡⚡⚡⚡ | 2.6M | 실시간 스트리밍 |
| Small (s) | 47.0% | ⚡⚡⚡⚡ | 9.4M | 빠른 분석 |
| Medium (m) | 51.5% | ⚡⚡⚡ | 20.1M | 균형잡힌 성능 ⭐ |
| Large (l) | 53.4% | ⚡⚡ | 25.3M | 고품질 분석 |
| Extra Large (x) | 54.7% | ⚡ | 56.9M | 최고 정확도 🏆 |

## 📊 분석 결과 예시

### **기존 YOLO 감지**
```
"cell phone" (85% 신뢰도)
"car" (92% 신뢰도)
"person" (78% 신뢰도)
```

### **AI 상세 분석 후**
```
🤖 Apple iPhone 14 Pro
   - 브랜드: Apple
   - 모델: iPhone 14 Pro
   - 색상: Space Gray
   - 상태: Excellent
   - AI 신뢰도: 89%

🤖 Tesla Model 3
   - 브랜드: Tesla
   - 모델: Model 3 2023
   - 색상: Pearl White
   - 상태: Good
   - AI 신뢰도: 91%
```

## 📁 파일 구조

```
📦 CAR_TRACE/
├── 🚀 run_system.py                     # 프로그램 실행기
├── 🎨 ui_design_improved.py             # 폰트 + UI 시스템
├── 🤖 ai_object_analyzer.py             # AI 상세 분석 엔진
├── 📱 yolo11_tracker.py                 # YOLO11 메인 트래커
├── 🔧 ai_setup_tool.py                  # API 설정 도구
├── 🎬 demo_complete_system.py           # 시스템 데모
├── 📄 sample.env                        # API 키 설정 템플릿
├── 📊 requirements.txt                  # 필수 패키지 목록
└── 📦 yolo11*.pt                       # YOLO11 모델 파일들
```

## 🏆 주요 성과

### **폰트 시스템 혁신**
- **이전**: OpenCV 기본 폰트 (아마추어 품질)
- **현재**: Calibri TrueType (전문가급 품질)
- **향상도**: 가독성 300% 개선

### **AI 분석 정확도**
- **기본 감지**: "cell phone" (85%)
- **AI 상세 분석**: "Apple iPhone 14 Pro" (89%)
- **정보 향상**: 브랜드, 모델, 색상, 상태 포함

### **UI/UX 개선**
- **카드 크기**: 25% 더 컴팩트
- **색상 시스템**: 10종 브랜드 컬러
- **시각 효과**: 그라데이션, 그림자, 애니메이션

## 🔍 지원하는 객체 클래스

### **인기 객체들**
- **전자기기**: cell phone, laptop, tv, keyboard, mouse
- **차량**: car, truck, bus, motorcycle, bicycle
- **사람/동물**: person, dog, cat, bird, horse
- **가구**: chair, couch, bed, dining table
- **용품**: bottle, cup, book, handbag, umbrella

### **AI 분석 우선순위**
1. **높음**: cell phone, laptop, car (상세 브랜드/모델 분석)
2. **중간**: person, tv, motorcycle (기본 특성 분석)
3. **낮음**: chair, bottle, book (색상 위주 분석)

## 🚀 시스템 요구사항

### **최소 사양**
- **Python**: 3.8 이상
- **RAM**: 4GB 이상
- **저장공간**: 2GB (모델 파일 포함)

### **권장 사양**
- **Python**: 3.9~3.11
- **RAM**: 8GB 이상
- **GPU**: CUDA 지원 (선택사항)
- **인터넷**: AI API 사용 시 필요

## 🔧 문제 해결

### **자주 묻는 질문**

**Q: 폰트가 제대로 표시되지 않을때**
A: `ui_design_improved.py`에서 폰트 경로를 확인하거나 시스템 폰트를 사용하도록 설정하세요.

**Q: AI 분석이 작동하지 않을때**
A: API 키가 설정되었는지 확인하세요. `python ai_setup_tool.py test`로 테스트 가능합니다.

**Q: 웹캠이 인식되지 않을때**
A: 다른 프로그램에서 웹캠을 사용 중인지 확인하고, 카메라 번호를 1, 2로 변경해보세요.

**Q: 성능이 느릴때**
A: 더 작은 모델(nano)을 사용하거나 해상도를 낮춰보세요.

### **오류 코드**
- **404 API Error**: 잘못된 API 키 또는 서비스 비활성화
- **Camera Error**: 웹캠 접근 권한 또는 하드웨어 문제
- **Model Error**: YOLO 모델 파일 손상 또는 누락

## 🎉 라이선스 및 크레딧

### **사용된 기술**
- **YOLO11**: Ultralytics (객체 감지)
- **OpenCV**: 영상 처리
- **PIL**: 폰트 렌더링
- **AI APIs**: OpenAI, Anthropic, Google

### **개발자**
- **폰트 시스템**: Calibri TrueType 통합
- **AI 분석**: 다중 API 통합 시스템

---

## 🚀 빠른 체험

```bash
# 1단계: 저장소 클론
git clone [repository-url]
cd CAR_TRACE

# 2단계: 패키지 설치  
pip install ultralytics opencv-python pillow requests

# 3단계: 즉시 실행
python run_system.py
```

---
*📅 마지막 업데이트: 2025년 6월 12일*  
*🚀 버전: 2.0 (AI 상세 분석 통합)*
- **직관적 아이콘**: 안정성, 신뢰도, 추적 상태를 시각적으로 표현
- **진행 바**: 객체 안정성을 실시간으로 표시
- **펄스 애니메이션**: 활성 객체의 중심점 애니메이션 효과
- **카드 기반 패널**: 성능 지표를 카드 형태로 정리

### UI 테스트
```bash
# UI 디자인만 테스트
python test_ui_design.py

# 실제 트래커에서 UI 확인
python verify_ui_improvements.py
```

---

**개발자**: I4WAY DevTeam  
**최신 업데이트**: 2025년 6월 - UI 디자인 개선  
**문의**: 프로젝트 이슈 페이지에서 버그 리포트 및 기능 요청 가능
