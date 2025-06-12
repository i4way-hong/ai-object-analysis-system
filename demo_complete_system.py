#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 AI 객체 상세 분석 시스템 완전 데모
폰트 품질 개선 + AI API 분석 통합 시스템
"""

import cv2
import numpy as np
import time
import os
from ultralytics import YOLO
from ui_design_improved import ImprovedUIDesign
from ai_object_analyzer import AIObjectAnalyzer
import argparse

class CompleteSystemDemo:
    """완전한 AI 객체 분석 시스템 데모"""
    
    def __init__(self):
        # UI 디자인 시스템 초기화
        print("🎨 개선된 UI 디자인 시스템 로드...")
        self.ui_design = ImprovedUIDesign()
        
        # AI 분석기 초기화
        print("🤖 AI 객체 상세 분석기 로드...")
        try:
            self.ai_analyzer = AIObjectAnalyzer()
            self.use_ai_analysis = True
            print("✅ AI 분석기 로드 성공")
        except Exception as e:
            self.ai_analyzer = None
            self.use_ai_analysis = False
            print(f"⚠️ AI 분석기 로드 실패: {e}")
        
        # YOLO 모델 로드
        print("🔍 YOLO11 모델 로드...")
        self.model = YOLO('yolo11n.pt')
        self.model.conf = 0.5
        print("✅ YOLO11 Nano 모델 로드 완료")
        
        # 데모 설정
        self.tracked_objects = {}
        self.next_id = 1
        self.frame_count = 0
        self.ai_analysis_interval = 5  # 5프레임마다 AI 분석
        
    def create_demo_image(self):
        """데모용 이미지 생성 (가상 객체들)"""
        # 800x600 검은 배경
        demo_image = np.zeros((600, 800, 3), dtype=np.uint8)
        
        # 배경 그라데이션
        for i in range(600):
            ratio = i / 600
            color = int(30 + ratio * 20)
            cv2.line(demo_image, (0, i), (800, i), (color, color, color), 1)
        
        # 가상 객체들 그리기
        objects = [
            {"name": "person", "box": [100, 150, 250, 400], "conf": 0.85},
            {"name": "car", "box": [400, 250, 650, 450], "conf": 0.92},
            {"name": "cell phone", "box": [200, 100, 280, 160], "conf": 0.78},
            {"name": "laptop", "box": [300, 350, 500, 450], "conf": 0.88},
        ]
        
        # 객체 윤곽선 그리기
        colors = [(52, 152, 219), (46, 204, 113), (231, 76, 60), (155, 89, 182)]
        for i, obj in enumerate(objects):
            x1, y1, x2, y2 = obj["box"]
            color = colors[i % len(colors)]
            
            # 객체 영역 채우기 (반투명)
            overlay = demo_image.copy()
            cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)
            cv2.addWeighted(demo_image, 0.7, overlay, 0.3, 0, demo_image)
            
            # 테두리
            cv2.rectangle(demo_image, (x1, y1), (x2, y2), color, 2)
            
            # 중앙에 객체명 표시
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            text = f"{obj['name']}"
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
            text_x = center_x - text_size[0] // 2
            text_y = center_y + text_size[1] // 2
            
            cv2.putText(demo_image, text, (text_x, text_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return demo_image, objects
    
    def simulate_detection(self, objects):
        """실제 YOLO 검출 결과를 시뮬레이션"""
        detections = []
        for obj in objects:
            detection_data = {
                'box': obj['box'],
                'class': obj['name'],
                'confidence': obj['conf']
            }
            detections.append(detection_data)
        return detections
    
    def update_tracked_objects(self, detections):
        """추적 객체 업데이트"""
        for i, detection in enumerate(detections):
            obj_id = i + 1
            if obj_id not in self.tracked_objects:
                self.tracked_objects[obj_id] = {
                    'box': detection['box'],
                    'class': detection['class'],
                    'confidence': detection['confidence'],
                    'stable_count': 1,
                    'avg_confidence': detection['confidence'],
                    'total_frames': 1,
                }
            else:
                # 기존 객체 업데이트
                self.tracked_objects[obj_id]['stable_count'] += 1
                self.tracked_objects[obj_id]['total_frames'] += 1
                frames = self.tracked_objects[obj_id]['total_frames']
                old_avg = self.tracked_objects[obj_id]['avg_confidence']
                new_conf = detection['confidence']
                self.tracked_objects[obj_id]['avg_confidence'] = (old_avg * (frames-1) + new_conf) / frames
    
    def add_ai_analysis(self, obj_data):
        """AI 분석 정보 시뮬레이션 (실제 API 없을 때)"""
        class_name = obj_data['class']
        
        # 시뮬레이션된 AI 분석 결과
        ai_analysis_samples = {
            'person': {
                'brand': 'Human',
                'model': 'Adult Male',
                'type': 'Standing Person',
                'color': 'Blue Shirt',
                'condition': 'Active',
                'confidence': 0.89
            },
            'car': {
                'brand': 'Toyota',
                'model': 'Camry 2023',
                'type': 'Sedan',
                'color': 'Silver',
                'condition': 'Good',
                'confidence': 0.92
            },
            'cell phone': {
                'brand': 'Apple',
                'model': 'iPhone 14 Pro',
                'type': 'Smartphone',
                'color': 'Space Gray',
                'condition': 'Excellent',
                'confidence': 0.87
            },
            'laptop': {
                'brand': 'MacBook',
                'model': 'MacBook Pro M2',
                'type': 'Laptop Computer',
                'color': 'Space Gray',
                'condition': 'New',
                'confidence': 0.91
            }
        }
        
        if class_name in ai_analysis_samples:
            analysis = ai_analysis_samples[class_name]
            obj_data['ai_analysis'] = analysis
            obj_data['detailed_name'] = f"{analysis['brand']} {analysis['model']}"
        
        return obj_data
    
    def run_demo(self, mode='static'):
        """데모 실행"""
        print("🚀" + "="*60)
        print("🎯 AI 객체 상세 분석 시스템 완전 데모")
        print("="*60)
        print(f"🎨 개선된 폰트 시스템: ✅")
        print(f"🤖 AI 상세 분석 시스템: {'✅' if self.use_ai_analysis else '❌'}")
        print(f"📊 YOLO11 객체 감지: ✅")
        print("")
        
        if mode == 'static':
            # 정적 이미지 데모
            print("📸 정적 이미지 데모 모드")
            demo_image, objects = self.create_demo_image()
            detections = self.simulate_detection(objects)
            self.update_tracked_objects(detections)
            
            # AI 분석 추가
            for obj_id, obj_data in self.tracked_objects.items():
                if self.frame_count % self.ai_analysis_interval == 0:
                    obj_data = self.add_ai_analysis(obj_data)
            
            # UI 오버레이 그리기
            for obj_id, obj_data in self.tracked_objects.items():
                self.ui_design.draw_modern_info_card(demo_image, obj_id, obj_data)
            
            # 정보 패널 추가
            tracker_info = {
                'model_name': '🚀 YOLO11 Nano',
                'fps': 30.0,
                'object_count': len(self.tracked_objects),
                'accuracy': 87.5,
                'stable_objects': len(self.tracked_objects),
                'model_params': '2.6M'
            }
            
            final_image = self.ui_design.draw_modern_info_panel(demo_image, tracker_info)
            
            # 결과 표시
            cv2.namedWindow('🚀 AI 객체 상세 분석 시스템 데모', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('🚀 AI 객체 상세 분석 시스템 데모', 1200, 800)
            cv2.imshow('🚀 AI 객체 상세 분석 시스템 데모', final_image)
            
            print("💡 키보드 조작:")
            print("  - 's': 스크린샷 저장")
            print("  - 'q': 종료")
            print("")
            
            while True:
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    timestamp = int(time.time())
                    filename = f'ai_analysis_demo_{timestamp}.jpg'
                    cv2.imwrite(filename, final_image)
                    print(f"📸 스크린샷 저장: {filename}")
            
            cv2.destroyAllWindows()
        
        else:
            # 동적 데모 (애니메이션)
            print("🎬 동적 애니메이션 데모 모드")
            # 향후 구현 가능
            
        print("🚀 데모가 완료되었습니다!")

def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description='AI 객체 상세 분석 시스템 완전 데모')
    parser.add_argument('--mode', choices=['static', 'dynamic'], default='static',
                        help='데모 모드 선택')
    args = parser.parse_args()
    
    # 시스템 요구사항 확인
    print("🔍 시스템 요구사항 확인...")
    
    required_files = [
        'ui_design_improved.py',
        'ai_object_analyzer.py',
        'yolo11n.pt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ 필수 파일이 없습니다: {missing_files}")
        return
    
    print("✅ 모든 필수 파일 확인됨")
    
    # 데모 실행
    demo = CompleteSystemDemo()
    demo.run_demo(args.mode)

if __name__ == "__main__":
    main()
