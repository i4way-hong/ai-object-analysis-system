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
import subprocess
import json
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

def setup_github_copilot():
    """GitHub Copilot 설정 도우미"""
    print("🚀" + "="*50)
    print("🤖 GitHub Copilot 설정 도우미")
    print("="*50)
    
    # VS Code 설치 확인
    vscode_installed = check_vscode_installation()
    github_cli_installed = check_github_cli_installation()
    
    if not vscode_installed and not github_cli_installed:
        print("❌ VS Code와 GitHub CLI 모두 설치되지 않았습니다.")
        print("\n📝 설치 옵션을 선택하세요:")
        print("1. VS Code + GitHub Copilot 확장 (추천)")
        print("2. GitHub CLI")
        print("3. 수동 설치 가이드 보기")
        
        choice = input("\n선택 (1-3): ").strip()
        
        if choice == "1":
            install_vscode_and_copilot()
        elif choice == "2":
            install_github_cli()
        elif choice == "3":
            show_manual_installation_guide()
        else:
            print("❌ 잘못된 선택입니다.")
            return False
    
    elif vscode_installed and not github_cli_installed:
        print("✅ VS Code가 설치되어 있습니다.")
        install_copilot_extension()
    
    elif not vscode_installed and github_cli_installed:
        print("✅ GitHub CLI가 설치되어 있습니다.")
        setup_github_cli_copilot()
    
    else:
        print("✅ VS Code와 GitHub CLI 모두 설치되어 있습니다.")
        print("GitHub Copilot 확장 상태를 확인합니다...")
        check_copilot_status()
    
    return True

def check_vscode_installation() -> bool:
    """VS Code 설치 여부 확인"""
    try:
        result = subprocess.run(['code', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✅ VS Code 설치됨: {version}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ VS Code가 설치되지 않았습니다.")
    return False

def check_github_cli_installation() -> bool:
    """GitHub CLI 설치 여부 확인"""
    try:
        result = subprocess.run(['gh', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version_info = result.stdout.split('\n')[0]
            print(f"✅ GitHub CLI 설치됨: {version_info}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ GitHub CLI가 설치되지 않았습니다.")
    return False

def install_vscode_and_copilot():
    """VS Code 및 GitHub Copilot 확장 설치"""
    print("\n🔧 VS Code 및 GitHub Copilot 설치 중...")
    
    # VS Code 다운로드 링크 제공
    print("1️⃣ VS Code 설치:")
    print("   • https://code.visualstudio.com/download")
    print("   • Windows x64 User Installer 다운로드")
    
    input("\nVS Code 설치 완료 후 Enter를 누르세요...")
    
    # VS Code 설치 확인
    if check_vscode_installation():
        install_copilot_extension()
    else:
        print("❌ VS Code 설치가 완료되지 않았습니다.")

def install_copilot_extension():
    """GitHub Copilot 확장 설치"""
    print("\n2️⃣ GitHub Copilot 확장 설치 중...")
    
    try:
        # GitHub Copilot 확장 설치
        result = subprocess.run([
            'code', '--install-extension', 'github.copilot'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ GitHub Copilot 확장 설치 완료!")
            
            # Copilot Chat 확장도 설치
            result2 = subprocess.run([
                'code', '--install-extension', 'github.copilot-chat'
            ], capture_output=True, text=True, timeout=30)
            
            if result2.returncode == 0:
                print("✅ GitHub Copilot Chat 확장 설치 완료!")
            
            print("\n🎯 다음 단계:")
            print("1. VS Code를 다시 시작하세요")
            print("2. GitHub 계정으로 로그인하세요")
            print("3. Copilot 구독을 활성화하세요")
            
        else:
            print(f"❌ 확장 설치 실패: {result.stderr}")
            print("\n수동 설치 방법:")
            print("1. VS Code 실행")
            print("2. Ctrl+Shift+X (확장 패널)")
            print("3. 'GitHub Copilot' 검색 및 설치")
            
    except Exception as e:
        print(f"❌ 확장 설치 중 오류: {e}")

def install_github_cli():
    """GitHub CLI 설치 가이드"""
    print("\n🔧 GitHub CLI 설치:")
    print("1️⃣ Winget 사용 (Windows 10/11):")
    print("   winget install --id GitHub.cli")
    print("\n2️⃣ 수동 다운로드:")
    print("   • https://cli.github.com/")
    print("   • Windows msi 파일 다운로드")
    
    input("\nGitHub CLI 설치 완료 후 Enter를 누르세요...")
    
    if check_github_cli_installation():
        setup_github_cli_copilot()

def setup_github_cli_copilot():
    """GitHub CLI Copilot 설정"""
    print("\n3️⃣ GitHub CLI 로그인 및 Copilot 설정:")
    
    try:
        # GitHub 로그인 상태 확인
        result = subprocess.run(['gh', 'auth', 'status'], 
                              capture_output=True, text=True, timeout=10)
        
        if "Logged in to github.com" not in result.stderr:
            print("GitHub에 로그인하세요:")
            subprocess.run(['gh', 'auth', 'login'], timeout=60)
        else:
            print("✅ GitHub에 이미 로그인되어 있습니다.")
        
        # Copilot 확장 설치
        print("GitHub CLI Copilot 확장 설치 중...")
        result = subprocess.run(['gh', 'extension', 'install', 'github/gh-copilot'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ GitHub CLI Copilot 확장 설치 완료!")
        else:
            print("⚠️ Copilot 확장이 이미 설치되어 있거나 설치에 실패했습니다.")
        
    except Exception as e:
        print(f"❌ GitHub CLI 설정 중 오류: {e}")

def check_copilot_status():
    """현재 GitHub Copilot 상태 확인"""
    print("\n🔍 GitHub Copilot 상태 확인:")
    
    # VS Code 확장 확인
    try:
        result = subprocess.run(['code', '--list-extensions'], 
                              capture_output=True, text=True, timeout=10)
        
        extensions = result.stdout.lower()
        copilot_installed = 'github.copilot' in extensions
        copilot_chat_installed = 'github.copilot-chat' in extensions
        
        print(f"VS Code GitHub Copilot: {'✅ 설치됨' if copilot_installed else '❌ 없음'}")
        print(f"VS Code Copilot Chat: {'✅ 설치됨' if copilot_chat_installed else '❌ 없음'}")
        
    except Exception as e:
        print(f"VS Code 확장 확인 실패: {e}")
    
    # GitHub CLI Copilot 확인
    try:
        result = subprocess.run(['gh', 'extension', 'list'], 
                              capture_output=True, text=True, timeout=10)
        
        gh_copilot_installed = 'gh-copilot' in result.stdout
        print(f"GitHub CLI Copilot: {'✅ 설치됨' if gh_copilot_installed else '❌ 없음'}")
        
    except Exception as e:
        print(f"GitHub CLI 확인 실패: {e}")
    
    # AI 분석기에서 Copilot 사용 가능 여부 확인
    try:
        from github_copilot_integration import GitHubCopilotIntegration
        copilot = GitHubCopilotIntegration()
        is_available = copilot.is_available()
        print(f"AI 분석기 연동: {'✅ 사용 가능' if is_available else '❌ 사용 불가'}")
        
        if is_available:
            print("\n🎉 GitHub Copilot이 AI 분석에 사용 가능합니다!")
        else:
            print("\n⚠️ GitHub Copilot 설정을 완료해주세요.")
            
    except Exception as e:
        print(f"AI 분석기 연동 확인 실패: {e}")

def show_manual_installation_guide():
    """수동 설치 가이드"""
    print("\n📖 GitHub Copilot 수동 설치 가이드:")
    print("="*50)
    
    print("\n🎯 방법 1: VS Code + GitHub Copilot (추천)")
    print("1. VS Code 설치: https://code.visualstudio.com/")
    print("2. VS Code 실행 → Ctrl+Shift+X")
    print("3. 'GitHub Copilot' 검색 및 설치")
    print("4. 'GitHub Copilot Chat' 검색 및 설치")
    print("5. GitHub 계정으로 로그인")
    print("6. Copilot 구독 활성화")
    
    print("\n🎯 방법 2: GitHub CLI")
    print("1. GitHub CLI 설치: https://cli.github.com/")
    print("2. PowerShell에서 실행:")
    print("   gh auth login")
    print("   gh extension install github/gh-copilot")
    
    print("\n💡 참고:")
    print("• GitHub Copilot은 유료 서비스입니다 ($10/월)")
    print("• 학생은 GitHub Student Pack으로 무료 사용 가능")
    print("• 개인 프로젝트에 60일 무료 체험 제공")

def test_api_keys():
    """API 키 테스트"""
    print("🔍 API 키 테스트 중...")
    
    # 환경변수 확인
    apis = {
        'OpenAI': os.getenv('OPENAI_API_KEY'),
        'Anthropic': os.getenv('ANTHROPIC_API_KEY'),
        'Google': os.getenv('GOOGLE_API_KEY')
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
        return True
    else:
        print("\n⚠️ 설정된 API가 없습니다.")
        print("\n📝 AI API 설정 방법:")
        print("1. PowerShell에서 환경변수 설정:")
        print('   $env:OPENAI_API_KEY="sk-your-actual-openai-key"')
        print('   $env:ANTHROPIC_API_KEY="sk-ant-your-actual-anthropic-key"')
        print('   $env:GOOGLE_API_KEY="your-actual-google-key"')
        print("\n2. GitHub Copilot 사용:")
        print("   - VS Code에서 GitHub Copilot 확장 설치")
        print("   - 또는 GitHub CLI 설치 및 로그인")
        print("\n3. 또는 sample.env 파일을 편집하여 실제 키 입력")
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
    print("1️⃣ AI 제공자 설정:")
    print("   🚀 GitHub Copilot (추천):")
    print("      python ai_setup_tool.py copilot")
    print("   🧠 클라우드 AI API:")
    print("      • OpenAI: https://platform.openai.com/api-keys")
    print("      • Anthropic: https://console.anthropic.com/")
    print("      • Google: https://ai.google.dev/")
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
    print("💡 AI 분석 우선순위:")
    print("   1. 🚀 GitHub Copilot (빠름, API 키 불필요)")
    print("   2. 🧠 OpenAI GPT-4 (고정밀)")
    print("   3. 🎯 Anthropic Claude (상세)")
    print("   4. 🌟 Google Gemini (빠름)")
    print()
    print("🎯 분석 예시:")
    print("   • 스마트폰 → iPhone 14 Pro, Galaxy S23 등")
    print("   • 자동차 → BMW X5, Tesla Model 3 등")
    print("   • 노트북 → MacBook Pro, ThinkPad 등")
    print("="*60)

def main():
    if len(sys.argv) < 2:
        print("🔧 AI 객체 분석기 설정 도구")
        print()
        print("사용법:")
        print("  python ai_setup_tool.py env       # 샘플 환경변수 파일 생성")
        print("  python ai_setup_tool.py test      # API 키 테스트")
        print("  python ai_setup_tool.py copilot   # GitHub Copilot 설정")
        print("  python ai_setup_tool.py guide     # 사용법 가이드")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'env':
        create_sample_env_file()
    elif command == 'test':
        test_ai_analysis()
    elif command == 'copilot':
        setup_github_copilot()
    elif command == 'guide':
        show_usage_guide()
    else:
        print(f"❌ 알 수 없는 명령어: {command}")
        print("\n사용 가능한 명령어: env, test, copilot, guide")

if __name__ == "__main__":
    main()
