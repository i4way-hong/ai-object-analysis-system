#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 AI 객체 상세 분석 시스템 - 간편 실행기
"""

import sys
import os
import subprocess

def print_banner():
    """시스템 배너 출력"""
    print("🚀" + "="*60)
    print("🎯 AI 객체 상세 분석 시스템")
    print("="*60)

def check_requirements():
    """필수 파일 및 패키지 확인"""
    print("🔍 시스템 요구사항 확인 중...")
    
    required_files = [
        'ui_design_improved.py',
        'ai_object_analyzer.py', 
        'yolo11_tracker.py',
        'yolo11n.pt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ 필수 파일 누락: {missing_files}")
        return False
    
    print("✅ 모든 필수 파일 확인됨")
    return True

def show_menu():
    """메인 메뉴 표시"""
    print("\n📋 실행 옵션을 선택하세요:")
    print("  1. 🚀 웹캠으로 실시간 객체 분석 (기본)")
    print("  2. 🎨 시스템 데모 보기")
    print("  3. 🔧 AI API 설정 및 테스트")
    print("  4. 📊 시스템 정보 보기")
    print("  0. 🚪 종료")
    print("")

def run_webcam_analysis():
    """웹캠 분석 실행"""
    print("\n🚀 웹캠 실시간 분석을 시작합니다...")
    print("")
    print("📹 모델 크기를 선택하세요:")
    print("  n: Nano (가장 빠름, 39.5% 정확도)")
    print("  s: Small (빠름, 47.0% 정확도)")
    print("  m: Medium (보통, 51.5% 정확도) ⭐ 추천")
    print("  l: Large (느림, 53.4% 정확도)")
    print("  x: Extra Large (가장 느림, 54.7% 정확도)")
    print("")
    
    while True:
        model = input("모델 선택 (n/s/m/l/x) [기본값: m]: ").strip().lower()
        if not model:
            model = 'm'
        if model in ['n', 's', 'm', 'l', 'x']:
            break
        print("❌ 잘못된 입력입니다. n, s, m, l, x 중 선택하세요.")
    
    print(f"\n🎯 YOLO11-{model.upper()} 모델로 실행합니다...")
    print("💡 실행 중 조작법:")
    print("   - q: 종료")
    print("   - s: 스크린샷 저장")
    print("   - m: 모델 변경")
    print("   - i: 정보 패널 토글")
    print("")
    
    try:
        subprocess.run([sys.executable, 'yolo11_tracker.py', '0', model], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 실행 오류: {e}")
    except KeyboardInterrupt:
        print("\n🔚 사용자에 의해 중단되었습니다.")

def run_demo():
    """시스템 데모 실행"""
    print("\n🎨 시스템 데모를 실행합니다...")
    print("   - AI 상세 분석 정보")
    print("")
    
    try:
        subprocess.run([sys.executable, 'demo_complete_system.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 데모 실행 오류: {e}")
    except KeyboardInterrupt:
        print("\n🔚 데모가 중단되었습니다.")

def setup_ai_api():
    """AI API 설정"""
    print("\n🔧 AI API 설정 및 테스트...")
    print("")
    print("📋 사용 가능한 옵션:")
    print("  1. API 키 테스트")
    print("  2. 샘플 환경변수 파일 생성")
    print("  3. API 설정 가이드 보기")
    print("")
    
    choice = input("선택 (1/2/3): ").strip()
    
    try:
        if choice == '1':
            subprocess.run([sys.executable, 'ai_setup_tool.py', 'test'], check=True)
        elif choice == '2':
            subprocess.run([sys.executable, 'ai_setup_tool.py', 'env'], check=True)
        elif choice == '3':
            subprocess.run([sys.executable, 'ai_setup_tool.py', 'guide'], check=True)
        else:
            print("❌ 잘못된 선택입니다.")
    except subprocess.CalledProcessError as e:
        print(f"❌ 실행 오류: {e}")

def show_system_info():
    """시스템 정보 표시"""
    print("\n📊 시스템 정보:")
    print("="*50)
    print("🎨 폰트 시스템: Calibri TrueType")
    print("🤖 AI 분석: OpenAI, Anthropic, Google 지원")
    print("🚀 YOLO 모델: YOLO11 (Nano~Extra Large)")
    print("")
    print("📁 핵심 파일:")
    print("   - ui_design_improved.py (UI 시스템)")
    print("   - ai_object_analyzer.py (AI 분석)")
    print("   - yolo11_tracker.py (메인 트래커)")
    print("")
    print("🔧 설정 파일:")
    print("   - sample.env (API 키 템플릿)")
    print("   - ai_setup_tool.py (설정 도구)")
    print("")

def main():
    """메인 함수"""
    print_banner()
    
    if not check_requirements():
        print("\n❌ 시스템을 실행할 수 없습니다. 필수 파일을 확인하세요.")
        return
    
    while True:
        show_menu()
        
        try:
            choice = input("선택: ").strip()
            
            if choice == '1':
                run_webcam_analysis()
            elif choice == '2':
                run_demo()
            elif choice == '3':
                setup_ai_api()
            elif choice == '4':
                show_system_info()
            elif choice == '0':
                print("\n🚪 프로그램을 종료합니다.")
                break
            else:
                print("❌ 잘못된 선택입니다. 0-4 중에서 선택하세요.")
                
        except KeyboardInterrupt:
            print("\n\n🚪 프로그램을 종료합니다.")
            break
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
    
if __name__ == "__main__":
    main()
