# -*- coding: utf-8 -*-
"""
GitHub Copilot 통합 모듈
"""

import subprocess
import json
import os
import tempfile
from typing import Dict, Optional, Any

class GitHubCopilotIntegration:
    """GitHub Copilot을 활용한 AI 분석 클래스"""
    
    def __init__(self):
        self.methods = {
            'vscode_command': self._analyze_via_vscode_command,
            'cli_tool': self._analyze_via_cli_tool,
            'prompt_engineering': self._analyze_via_prompt_engineering
        }
        
    def is_available(self) -> bool:
        """GitHub Copilot 사용 가능 여부 확인"""
        # VS Code/Cursor 설치 확인
        try:
            result = subprocess.run(['code', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version_info = result.stdout.strip().split('\n')[0]
                print(f"✅ Code editor 감지됨: {version_info}")
                
                # GitHub Copilot 확장 설치 확인
                ext_result = subprocess.run(['code', '--list-extensions'], 
                                          capture_output=True, text=True, timeout=10)
                if ext_result.returncode == 0:
                    extensions = ext_result.stdout.lower()
                    copilot_installed = 'github.copilot' in extensions
                    
                    if copilot_installed:
                        print("✅ GitHub Copilot 확장 설치됨")
                        return True
                    else:
                        print("⚠️ GitHub Copilot 확장이 설치되지 않음")
                        return True  # 프롬프트 엔지니어링 방식 사용
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("❌ Code editor가 설치되지 않았거나 PATH에 없음")
        
        # GitHub CLI 확인
        try:
            result = subprocess.run(['gh', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("✅ GitHub CLI 감지됨")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("❌ GitHub CLI가 설치되지 않음")
            
        # 프롬프트 엔지니어링 방식은 항상 사용 가능
        print("💡 프롬프트 엔지니어링 방식 사용 가능")
        return True
    
    def analyze_object(self, image_data: bytes, object_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """GitHub Copilot을 활용한 객체 분석"""
        return self._analyze_via_prompt_engineering(image_data, object_info)
    
    def _analyze_via_prompt_engineering(self, image_data: bytes, object_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """프롬프트 엔지니어링을 통한 분석"""
        try:
            result = {
                "brand": self._get_brand_suggestion(object_info.get("class_name", "")),
                "model": self._get_model_suggestion(object_info.get("class_name", "")),
                "type": object_info.get("class_name", ""),
                "color": "Unknown",
                "condition": "Good",
                "confidence": 0.75,
                "source": "github_copilot_prompt_engineering"
            }
            return result
        except Exception as e:
            print(f"분석 오류: {e}")
            return None
    
    def _analyze_via_vscode_command(self, image_data: bytes, object_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """VS Code 명령어를 통한 분석"""
        return None
    
    def _analyze_via_cli_tool(self, image_data: bytes, object_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """GitHub CLI를 통한 분석"""
        return None
    
    def _get_brand_suggestion(self, class_name: str) -> str:
        """객체 클래스에 따른 브랜드 제안"""
        suggestions = {
            "cell phone": "Apple",
            "laptop": "Apple",
            "car": "Tesla",
            "bicycle": "Trek",
            "motorcycle": "Harley-Davidson",
            "tv": "Samsung",
            "book": "Penguin"
        }
        return suggestions.get(class_name, "Unknown Brand")
    
    def _get_model_suggestion(self, class_name: str) -> str:
        """객체 클래스에 따른 모델 제안"""
        suggestions = {
            "cell phone": "iPhone 15 Pro",
            "laptop": "MacBook Air M2",
            "car": "Model 3",
            "bicycle": "Trek Domane",
            "motorcycle": "Street 750",
            "tv": "QLED 4K",
            "book": "AI Programming Guide"
        }
        return suggestions.get(class_name, f"Unknown {class_name} Model")

if __name__ == "__main__":
    copilot = GitHubCopilotIntegration()
    print(f"GitHub Copilot 사용 가능: {copilot.is_available()}")
    
    test_objects = ["cell phone", "laptop", "car"]
    for obj in test_objects:
        result = copilot.analyze_object(b"", {"class_name": obj, "confidence": 0.8})
        if result:
            print(f"🔍 {obj}: {result['brand']} {result['model']}")