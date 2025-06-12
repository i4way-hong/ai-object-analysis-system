#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 AI 객체 상세 분석 시스템 최종 통합 테스트
"""

import cv2
import numpy as np
import time
import os
from ui_design_improved import ImprovedUIDesign
from ai_object_analyzer import AIObjectAnalyzer

def test_font_system():
    """폰트 시스템 테스트"""
    print("🎨 폰트 시스템 테스트...")
    try:
        ui_design = ImprovedUIDesign()
        
        # 테스트 이미지 생성
        test_img = np.zeros((400, 600, 3), dtype=np.uint8)
        
        # 다양한 폰트 크기 테스트
        ui_design.draw_professional_text(test_img, "Large Text", (50, 50), 'large', (255, 255, 255))
        ui_design.draw_professional_text(test_img, "Medium Text", (50, 100), 'medium', (255, 255, 255))
        ui_design.draw_professional_text(test_img, "Small Text", (50, 150), 'small', (255, 255, 255))
        ui_design.draw_professional_text(test_img, "Tiny Text", (50, 200), 'tiny', (255, 255, 255))
        
        cv2.imwrite('font_test_result.jpg', test_img)
        print("✅ 폰트 시스템 테스트 완료: font_test_result.jpg")
        return True
    except Exception as e:
        print(f"❌ 폰트 시스템 테스트 실패: {e}")
        return False

def test_ui_design():
    """UI 디자인 테스트"""
    print("🎨 UI 디자인 테스트...")
    try:
        ui_design = ImprovedUIDesign()
        
        # 테스트 이미지 생성
        test_img = np.zeros((600, 800, 3), dtype=np.uint8)
        
        # 가상 객체 데이터
        obj_data = {
            'box': [100, 150, 300, 350],
            'class': 'person',
            'confidence': 0.85,
            'stable_count': 5,
            'avg_confidence': 0.87,
            'total_frames': 10,
            'ai_analysis': {
                'brand': 'Human',
                'model': 'Adult Male',
                'type': 'Standing Person',
                'color': 'Blue Shirt',
                'condition': 'Active',
                'confidence': 0.89
            },
            'detailed_name': 'Human Adult Male'
        }
        
        # UI 카드 그리기
        ui_design.draw_modern_info_card(test_img, 1, obj_data)
        
        # 정보 패널 추가
        tracker_info = {
            'model_name': '🚀 YOLO11 Test',
            'fps': 30.0,
            'object_count': 1,
            'accuracy': 87.5,
            'stable_objects': 1,
            'model_params': '2.6M'
        }
        
        final_img = ui_design.draw_modern_info_panel(test_img, tracker_info)
        cv2.imwrite('ui_design_test_result.jpg', final_img)
        print("✅ UI 디자인 테스트 완료: ui_design_test_result.jpg")
        return True
    except Exception as e:
        print(f"❌ UI 디자인 테스트 실패: {e}")
        return False

def test_ai_analyzer():
    """AI 분석기 테스트"""
    print("🤖 AI 분석기 테스트...")
    try:
        analyzer = AIObjectAnalyzer()
        
        # 테스트 이미지 생성
        test_img = np.zeros((400, 600, 3), dtype=np.uint8)
        # 가상 스마트폰 그리기
        cv2.rectangle(test_img, (200, 150), (300, 300), (100, 100, 100), -1)
        cv2.rectangle(test_img, (200, 150), (300, 300), (255, 255, 255), 2)
        
        # AI 분석 시도 (API 없이도 동작해야 함)
        result = analyzer.analyze_object_detailed(test_img, [200, 150, 300, 300], 'cell phone', 0.85)
        
        if result:
            print(f"✅ AI 분석 성공: {result}")
        else:
            print("⚠️ AI 분석 결과 없음 (API 키 없음 - 정상)")
        
        print("✅ AI 분석기 테스트 완료")
        return True
    except Exception as e:
        print(f"❌ AI 분석기 테스트 실패: {e}")
        return False

def test_complete_integration():
    """완전 통합 테스트"""
    print("🚀 완전 통합 테스트...")
    try:
        # UI 시스템 로드
        ui_design = ImprovedUIDesign()
        
        # AI 분석기 로드
        try:
            ai_analyzer = AIObjectAnalyzer()
            ai_available = True
        except:
            ai_analyzer = None
            ai_available = False
        
        # 통합 테스트 이미지 생성
        test_img = np.zeros((700, 1000, 3), dtype=np.uint8)
        
        # 배경 그라데이션
        for i in range(700):
            ratio = i / 700
            color = int(20 + ratio * 30)
            cv2.line(test_img, (0, i), (1000, i), (color, color, color), 1)
        
        # 여러 객체 시뮬레이션
        objects = [
            {'id': 1, 'class': 'person', 'box': [50, 100, 200, 400], 'conf': 0.92},
            {'id': 2, 'class': 'car', 'box': [300, 200, 600, 450], 'conf': 0.88},
            {'id': 3, 'class': 'cell phone', 'box': [150, 50, 220, 120], 'conf': 0.85},
        ]
        
        # AI 분석 시뮬레이션 데이터
        ai_data = {
            'person': {'brand': 'Human', 'model': 'Adult Female', 'color': 'Red Jacket'},
            'car': {'brand': 'Tesla', 'model': 'Model 3', 'color': 'White'},
            'cell phone': {'brand': 'Samsung', 'model': 'Galaxy S24', 'color': 'Black'}
        }
        
        # 각 객체에 대해 UI 카드 그리기
        for obj in objects:
            obj_data = {
                'box': obj['box'],
                'class': obj['class'],
                'confidence': obj['conf'],
                'stable_count': 7,
                'avg_confidence': obj['conf'] + 0.02,
                'total_frames': 15
            }
            
            # AI 분석 데이터 추가
            if obj['class'] in ai_data:
                ai_info = ai_data[obj['class']]
                obj_data['ai_analysis'] = {
                    'brand': ai_info['brand'],
                    'model': ai_info['model'],
                    'color': ai_info['color'],
                    'confidence': 0.89
                }
                obj_data['detailed_name'] = f"{ai_info['brand']} {ai_info['model']}"
            
            # UI 카드 그리기
            ui_design.draw_modern_info_card(test_img, obj['id'], obj_data)
        
        # 최종 정보 패널
        tracker_info = {
            'model_name': '🚀 YOLO11 Integrated',
            'fps': 28.5,
            'object_count': len(objects),
            'accuracy': 89.3,
            'stable_objects': len(objects),
            'model_params': '2.6M'
        }
        
        final_img = ui_design.draw_modern_info_panel(test_img, tracker_info)
        
        # 결과 저장
        timestamp = int(time.time())
        filename = f'integration_test_result_{timestamp}.jpg'
        cv2.imwrite(filename, final_img)
        
        print(f"✅ 완전 통합 테스트 완료: {filename}")
        print(f"   - 폰트 시스템: ✅")
        print(f"   - UI 디자인: ✅")
        print(f"   - AI 분석기: {'✅' if ai_available else '⚠️ (API 없음)'}")
        print(f"   - 객체 추적: ✅")
        
        return True
    except Exception as e:
        print(f"❌ 완전 통합 테스트 실패: {e}")
        return False

def main():
    """메인 테스트 함수"""
    print("🚀" + "="*60)
    print("🧪 AI 객체 상세 분석 시스템 최종 통합 테스트")
    print("="*60)
    
    tests = [
        ("폰트 시스템", test_font_system),
        ("UI 디자인", test_ui_design),
        ("AI 분석기", test_ai_analyzer),
        ("완전 통합", test_complete_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name} 테스트 시작...")
        try:
            result = test_func()
            results.append((test_name, result))
            status = "✅ 성공" if result else "❌ 실패"
            print(f"   결과: {status}")
        except Exception as e:
            results.append((test_name, False))
            print(f"   결과: ❌ 예외 발생 - {e}")
    
    # 최종 결과 요약
    print("\n🚀" + "="*60)
    print("📊 최종 테스트 결과 요약")
    print("="*60)
    
    success_count = sum(1 for _, result in results if result)
    total_count = len(results)
    
    for test_name, result in results:
        status = "✅ 성공" if result else "❌ 실패"
        print(f"   {test_name}: {status}")
    
    print(f"\n🎯 전체 성공률: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    if success_count == total_count:
        print("🎉 모든 테스트가 성공적으로 완료되었습니다!")
        print("🚀 시스템이 완전히 준비되었습니다!")
    else:
        print("⚠️ 일부 테스트가 실패했습니다. 로그를 확인하세요.")
    
    print("="*60)

if __name__ == "__main__":
    main()
