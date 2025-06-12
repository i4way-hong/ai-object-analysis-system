#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 AI 객체 상세 분석기
YOLO 기본 감지 결과를 AI API로 상세 분석하여 구체적인 모델명/브랜드 정보 제공
"""

import cv2
import numpy as np
import base64
import requests
import json
import time
import os
from typing import Dict, List, Tuple, Optional
import threading
from queue import Queue
import logging

class AIObjectAnalyzer:
    """AI API를 활용한 객체 상세 분석 클래스"""
    
    def __init__(self):
        self.api_providers = {
            'openai': {
                'enabled': False,
                'api_key': os.getenv('OPENAI_API_KEY'),
                'endpoint': 'https://api.openai.com/v1/chat/completions',
                'model': 'gpt-4-vision-preview'
            },
            'anthropic': {
                'enabled': False,
                'api_key': os.getenv('ANTHROPIC_API_KEY'),
                'endpoint': 'https://api.anthropic.com/v1/messages',
                'model': 'claude-3-sonnet-20240229'
            },
            'google': {
                'enabled': False,
                'api_key': os.getenv('GOOGLE_API_KEY'),
                'endpoint': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent',
                'model': 'gemini-2.0-flash'
            },
            'github_copilot': {
                'enabled': False,
                'api_key': None,  # GitHub Copilot은 별도 API 키 불필요
                'endpoint': 'local_vscode_integration',
                'model': 'github-copilot'
            }
        }
        
        # GitHub Copilot 통합 초기화
        try:
            from github_copilot_integration import GitHubCopilotIntegration
            self.copilot_integration = GitHubCopilotIntegration()
            if self.copilot_integration.is_available():
                self.api_providers['github_copilot']['enabled'] = True
                print("✅ GitHub Copilot 통합 활성화")
            else:
                print("⚠️ GitHub Copilot 사용 불가 (VS Code 또는 GitHub CLI 필요)")
        except ImportError:
            self.copilot_integration = None
            print("⚠️ GitHub Copilot 통합 모듈을 찾을 수 없습니다")
        
        # API 설정 확인
        self.check_api_availability()
        
        # 분석 캐시 (같은 객체 반복 분석 방지)
        self.analysis_cache = {}
        self.cache_expire_time = 300  # 5분
        
        # 비동기 분석을 위한 큐
        self.analysis_queue = Queue()
        self.result_cache = {}
        
        # 분석 설정
        self.analysis_settings = {
            'detail_level': 'high',  # low, medium, high
            'focus_areas': [
                'brand', 'model', 'type', 'color', 'condition', 'distinctive_features'
            ],
            'confidence_threshold': 0.7,
            'max_analysis_time': 10  # 초
        }
        
        # 객체별 분석 우선순위
        self.analysis_priority = {
            'cell phone': 10,
            'laptop': 9,
            'car': 8,
            'truck': 7,
            'person': 6,
            'tv': 5,
            'book': 4,
            'bottle': 3,
            'chair': 2,
            'cup': 1
        }
        
        print("🤖 AI 객체 분석기 초기화 완료")
        
    def check_api_availability(self):
        """API 사용 가능성 확인"""
        available_apis = []
        
        for provider, config in self.api_providers.items():
            if config['api_key']:
                config['enabled'] = True
                available_apis.append(provider)
                print(f"✅ {provider.upper()} API 사용 가능")
            else:
                print(f"⚠️ {provider.upper()} API 키가 설정되지 않음")
        
        if not available_apis:
            print("⚠️ 사용 가능한 AI API가 없습니다. 환경변수를 설정하세요:")
            print("   OPENAI_API_KEY=your_openai_key")
            print("   ANTHROPIC_API_KEY=your_anthropic_key") 
            print("   GOOGLE_API_KEY=your_google_key")
        
        return available_apis
    
    def encode_image_to_base64(self, image_crop: np.ndarray) -> str:
        """이미지를 base64로 인코딩"""
        try:
            # 이미지 품질 최적화
            if image_crop.shape[1] > 512:
                height, width = image_crop.shape[:2]
                scale = 512 / width
                new_width, new_height = int(width * scale), int(height * scale)
                image_crop = cv2.resize(image_crop, (new_width, new_height))
            
            # JPEG 인코딩 (압축률 높음)
            _, buffer = cv2.imencode('.jpg', image_crop, [cv2.IMWRITE_JPEG_QUALITY, 85])
            image_base64 = base64.b64encode(buffer).decode('utf-8')
            return image_base64
        except Exception as e:
            print(f"❌ 이미지 인코딩 실패: {e}")
            return None
    
    def create_analysis_prompt(self, object_class: str, detail_level: str = 'high') -> str:
        """분석 프롬프트 생성"""
        base_prompt = f"""이 이미지에 보이는 {object_class}에 대해 상세히 분석해주세요.
        
다음 정보를 JSON 형태로 제공해주세요:
{{
    "brand": "브랜드명 (알 수 있는 경우)",
    "model": "모델명 (알 수 있는 경우)", 
    "type": "구체적인 타입/분류",
    "color": "주요 색상",
    "distinctive_features": ["특징1", "특징2", "특징3"],
    "estimated_value": "추정 가격대 (알 수 있는 경우)",
    "condition": "상태 (새것/사용됨/낡음 등)",
    "confidence": 0.0-1.0 사이의 신뢰도
}}

분석 기준:
- 브랜드 로고나 디자인 특징을 주의깊게 관찰
- 모델 고유의 특징적 디자인 요소 식별
- 색상, 크기, 형태 등 시각적 특징 분석
- 가능한 한 구체적으로 식별

응답은 반드시 JSON 형태로만 제공하고, 다른 설명은 포함하지 마세요."""

        if detail_level == 'high':
            if object_class == 'cell phone':
                base_prompt += """

특별히 스마트폰의 경우:
- 카메라 배치와 개수 확인
- 홈버튼 유무 확인  
- 브랜드별 특징적 디자인 (iPhone의 홈버튼/노치, Samsung의 곡면 등)
- 크기와 비율 분석"""

            elif object_class == 'car':
                base_prompt += """

특별히 자동차의 경우:
- 그릴 디자인과 로고 확인
- 헤드라이트 형태 분석
- 차체 라인과 비율 확인
- 휠 디자인 관찰"""

            elif object_class == 'laptop':
                base_prompt += """

특별히 노트북의 경우:
- 브랜드 로고 위치와 형태
- 화면 베젤 두께
- 키보드 레이아웃
- 전체적인 디자인 언어"""

        return base_prompt
    
    def analyze_with_openai(self, image_base64: str, object_class: str) -> Optional[Dict]:
        """OpenAI GPT-4 Vision으로 분석"""
        if not self.api_providers['openai']['enabled']:
            return None
            
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f"Bearer {self.api_providers['openai']['api_key']}"
            }
            
            prompt = self.create_analysis_prompt(object_class)
            
            payload = {
                "model": "gpt-4-vision-preview",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 500,
                "temperature": 0.1
            }
            
            response = requests.post(
                self.api_providers['openai']['endpoint'],
                headers=headers,
                json=payload,
                timeout=self.analysis_settings['max_analysis_time']
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                try:
                    # JSON 파싱
                    analysis = json.loads(content)
                    analysis['provider'] = 'OpenAI GPT-4'
                    return analysis
                except json.JSONDecodeError:
                    print(f"⚠️ OpenAI 응답 JSON 파싱 실패: {content}")
                    return None
            else:
                print(f"❌ OpenAI API 오류: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ OpenAI 분석 실패: {e}")
            return None
    
    def analyze_with_anthropic(self, image_base64: str, object_class: str) -> Optional[Dict]:
        """Anthropic Claude로 분석"""
        if not self.api_providers['anthropic']['enabled']:
            return None
            
        try:
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': self.api_providers['anthropic']['api_key'],
                'anthropic-version': '2023-06-01'
            }
            
            prompt = self.create_analysis_prompt(object_class)
            
            payload = {
                "model": "claude-3-sonnet-20240229",
                "max_tokens": 500,
                "temperature": 0.1,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": image_base64
                                }
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(
                self.api_providers['anthropic']['endpoint'],
                headers=headers,
                json=payload,
                timeout=self.analysis_settings['max_analysis_time']
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['content'][0]['text']
                try:
                    analysis = json.loads(content)
                    analysis['provider'] = 'Anthropic Claude'
                    return analysis
                except json.JSONDecodeError:
                    print(f"⚠️ Claude 응답 JSON 파싱 실패: {content}")
                    return None
            else:
                print(f"❌ Anthropic API 오류: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Anthropic 분석 실패: {e}")
            return None
    
    def analyze_with_google(self, image_base64: str, object_class: str) -> Optional[Dict]:
        """Google Gemini로 분석"""
        if not self.api_providers['google']['enabled']:
            return None
            
        try:
            headers = {
                'Content-Type': 'application/json'
            }
            
            prompt = self.create_analysis_prompt(object_class)
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt},
                            {
                                "inline_data": {
                                    "mime_type": "image/jpeg",
                                    "data": image_base64
                                }
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.1,
                    "maxOutputTokens": 500
                }
            }
            
            url = f"{self.api_providers['google']['endpoint']}?key={self.api_providers['google']['api_key']}"
            
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=self.analysis_settings['max_analysis_time']
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['candidates'][0]['content']['parts'][0]['text']
                try:
                    analysis = json.loads(content)
                    analysis['provider'] = 'Google Gemini'
                    return analysis
                except json.JSONDecodeError:
                    print(f"⚠️ Gemini 응답 JSON 파싱 실패: {content}")
                    return None
            else:
                print(f"❌ Google API 오류: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Google 분석 실패: {e}")
            return None
    
    def analyze_with_github_copilot(self, image_base64: str, object_class: str) -> Optional[Dict]:
        """GitHub Copilot로 분석"""
        if not self.api_providers['github_copilot']['enabled'] or not self.copilot_integration:
            return None
            
        try:
            # GitHub Copilot 통합을 통한 분석
            object_info = {
                "class_name": object_class,
                "confidence": 0.8
            }
            
            # 이미지 데이터 변환 (base64 -> bytes)
            image_data = base64.b64decode(image_base64) if image_base64 else b""
            
            # Copilot 분석 실행
            result = self.copilot_integration.analyze_object(image_data, object_info)
            
            if result:
                # 표준 형식으로 변환
                analysis = {
                    "brand": result.get("brand", "Unknown"),
                    "model": result.get("model", "Unknown"),
                    "type": result.get("type", object_class),
                    "color": result.get("color", "Unknown"),
                    "distinctive_features": [
                        f"GitHub Copilot suggested {result.get('brand', 'Unknown')} brand",
                        f"Model: {result.get('model', 'Unknown')}",
                        f"Condition: {result.get('condition', 'Good')}"
                    ],
                    "estimated_value": "AI estimated",
                    "condition": result.get("condition", "Good"),
                    "confidence": result.get("confidence", 0.75),
                    "provider": "GitHub Copilot",
                    "source": result.get("source", "github_copilot")
                }
                
                print(f"✅ GitHub Copilot 분석 완료: {analysis['brand']} {analysis['model']}")
                return analysis
            else:
                print("⚠️ GitHub Copilot 분석 결과 없음")
                return None
                
        except Exception as e:
            print(f"❌ GitHub Copilot 분석 실패: {e}")
            return None
    
    def get_object_crop(self, frame: np.ndarray, box: List[float], 
                       padding: float = 0.1) -> np.ndarray:
        """객체 영역 크롭 (패딩 포함)"""
        try:
            x1, y1, x2, y2 = map(int, box)
            height, width = frame.shape[:2]
            
            # 패딩 추가
            pad_w = int((x2 - x1) * padding)
            pad_h = int((y2 - y1) * padding)
            
            # 경계 확인
            x1 = max(0, x1 - pad_w)
            y1 = max(0, y1 - pad_h)
            x2 = min(width, x2 + pad_w)
            y2 = min(height, y2 + pad_h)
            
            crop = frame[y1:y2, x1:x2]
            return crop
            
        except Exception as e:
            print(f"❌ 객체 크롭 실패: {e}")
            return None
    
    def analyze_object_detailed(self, frame: np.ndarray, box: List[float], 
                              object_class: str, confidence: float) -> Optional[Dict]:
        """객체 상세 분석 메인 함수"""
        
        # 신뢰도가 낮으면 분석하지 않음
        if confidence < self.analysis_settings['confidence_threshold']:
            return None
        
        # 우선순위가 낮은 객체는 건너뛰기
        priority = self.analysis_priority.get(object_class, 0)
        if priority < 5:  # 임계값
            return None
        
        # 캐시 확인
        cache_key = f"{object_class}_{int(time.time() // 60)}"  # 1분 단위 캐시
        if cache_key in self.analysis_cache:
            return self.analysis_cache[cache_key]
        
        # 객체 영역 크롭
        crop = self.get_object_crop(frame, box)
        if crop is None or crop.size == 0:
            return None
        
        # 이미지 인코딩
        image_base64 = self.encode_image_to_base64(crop)
        if not image_base64:
            return None
          # 사용 가능한 API로 분석 시도 (우선순위 순)
        analysis_result = None
        
        # GitHub Copilot 최우선 (로컬 처리, 빠름)
        if self.api_providers['github_copilot']['enabled']:
            analysis_result = self.analyze_with_github_copilot(image_base64, object_class)
        
        # GitHub Copilot 실패 시 OpenAI
        if not analysis_result and self.api_providers['openai']['enabled']:
            analysis_result = self.analyze_with_openai(image_base64, object_class)
        
        # OpenAI 실패 시 Anthropic
        if not analysis_result and self.api_providers['anthropic']['enabled']:
            analysis_result = self.analyze_with_anthropic(image_base64, object_class)
        
        # Anthropic 실패 시 Google
        if not analysis_result and self.api_providers['google']['enabled']:
            analysis_result = self.analyze_with_google(image_base64, object_class)
        
        # 결과 캐싱
        if analysis_result:
            self.analysis_cache[cache_key] = analysis_result
            print(f"🔍 {object_class} 상세 분석 완료: {analysis_result.get('brand', 'Unknown')} {analysis_result.get('model', 'Unknown')}")
        
        return analysis_result
    
    def get_detailed_object_name(self, analysis: Dict, original_class: str) -> str:
        """분석 결과를 바탕으로 상세한 객체명 생성"""
        if not analysis:
            return original_class
        
        try:
            parts = []
            
            # 브랜드 추가
            if analysis.get('brand') and analysis['brand'] != 'Unknown':
                parts.append(analysis['brand'])
            
            # 모델 추가
            if analysis.get('model') and analysis['model'] != 'Unknown':
                parts.append(analysis['model'])
            
            # 타입 추가 (브랜드/모델이 없는 경우)
            if not parts and analysis.get('type'):
                parts.append(analysis['type'])
            
            # 색상 추가 (선택적)
            if analysis.get('color') and len(parts) < 2:
                parts.append(analysis['color'])
            
            if parts:
                detailed_name = ' '.join(parts)
                confidence = analysis.get('confidence', 0)
                
                # 신뢰도에 따라 표시 방식 조정
                if confidence > 0.8:
                    return f"{detailed_name}"
                elif confidence > 0.6:
                    return f"{detailed_name} (?)"
                else:
                    return f"{original_class} ({detailed_name}?)"
            
        except Exception as e:
            print(f"⚠️ 상세명 생성 실패: {e}")
        
        return original_class
    
    def clear_cache(self):
        """캐시 정리"""
        current_time = time.time()
        expired_keys = []
        
        for key, data in self.analysis_cache.items():
            if 'timestamp' in data:
                if current_time - data['timestamp'] > self.cache_expire_time:
                    expired_keys.append(key)
        
        for key in expired_keys:
            del self.analysis_cache[key]

# 설정 파일 생성 함수
def create_api_config_template():
    """API 키 설정 템플릿 생성"""
    config_content = """# AI 객체 분석기 API 설정
# 이 파일을 .env로 저장하고 실제 API 키를 입력하세요

# OpenAI API 키 (GPT-4 Vision)
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic API 키 (Claude 3)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Google API 키 (Gemini Pro Vision)
GOOGLE_API_KEY=your_google_api_key_here

# 사용법:
# 1. 위 API 키들 중 하나 이상을 실제 키로 교체
# 2. 파일명을 .env로 변경
# 3. 프로그램 실행 전에 환경변수로 로드
"""
    
    with open('api_config_template.txt', 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print("📝 API 설정 템플릿이 생성되었습니다: api_config_template.txt")

if __name__ == "__main__":
    # 테스트 코드
    analyzer = AIObjectAnalyzer()
    create_api_config_template()
    
    print("🤖 AI 객체 분석기 테스트 완료")
    print("💡 실제 사용을 위해서는 API 키 설정이 필요합니다.")
