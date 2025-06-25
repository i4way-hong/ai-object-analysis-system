#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YOLO11 최신 모델 사물 인식 및 추적 프로그램
YOLO11 - 최신 Ultralytics 모델 사용
"""

import cv2
import numpy as np
import yt_dlp
import random
from ultralytics import YOLO
import threading
import queue
import time
import sys
import re
import os
from simple_text_utils import put_korean_text
from ui_design_improved import ImprovedUIDesign
from ai_object_analyzer import AIObjectAnalyzer

class YOLO11ObjectTracker:
    def __init__(self, model_size='n'):
        """YOLO11 최신 모델 사물 인식 및 추적 클래스"""
        
        # YOLO11 사용 가능한 모델들
        self.models = {
            'n': {'file': 'yolo11n.pt', 'name': 'YOLO11 Nano', 'accuracy': '39.5%', 'speed': '매우 빠름', 'params': '2.6M'},
            's': {'file': 'yolo11s.pt', 'name': 'YOLO11 Small', 'accuracy': '47.0%', 'speed': '빠름', 'params': '9.4M'},
            'm': {'file': 'yolo11m.pt', 'name': 'YOLO11 Medium', 'accuracy': '51.5%', 'speed': '보통', 'params': '20.1M'},
            'l': {'file': 'yolo11l.pt', 'name': 'YOLO11 Large', 'accuracy': '53.4%', 'speed': '느림', 'params': '25.3M'},
            'x': {'file': 'yolo11x.pt', 'name': 'YOLO11 Extra Large', 'accuracy': '54.7%', 'speed': '매우 느림', 'params': '56.9M'}
        }
        
        self.current_model = model_size
        model_info = self.models[model_size]
        
        print("🚀" + "="*60)
        print(f"🎯 YOLO11 최신 모델 로드 중...")
        print(f"   📦 모델: {model_info['name']} ({model_info['file']})")
        print(f"   🎯 정확도: {model_info['accuracy']} mAP")
        print(f"   ⚡ 속도: {model_info['speed']}")
        print(f"   📊 파라미터: {model_info['params']}")
        print("="*60)
        
        # YOLO11 모델 로드
        self.model = YOLO(model_info['file'])
        
        # YOLO11 최적화 설정
        if model_size == 'x':
            self.model.conf = 0.35   # Extra Large: 낮은 임계값으로 더 많은 검출
            self.model.iou = 0.25    # 더 관대한 NMS
        elif model_size == 'l':
            self.model.conf = 0.4
            self.model.iou = 0.3
        elif model_size == 'm':
            self.model.conf = 0.45
            self.model.iou = 0.35
        else:
            self.model.conf = 0.5
            self.model.iou = 0.4
        
        # 향상된 색상 팔레트 (YOLO11용 특별 색상)
        self.colors = {}
        self.color_palette = [
            (52, 152, 219),   # 파란색 (Primary)
            (46, 204, 113),   # 녹색 (Success)
            (231, 76, 60),    # 빨간색 (Danger)
            (241, 196, 15),   # 노란색 (Warning)
            (155, 89, 182),   # 보라색 (Info)
            (230, 126, 34),   # 주황색 (Accent)
            (26, 188, 156),   # 청록색 (Teal)
            (245, 183, 177),  # 분홍색 (Pink)
            (52, 73, 94),     # 어두운 회색 (Dark)
            (149, 165, 166),  # 밝은 회색 (Light)
            (192, 57, 43),    # 진한 빨간색
            (39, 174, 96),    # 진한 녹색
            (142, 68, 173),   # 진한 보라색
            (211, 84, 0),     # 진한 주황색
            (41, 128, 185),   # 진한 파란색
        ]
        
        # 고급 추적 설정 (YOLO11 최적화)
        self.tracked_objects = {}
        self.next_id = 1
        self.object_history = {}
        self.frame_buffer = []
        self.max_buffer_size = 5
        
        # YOLO11 최적화된 필터링 설정
        self.min_confidence = 0.25 if model_size in ['x', 'l'] else 0.4
        self.min_detection_size = 10 if model_size in ['x', 'l'] else 15
        self.max_detection_size = 0.95  # YOLO11은 더 큰 객체까지 정확하게 검출
        self.stable_frames_required = 3 if model_size in ['x', 'l', 'm'] else 2
        
        # 성능 모니터링
        self.fps_counter = 0
        self.fps_start_time = time.time()
        self.current_fps = 0
        self.total_detections = 0
        self.valid_detections = 0
          # UI 디자인 개선
        self.ui_design = ImprovedUIDesign()
        
        # AI 객체 상세 분석기 (선택적)
        try:
            self.ai_analyzer = AIObjectAnalyzer()
            self.use_ai_analysis = True
            print("🤖 AI 상세 분석 시스템 활성화")
        except Exception as e:
            self.ai_analyzer = None
            self.use_ai_analysis = False
            print(f"⚠️ AI 분석 시스템 비활성화: {e}")
        
        # AI 분석 설정
        self.ai_analysis_interval = 5  # 5프레임마다 AI 분석
        self.frame_count_for_ai = 0
        self.detailed_object_info = {}  # 상세 정보 캐시
        
        # YOLO11 최적화된 클래스별 임계값
        self.class_thresholds = {
            # 사람 및 동물 (높은 정확도 요구)
            'person': 0.6,
            'dog': 0.55,
            'cat': 0.55,
            'bird': 0.65,
            'horse': 0.5,
            'sheep': 0.5,
            'cow': 0.5,
            'elephant': 0.45,
            'bear': 0.55,
            'zebra': 0.5,
            'giraffe': 0.45,
            
            # 차량 (중간 정확도)
            'car': 0.4,
            'truck': 0.4,
            'bus': 0.4,
            'motorcycle': 0.5,
            'bicycle': 0.5,
            'train': 0.35,
            'boat': 0.45,
            'airplane': 0.35,
            
            # 생활용품 (다양한 정확도)
            'cell phone': 0.65,
            'laptop': 0.45,
            'tv': 0.3,
            'keyboard': 0.5,
            'mouse': 0.55,
            'remote': 0.6,
            'microwave': 0.4,
            'oven': 0.35,
            'refrigerator': 0.3,
            
            # 가구 (낮은 정확도)
            'chair': 0.35,
            'couch': 0.35,
            'bed': 0.3,
            'dining table': 0.3,
            'toilet': 0.4,
            
            # 음식 (높은 정확도 요구)
            'banana': 0.7,
            'apple': 0.7,
            'sandwich': 0.6,
            'orange': 0.65,
            'broccoli': 0.6,
            'carrot': 0.65,
            'pizza': 0.5,
            'donut': 0.6,
            'cake': 0.55,
            
            # 용기류 (중-높은 정확도)
            'bottle': 0.55,
            'cup': 0.6,
            'fork': 0.65,
            'knife': 0.65,
            'spoon': 0.65,
            'bowl': 0.55,
            'wine glass': 0.6,
            
            # 기타
            'book': 0.45,
            'clock': 0.5,
            'vase': 0.5,
            'scissors': 0.6,
            'teddy bear': 0.5,
            'hair drier': 0.55,
            'toothbrush': 0.65,
            'umbrella': 0.45,
            'handbag': 0.5,
            'tie': 0.55,
            'suitcase': 0.4,
            'frisbee': 0.55,
            'skis': 0.5,
            'snowboard': 0.5,
            'sports ball': 0.6,
            'kite': 0.5,
            'baseball bat': 0.5,
            'baseball glove': 0.55,
            'skateboard': 0.5,
            'surfboard': 0.45,
            'tennis racket': 0.5,
        }
        
        # 모델 크기별 임계값 조정
        if model_size in ['x', 'l']:
            # 큰 모델은 더 관대하게
            for key in self.class_thresholds:
                self.class_thresholds[key] = max(0.25, self.class_thresholds[key] - 0.15)
        elif model_size == 'm':
            # 중간 모델은 약간 관대하게
            for key in self.class_thresholds:
                self.class_thresholds[key] = max(0.3, self.class_thresholds[key] - 0.1)
        
        print(f"✅ YOLO11 {model_info['name']} 모델 로드 완료!")
        print(f"🎯 설정된 신뢰도 임계값: {self.model.conf}")
        print(f"📏 NMS IoU 임계값: {self.model.iou}")
        print("")
        
    def is_youtube_url(self, url):
        """YouTube URL인지 확인"""
        return ('youtube.com' in url or 'youtu.be' in url)
    
    def is_local_file(self, path):
        """로컬 파일인지 확인"""
        return os.path.isfile(path)
    
    def normalize_youtube_url(self, url):
        """YouTube URL을 표준 형식으로 변환"""
        if '/embed/' in url:
            video_id = re.search(r'/embed/([a-zA-Z0-9_-]+)', url)
            if video_id:
                return f"https://www.youtube.com/watch?v={video_id.group(1)}"
        
        if 'youtu.be/' in url:
            video_id = re.search(r'youtu\.be/([a-zA-Z0-9_-]+)', url)
            if video_id:
                return f"https://www.youtube.com/watch?v={video_id.group(1)}"
        
        return url
    
    def get_youtube_stream_url(self, youtube_url):
        """유튜브 URL에서 스트림 URL 추출 (YOLO11 최적화)"""
        normalized_url = self.normalize_youtube_url(youtube_url)
        print(f"🔗 정규화된 URL: {normalized_url}")
        
        # YOLO11 성능을 위한 최적 품질 선택
        format_options = [
            'best[height<=1080][height>=720]',  # 1080p-720p (최적 품질)
            'best[height<=720][height>=480]',   # 720p-480p
            'best[height<=480][height>=360]',   # 480p-360p
            'best[height<=360]',                # 360p 이하
            'worst[height>=240]',               # 240p 이상 최저품질
        ]
        
        for format_option in format_options:
            ydl_opts = {
                'format': format_option,
                'quiet': True,
                'no_warnings': True,
                'extractaudio': False,
                'ignoreerrors': True,
                'socket_timeout': 30,
                'retries': 2,
            }
            
            try:
                print(f"🎯 품질 옵션 시도: {format_option}")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(normalized_url, download=False)
                    
                    if info and 'url' in info:
                        print(f"✅ 스트림 URL 추출 성공 (품질: {format_option})")
                        return info['url']
                        
            except Exception as e:
                print(f"❌ 품질 {format_option} 시도 실패: {str(e)[:100]}")
                continue
        
        print("❌ 모든 품질 옵션에서 실패했습니다.")
        return None
    
    def get_video_source(self, source):
        """비디오 소스 결정"""
        if source.isdigit():
            return int(source), "webcam"
        elif self.is_local_file(source):
            return source, "local_file"
        elif self.is_youtube_url(source):
            stream_url = self.get_youtube_stream_url(source)
            return stream_url, "youtube"
        else:
            return source, "stream"
    
    def get_class_threshold(self, class_name):
        """클래스별 신뢰도 임계값 반환"""
        return self.class_thresholds.get(class_name, self.min_confidence)
    
    def is_valid_detection(self, box, confidence, class_name, frame_shape):
        """YOLO11 최적화된 검출 유효성 검사"""
        x1, y1, x2, y2 = box
        
        # 1. 클래스별 신뢰도 체크
        threshold = self.get_class_threshold(class_name)
        if confidence < threshold:
            return False, f"신뢰도 부족 ({confidence:.3f} < {threshold:.3f})"
        
        # 2. 크기 체크 (YOLO11은 더 정확한 크기 감지)
        width = x2 - x1
        height = y2 - y1
        
        # 최소 크기 체크
        if width < self.min_detection_size or height < self.min_detection_size:
            return False, f"크기가 너무 작음 ({width:.0f}x{height:.0f})"
        
        # 최대 크기 체크
        frame_height, frame_width = frame_shape[:2]
        width_ratio = width / frame_width
        height_ratio = height / frame_height
        
        if width_ratio > self.max_detection_size or height_ratio > self.max_detection_size:
            return False, f"크기가 너무 큼 ({width_ratio*100:.1f}%x{height_ratio*100:.1f}%)"
        
        # 3. 비율 체크 (YOLO11은 더 다양한 비율 지원)
        aspect_ratio = width / height
        if aspect_ratio > 10 or aspect_ratio < 0.05:  # 매우 관대한 비율
            return False, f"비정상적인 가로세로 비율 ({aspect_ratio:.2f})"
        
        # 4. 경계 체크
        if x1 < -5 or y1 < -5 or x2 > frame_width + 5 or y2 > frame_height + 5:
            return False, "화면 경계를 크게 벗어남"
        
        return True, "유효한 검출"
    
    def get_color_for_class(self, class_name):
        """클래스별 고유 색상 반환 (YOLO11 향상된 색상)"""
        if class_name not in self.colors:
            color_idx = len(self.colors) % len(self.color_palette)
            self.colors[class_name] = self.color_palette[color_idx]
        return self.colors[class_name]
    
    def calculate_distance(self, box1, box2):
        """두 바운딩 박스 간의 거리 계산 (개선된 알고리즘)"""
        # 중심점 거리
        center1 = ((box1[0] + box1[2]) / 2, (box1[1] + box1[3]) / 2)
        center2 = ((box2[0] + box2[2]) / 2, (box2[1] + box2[3]) / 2)
        center_distance = np.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)
        
        # 크기 차이도 고려
        area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
        area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
        area_ratio = min(area1, area2) / max(area1, area2) if max(area1, area2) > 0 else 0
        
        # 가중치 적용된 거리 (크기가 비슷할수록 가중치 증가)
        weighted_distance = center_distance * (2 - area_ratio)
        return weighted_distance

    def track_objects(self, detections):
        """YOLO11 최적화된 고급 객체 추적 로직"""
        if not self.tracked_objects:
            # 첫 번째 프레임: 모든 검출을 새 객체로 등록
            for detection in detections:
                new_obj = {
                    'box': detection['box'],
                    'class': detection['class'],
                    'confidence': detection['confidence'],
                    'color': self.get_color_for_class(detection['class']),
                    'stable_count': 1,
                    'history': [detection['box']],
                    'avg_confidence': detection['confidence'],
                    'total_frames': 1,
                }
                
                # AI 분석 데이터가 있으면 추가
                if 'ai_analysis' in detection:
                    new_obj['ai_analysis'] = detection['ai_analysis']
                if 'detailed_name' in detection:
                    new_obj['detailed_name'] = detection['detailed_name']
                
                self.tracked_objects[self.next_id] = new_obj
                self.next_id += 1
        else:
            matched = set()
            new_tracked = {}
            
            # 기존 객체와 새 검출 매칭
            for obj_id, tracked_obj in self.tracked_objects.items():
                best_match = None
                min_distance = float('inf')
                
                for i, detection in enumerate(detections):
                    if i in matched:
                        continue
                    
                    # 클래스가 같은 경우에만 매칭 고려
                    if detection['class'] == tracked_obj['class']:
                        distance = self.calculate_distance(tracked_obj['box'], detection['box'])
                        
                        # YOLO11 최적화된 매칭 거리 (모델 크기별 조정)
                        max_distance = 250 if self.current_model in ['x', 'l'] else 200 if self.current_model == 'm' else 150
                        
                        if distance < min_distance and distance < max_distance:
                            min_distance = distance
                            best_match = i

                if best_match is not None:
                    matched.add(best_match)
                    
                    # 히스토리 업데이트 (더 긴 히스토리 유지)
                    history = tracked_obj['history'][-9:]  # 최근 10개 위치 유지
                    history.append(detections[best_match]['box'])
                    
                    # 평균 신뢰도 계산
                    total_frames = tracked_obj['total_frames'] + 1
                    avg_confidence = (tracked_obj['avg_confidence'] * tracked_obj['total_frames'] + 
                                    detections[best_match]['confidence']) / total_frames
                    
                    # 기존 AI 분석 데이터 유지 또는 새 데이터 추가
                    updated_obj = {
                        'box': detections[best_match]['box'],
                        'class': detections[best_match]['class'],
                        'confidence': detections[best_match]['confidence'],
                        'color': tracked_obj['color'],
                        'stable_count': min(tracked_obj['stable_count'] + 1, 20),  # 더 높은 안정성 수준
                        'history': history,
                        'avg_confidence': avg_confidence,
                        'total_frames': total_frames,
                    }
                    
                    # AI 분석 데이터 전달 (기존 데이터 우선, 새 데이터로 업데이트)
                    if 'ai_analysis' in tracked_obj:
                        updated_obj['ai_analysis'] = tracked_obj['ai_analysis']
                    if 'detailed_name' in tracked_obj:
                        updated_obj['detailed_name'] = tracked_obj['detailed_name']
                        
                    # 새로운 AI 분석 데이터가 있으면 업데이트
                    if 'ai_analysis' in detections[best_match]:
                        updated_obj['ai_analysis'] = detections[best_match]['ai_analysis']
                    if 'detailed_name' in detections[best_match]:
                        updated_obj['detailed_name'] = detections[best_match]['detailed_name']
                    
                    new_tracked[obj_id] = updated_obj

            # 새로운 검출 추가 (YOLO11 최적화된 기준)
            for i, detection in enumerate(detections):
                if i not in matched:
                    threshold = self.get_class_threshold(detection['class'])
                    
                    # 모델 크기별 보너스 조정
                    if self.current_model in ['x', 'l']:
                        bonus = 0.02  # 큰 모델은 매우 관대하게
                    elif self.current_model == 'm':
                        bonus = 0.05  # 중간 모델은 조금 관대하게
                    else:
                        bonus = 0.1   # 작은 모델은 더 엄격하게
                    
                    if detection['confidence'] > threshold + bonus:
                        new_obj = {
                            'box': detection['box'],
                            'class': detection['class'],
                            'confidence': detection['confidence'],
                            'color': self.get_color_for_class(detection['class']),
                            'stable_count': 1,
                            'history': [detection['box']],
                            'avg_confidence': detection['confidence'],
                            'total_frames': 1,
                        }
                        
                        # AI 분석 데이터가 있으면 새 객체에 추가
                        if 'ai_analysis' in detection:
                            new_obj['ai_analysis'] = detection['ai_analysis']
                        if 'detailed_name' in detection:
                            new_obj['detailed_name'] = detection['detailed_name']
                            
                        new_tracked[self.next_id] = new_obj
                        self.next_id += 1
            
            self.tracked_objects = new_tracked
    
    def draw_enhanced_overlay(self, frame, obj_id, obj_data):
        """YOLO11 최적화된 향상된 오버레이 그리기 - AI 상세 정보 포함"""
        # 개선된 UI 디자인 사용 (YOLO11 + AI 분석 정보 포함)
        enhanced_obj_data = obj_data.copy()
        enhanced_obj_data['model_name'] = f"YOLO11-{self.current_model.upper()}"
        enhanced_obj_data['avg_confidence'] = obj_data.get('avg_confidence', obj_data['confidence'])
        enhanced_obj_data['total_frames'] = obj_data.get('total_frames', 1)
        
        # AI 분석 정보 추가 (있는 경우)
        if 'ai_analysis' in obj_data:
            enhanced_obj_data['ai_analysis'] = obj_data['ai_analysis']
        if 'detailed_name' in obj_data:
            enhanced_obj_data['detailed_name'] = obj_data['detailed_name']
        
        self.ui_design.draw_modern_info_card(frame, obj_id, enhanced_obj_data)
    
    def process_frame_yolo11(self, frame):
        """YOLO11 최적화된 프레임 처리"""
        original_frame = frame.copy()
        
        # YOLO11 최적화된 전처리
        # 1. 적응적 노이즈 제거 (모델 크기별 조정)
        if self.current_model in ['x', 'l']:
            # 큰 모델은 더 강한 전처리
            frame_enhanced = cv2.bilateralFilter(frame, 13, 90, 90)
        elif self.current_model == 'm':
            frame_enhanced = cv2.bilateralFilter(frame, 11, 80, 80)
        else:
            # 작은 모델은 가벼운 전처리
            frame_enhanced = cv2.bilateralFilter(frame, 9, 70, 70)
        
        # 2. 대비 향상 (YOLO11 최적화)
        alpha = 1.1 if self.current_model in ['n', 's'] else 1.05  # 작은 모델일수록 더 강한 대비
        beta = 5 if self.current_model in ['x', 'l'] else 10
        frame_enhanced = cv2.convertScaleAbs(frame_enhanced, alpha=alpha, beta=beta)
        
        # 3. 선택적 선명도 향상 (큰 모델에만 적용)
        if self.current_model in ['l', 'x']:
            kernel = np.array([[-0.5,-0.5,-0.5], [-0.5,5,-0.5], [-0.5,-0.5,-0.5]])
            frame_enhanced = cv2.filter2D(frame_enhanced, -1, kernel)
        
        # YOLO11 객체 검출 (최적화된 설정)
        # 이미지 크기 조정 (모델별 최적화)
        imgsz = 1280 if self.current_model in ['l', 'x'] else 640
        
        results = self.model(frame_enhanced, verbose=False, imgsz=imgsz, 
                           augment=True if self.current_model in ['m', 'l', 'x'] else False)
        
        valid_detections = []
        invalid_count = 0
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    self.total_detections += 1
                    
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = box.conf[0].cpu().numpy()
                    class_id = int(box.cls[0].cpu().numpy())
                    class_name = self.model.names[class_id]
                      # YOLO11 최적화된 유효성 검사
                    is_valid, reason = self.is_valid_detection(
                        [x1, y1, x2, y2], confidence, class_name, frame.shape)
                    
                    if is_valid:
                        self.valid_detections += 1
                        detection_data = {
                            'box': [x1, y1, x2, y2],
                            'class': class_name,
                            'confidence': confidence
                        }
                        
                        # AI 상세 분석 (선택적, 간헐적)
                        if (self.use_ai_analysis and 
                            self.frame_count_for_ai % self.ai_analysis_interval == 0 and
                            confidence > 0.7):  # 고신뢰도 객체만 분석
                            
                            try:
                                ai_analysis = self.ai_analyzer.analyze_object_detailed(
                                    frame, [x1, y1, x2, y2], class_name, confidence
                                )
                                if ai_analysis:
                                    # 상세 정보를 객체 데이터에 추가
                                    detection_data['ai_analysis'] = ai_analysis
                                    detection_data['detailed_name'] = self.ai_analyzer.get_detailed_object_name(
                                        ai_analysis, class_name
                                    )
                            except Exception as e:
                                print(f"⚠️ AI 분석 오류: {e}")
                        
                        valid_detections.append(detection_data)
                    else:
                        invalid_count += 1
        
        self.frame_count_for_ai += 1
        
        # YOLO11 최적화된 객체 추적
        self.track_objects(valid_detections)
        
        # 안정적인 객체만 표시
        stable_objects = {obj_id: obj_data for obj_id, obj_data in self.tracked_objects.items() 
                         if obj_data['stable_count'] >= self.stable_frames_required}
        
        # YOLO11 최적화된 오버레이 그리기
        for obj_id, obj_data in stable_objects.items():
            self.draw_enhanced_overlay(original_frame, obj_id, obj_data)
        
        return original_frame
    
    def draw_yolo11_info_panel(self, frame, source_type):
        """YOLO11 특화된 정보 패널 그리기"""
        # 트래커 정보 수집
        stable_objects = sum(1 for obj in self.tracked_objects.values() 
                           if obj['stable_count'] >= self.stable_frames_required)
        accuracy = (self.valid_detections / max(self.total_detections, 1)) * 100
        
        # 평균 신뢰도 계산
        avg_confidence = np.mean([obj.get('avg_confidence', obj['confidence']) 
                                for obj in self.tracked_objects.values()]) if self.tracked_objects else 0
        
        model_info = self.models[self.current_model]
        tracker_info = {
            'model_name': f'🚀 {model_info["name"]}',
            'fps': self.current_fps,
            'object_count': len(self.tracked_objects),
            'accuracy': accuracy,
            'stable_objects': stable_objects,
            'avg_confidence': avg_confidence,
            'model_params': model_info['params'],
        }
        
        # 개선된 UI 디자인 사용
        return self.ui_design.draw_modern_info_panel(frame, tracker_info)
    
    def calculate_fps(self):
        """FPS 계산 (더 정확한 계산)"""
        self.fps_counter += 1
        if self.fps_counter % 30 == 0:  # 30프레임마다 계산
            end_time = time.time()
            elapsed_time = end_time - self.fps_start_time
            self.current_fps = 30 / elapsed_time if elapsed_time > 0 else 0
            self.fps_start_time = end_time
    
    def change_model(self, new_size):
        """실시간 YOLO11 모델 변경"""
        if new_size in self.models:
            old_model = self.current_model
            try:
                model_info = self.models[new_size]
                print(f"🔄 YOLO11 모델 변경 중...")
                print(f"   이전: {self.models[old_model]['name']}")
                print(f"   새로운: {model_info['name']} ({model_info['accuracy']}, {model_info['params']})")
                
                self.current_model = new_size
                self.model = YOLO(model_info['file'])
                
                # 모델별 최적화 설정 적용
                if new_size == 'x':
                    self.model.conf = 0.35
                    self.model.iou = 0.25
                elif new_size == 'l':
                    self.model.conf = 0.4
                    self.model.iou = 0.3
                elif new_size == 'm':
                    self.model.conf = 0.45
                    self.model.iou = 0.35
                else:
                    self.model.conf = 0.5
                    self.model.iou = 0.4
                
                print(f"✅ YOLO11 모델 변경 완료!")
                print(f"🎯 새로운 설정 - 신뢰도: {self.model.conf}, NMS: {self.model.iou}")
                return True
                
            except Exception as e:
                print(f"❌ YOLO11 모델 변경 실패: {e}")
                self.current_model = old_model
                return False
        return False
    
    def run(self, source):
        """YOLO11 메인 실행 함수"""
        print("🚀" + "="*60)
        print(f"🎯 YOLO11 최신 모델로 비디오 처리 시작: {source}")
        print("="*60)
        
        video_source, source_type = self.get_video_source(source)
        
        if video_source is None:
            print("❌ 비디오 소스를 처리할 수 없습니다.")
            return
        
        print(f"✅ 소스 타입: {source_type}")
        print("📹 동영상 스트림을 여는 중...")
        
        # OpenCV VideoCapture 설정
        cap = cv2.VideoCapture()
        
        if source_type == "youtube" and video_source:
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            success = cap.open(video_source)
        else:
            success = cap.open(video_source)
        
        if not success:
            print("❌ 동영상을 열 수 없습니다.")
            return
        
        model_info = self.models[self.current_model]
        print("🎯 YOLO11 최신 사물 인식을 시작합니다!")
        print(f"🚀 사용 모델: {model_info['name']}")
        print(f"📊 정확도: {model_info['accuracy']} mAP")
        print(f"⚡ 성능: {model_info['speed']}")
        print(f"🔧 파라미터: {model_info['params']}")
        print("")
        print("🎮 YOLO11 고급 조작법:")
        print("  q: 종료")
        print("  s: 고해상도 스크린샷")
        print("  r: 통계 리셋")
        print("  m: YOLO11 모델 변경 (n→s→m→l→x 순환)")
        print("  i: 실시간 정보 표시 토글")
        print("")
        
        # 윈도우 설정
        window_name = f'🚀 YOLO11 {model_info["name"]} - {source_type.title()}'
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 1600, 1000)
        
        show_info = True
        frame_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("프레임을 읽을 수 없습니다.")
                    break
                
                # YOLO11 최적화된 프레임 크기 조정
                if self.current_model in ['x', 'l']:
                    # 큰 모델은 고해상도 유지
                    if frame.shape[1] > 1920:
                        frame = cv2.resize(frame, (1920, 1080))
                    elif frame.shape[1] < 1280:
                        frame = cv2.resize(frame, (1280, 720))
                elif self.current_model == 'm':
                    # 중간 모델은 적정 해상도
                    if frame.shape[1] > 1280:
                        frame = cv2.resize(frame, (1280, 720))
                    elif frame.shape[1] < 960:
                        frame = cv2.resize(frame, (960, 540))
                else:
                    # 작은 모델은 낮은 해상도로 빠른 처리
                    if frame.shape[1] > 960:
                        frame = cv2.resize(frame, (960, 540))
                    elif frame.shape[1] < 640:
                        frame = cv2.resize(frame, (640, 480))
                
                # YOLO11 최적화된 객체 인식 및 추적
                processed_frame = self.process_frame_yolo11(frame)
                
                # 정보 패널 추가 (토글 가능)
                if show_info:
                    final_frame = self.draw_yolo11_info_panel(processed_frame, source_type)
                else:
                    final_frame = processed_frame
                
                # FPS 계산
                self.calculate_fps()
                
                # 프레임 표시
                cv2.imshow(window_name, final_frame)
                
                # 키 입력 처리
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    timestamp = int(time.time())
                    screenshot_name = f'yolo11_{self.current_model}_{source_type}_{timestamp}.jpg'
                    cv2.imwrite(screenshot_name, final_frame)
                    print(f"📸 YOLO11 고해상도 스크린샷 저장: {screenshot_name}")
                elif key == ord('r'):
                    # 통계 리셋
                    self.total_detections = 0
                    self.valid_detections = 0
                    self.tracked_objects = {}
                    self.next_id = 1
                    print("🔄 YOLO11 통계가 리셋되었습니다.")
                elif key == ord('m'):
                    # YOLO11 모델 변경 (순환)
                    models = ['n', 's', 'm', 'l', 'x']
                    current_idx = models.index(self.current_model)
                    next_idx = (current_idx + 1) % len(models)
                    
                    if self.change_model(models[next_idx]):
                        # 윈도우 제목 업데이트
                        new_model_info = self.models[self.current_model]
                        window_name = f'🚀 YOLO11 {new_model_info["name"]} - {source_type.title()}'
                        cv2.setWindowTitle(window_name, window_name)
                elif key == ord('i'):
                    # 정보 표시 토글
                    show_info = not show_info
                    print(f"ℹ️ 정보 패널: {'표시' if show_info else '숨김'}")
                
                frame_count += 1
                
        except KeyboardInterrupt:
            print("🔚 사용자에 의해 중단되었습니다.")
        
        finally:
            cap.release()
            cv2.destroyAllWindows()
            
            # YOLO11 최종 통계 출력
            if self.total_detections > 0:
                final_accuracy = (self.valid_detections / self.total_detections) * 100
                model_info = self.models[self.current_model]
                
                print("🚀" + "="*60)
                print(f"📊 YOLO11 최종 성능 통계")
                print("="*60)
                print(f"🎯 사용 모델: {model_info['name']}")
                print(f"📈 모델 mAP: {model_info['accuracy']}")
                print(f"🔢 파라미터 수: {model_info['params']}")
                print(f"📊 전체 검출: {self.total_detections:,}")
                print(f"✅ 유효 검출: {self.valid_detections:,}")
                print(f"🎯 검출 정확도: {final_accuracy:.2f}%")
                print(f"🚀 평균 FPS: {self.current_fps:.1f}")
                print(f"📹 처리 프레임: {frame_count:,}")
                print("="*60)
            
            print("🚀 YOLO11 최신 모델 프로그램이 종료되었습니다.")

def main():
    """메인 함수"""
    print("🚀" + "="*60)
    print("🎯 YOLO11 최신 사물 인식 시스템")
    print("="*60)
    
    if len(sys.argv) < 2:
        print("📖 YOLO11 사용법:")
        print("  python yolo11_tracker.py <video_source> [model_size]")
        print("")
        print("📺 지원하는 소스:")
        print("  • YouTube URL: https://www.youtube.com/watch?v=VIDEO_ID")
        print("  • 로컬 파일: C:/path/to/video.mp4")
        print("  • 웹캠: 0 (기본 웹캠)")
        print("")
        print("🚀 YOLO11 모델 크기 옵션:")
        print("  • n: Nano (39.5% mAP, 2.6M params, 매우 빠름)")
        print("  • s: Small (47.0% mAP, 9.4M params, 빠름)")
        print("  • m: Medium (51.5% mAP, 20.1M params, 보통) ⭐ 기본값")
        print("  • l: Large (53.4% mAP, 25.3M params, 느림)")
        print("  • x: Extra Large (54.7% mAP, 56.9M params, 매우 느림) 🏆 최고 정확도")
        print("")
        print("💡 YOLO11 예시:")
        print("  python yolo11_tracker.py 0          # 웹캠, Medium 모델")
        print("  python yolo11_tracker.py 0 x        # 웹캠, Extra Large 모델")
        print("  python yolo11_tracker.py youtube_url l  # YouTube, Large 모델")
        print("")
        print("🚀 YOLO11의 새로운 특징:")
        print("  • 향상된 정확도와 속도")
        print("  • 더 정교한 객체 감지")
        print("  • 최적화된 모델 아키텍처")
        print("  • 향상된 실시간 성능")
        print("="*60)
        return
    
    source = sys.argv[1]
    model_size = sys.argv[2] if len(sys.argv) > 2 else 'n'  # 기본값: Medium
    
    if model_size not in ['n', 's', 'm', 'l', 'x']:
        print(f"❌ 잘못된 YOLO11 모델 크기: {model_size}")
        print("🚀 사용 가능한 크기: n, s, m, l, x")
        return
    
    # YOLO11 추적기 생성 및 실행
    tracker = YOLO11ObjectTracker(model_size)
    tracker.run(source)

if __name__ == "__main__":
    main()
