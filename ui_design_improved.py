import cv2
import numpy as np
from simple_text_utils import put_korean_text
import math
import time
from PIL import Image, ImageDraw, ImageFont
import os

class ImprovedUIDesign:
    """개선된 UI 디자인 클래스 - 전문적이고 또렷한 폰트 시스템"""
    
    def __init__(self):
        # 고품질 폰트 시스템 초기화
        self.init_professional_fonts()
          # 색상 팔레트 (모던하고 시각적으로 매력적인 색상들)
        self.color_palette = {
            'primary': (52, 152, 219),      # 파란색
            'success': (46, 204, 113),      # 녹색
            'warning': (241, 196, 15),      # 노란색
            'danger': (231, 76, 60),        # 빨간색
            'info': (155, 89, 182),         # 보라색
            'dark': (52, 73, 94),           # 어두운 회색
            'light': (236, 240, 241),       # 밝은 회색
            'accent': (230, 126, 34),       # 주황색
            'teal': (26, 188, 156),         # 청록색
            'pink': (245, 183, 177),        # 분홍색
            'copilot': (100, 255, 255)      # GitHub Copilot 전용 색상
        }
          # 객체별 색상 매핑
        self.class_colors = {
            'person': self.color_palette['primary'],
            'car': self.color_palette['success'],
            'truck': self.color_palette['danger'],
            'bus': self.color_palette['warning'],
            'bicycle': self.color_palette['info'],
            'motorcycle': self.color_palette['accent'],
            'dog': self.color_palette['teal'],
            'cat': self.color_palette['pink'],
            'bird': self.color_palette['light'],
            'cell phone': self.color_palette['copilot'],  # 스마트폰은 Copilot 색상
            'laptop': self.color_palette['copilot']       # 노트북도 Copilot 색상
        }
        
        self.animation_time = time.time()
        self.pulse_factor = 0
    
    def init_professional_fonts(self):
        """전문적인 폰트 시스템 초기화"""
        self.fonts = {}
        self.use_pil_fonts = True
        
        # Windows 시스템 폰트 경로
        font_paths = [
            "C:/Windows/Fonts/",
            "C:/Windows/Fonts/segoeui.ttf",  # Segoe UI
            "C:/Windows/Fonts/calibri.ttf",   # Calibri
            "C:/Windows/Fonts/arial.ttf",     # Arial
            "C:/Windows/Fonts/tahoma.ttf",    # Tahoma
        ]
        
        # 폰트 크기별 로드
        font_sizes = {
            'tiny': 10,      # 매우 작은 텍스트
            'small': 12,     # 작은 텍스트
            'normal': 14,    # 일반 텍스트
            'medium': 16,    # 중간 텍스트
            'large': 18,     # 큰 텍스트
            'xlarge': 22,    # 매우 큰 텍스트
            'title': 24      # 제목
        }
        
        try:
            # 가장 선명한 폰트 우선순위로 로드
            preferred_fonts = [
                "C:/Windows/Fonts/calibri.ttf",   # 가장 선명하고 모던
                "C:/Windows/Fonts/segoeui.ttf",   # Windows 기본
                "C:/Windows/Fonts/tahoma.ttf",    # 작은 크기에 최적화
                "C:/Windows/Fonts/arial.ttf",     # 범용성
            ]
            
            best_font = None
            for font_path in preferred_fonts:
                if os.path.exists(font_path):
                    best_font = font_path
                    break
            
            if best_font:
                for size_name, size in font_sizes.items():
                    try:
                        self.fonts[size_name] = ImageFont.truetype(best_font, size)
                    except:
                        self.fonts[size_name] = ImageFont.load_default()
                print(f"✅ 고품질 폰트 로드 완료: {os.path.basename(best_font)}")
            else:
                # 폴백: 기본 폰트
                for size_name, size in font_sizes.items():
                    self.fonts[size_name] = ImageFont.load_default()
                print("⚠️ 시스템 폰트를 찾을 수 없어 기본 폰트를 사용합니다")
                
        except Exception as e:
            print(f"⚠️ 폰트 로드 실패, OpenCV 폰트 사용: {e}")
            self.use_pil_fonts = False
    
    def draw_professional_text(self, frame, text, position, size='normal', 
                             color=(255, 255, 255), background=None, 
                             bold=False, shadow=True):
        """전문적이고 또렷한 텍스트 렌더링"""
        if not self.use_pil_fonts or size not in self.fonts:
            # 폴백: OpenCV 기본 폰트 (최적화)
            return self._draw_opencv_text(frame, text, position, size, color, background, shadow)
        
        try:
            # PIL을 사용한 고품질 텍스트 렌더링
            frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(frame_pil)
            
            font = self.fonts[size]
            x, y = position
            
            # 텍스트 색상 변환 (BGR → RGB)
            text_color = (color[2], color[1], color[0])
            
            # 그림자 효과 (더 미묘하게)
            if shadow:
                shadow_offset = 1 if size in ['tiny', 'small'] else 2
                shadow_color = (30, 30, 30)  # 어두운 그림자
                draw.text((x + shadow_offset, y + shadow_offset), text, 
                         font=font, fill=shadow_color)
            
            # 배경 (선택사항)
            if background:
                bbox = draw.textbbox((x, y), text, font=font)
                padding = 3
                bg_color = (background[2], background[1], background[0])  # BGR → RGB
                draw.rectangle([bbox[0]-padding, bbox[1]-padding, 
                              bbox[2]+padding, bbox[3]+padding], fill=bg_color)
            
            # 메인 텍스트
            draw.text((x, y), text, font=font, fill=text_color)
            
            # PIL → OpenCV 변환
            frame[:] = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)
            
            return frame
            
        except Exception as e:
            # 에러 시 OpenCV 폴백
            return self._draw_opencv_text(frame, text, position, size, color, background, shadow)
    
    def _draw_opencv_text(self, frame, text, position, size, color, background, shadow):
        """OpenCV 기본 폰트 최적화 버전"""
        # 크기별 설정 (더 작고 선명하게)
        size_settings = {
            'tiny': (cv2.FONT_HERSHEY_SIMPLEX, 0.35, 1),
            'small': (cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1), 
            'normal': (cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1),
            'medium': (cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1),
            'large': (cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2),
            'xlarge': (cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2),
            'title': (cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
        }
        
        font_face, font_scale, thickness = size_settings.get(size, size_settings['normal'])
        x, y = position
        
        # 배경
        if background:
            (text_w, text_h), baseline = cv2.getTextSize(text, font_face, font_scale, thickness)
            cv2.rectangle(frame, (x-2, y-text_h-2), (x+text_w+2, y+baseline+2), background, -1)
        
        # 그림자 (더 미묘하게)
        if shadow:
            cv2.putText(frame, text, (x+1, y+1), font_face, font_scale, (30, 30, 30), thickness)
        
        # 메인 텍스트
        cv2.putText(frame, text, (x, y), font_face, font_scale, color, thickness)
        
        return frame
    
    def get_class_color(self, class_name):
        """클래스별 색상 반환"""
        return self.class_colors.get(class_name, self.color_palette['dark'])
    
    def draw_rounded_rectangle(self, frame, pt1, pt2, color, thickness=2, radius=8):
        """둥근 모서리 사각형 그리기"""
        x1, y1 = pt1
        x2, y2 = pt2
        
        # 직선 부분
        cv2.rectangle(frame, (x1 + radius, y1), (x2 - radius, y2), color, thickness)
        cv2.rectangle(frame, (x1, y1 + radius), (x2, y2 - radius), color, thickness)
        
        # 모서리 원호        cv2.ellipse(frame, (x1 + radius, y1 + radius), (radius, radius), 180, 0, 90, color, thickness)
        cv2.ellipse(frame, (x2 - radius, y1 + radius), (radius, radius), 270, 0, 90, color, thickness)
        cv2.ellipse(frame, (x1 + radius, y2 - radius), (radius, radius), 90, 0, 90, color, thickness)
        cv2.ellipse(frame, (x2 - radius, y2 - radius), (radius, radius), 0, 0, 90, color, thickness)
    
    def draw_icon(self, frame, icon_type, position, size=20, color=(255, 255, 255)):
        """작고 선명한 아이콘 그리기"""
        x, y = position
        
        if icon_type == "tracking":
            # 추적 아이콘 (타겟 모양) - 더 작고 선명하게
            center = (x + size//2, y + size//2)
            # 외부 원
            cv2.circle(frame, center, size//2, color, 1)
            # 내부 원
            cv2.circle(frame, center, size//4, color, 1)
            # 십자선 (더 짧게)
            offset = size//3
            cv2.line(frame, (center[0], center[1] - offset), 
                    (center[0], center[1] - size//5), color, 1)
            cv2.line(frame, (center[0], center[1] + size//5), 
                    (center[0], center[1] + offset), color, 1)
            cv2.line(frame, (center[0] - offset, center[1]), 
                    (center[0] - size//5, center[1]), color, 1)
            cv2.line(frame, (center[0] + size//5, center[1]), 
                    (center[0] + offset, center[1]), color, 1)
        
        elif icon_type == "ai":
            # AI 아이콘 (GitHub Copilot용 특별 아이콘)
            center = (x + size//2, y + size//2)
            # 외부 육각형 (AI 느낌)
            points = []
            for i in range(6):
                angle = i * 60 * np.pi / 180
                px = int(center[0] + (size//2) * np.cos(angle))
                py = int(center[1] + (size//2) * np.sin(angle))
                points.append([px, py])
            cv2.polylines(frame, [np.array(points, np.int32)], True, color, 1)
            
            # 내부 점들 (신경망 느낌)
            cv2.circle(frame, center, 2, color, -1)
            cv2.circle(frame, (center[0]-3, center[1]-3), 1, color, -1)
            cv2.circle(frame, (center[0]+3, center[1]-3), 1, color, -1)
            cv2.circle(frame, (center[0], center[1]+4), 1, color, -1)
    
    def draw_modern_info_card(self, frame, obj_id, obj_data):
        """모던한 정보 카드 그리기 - 전문적이고 간결한 디자인 + AI 분석 정보"""
        x1, y1, x2, y2 = map(int, obj_data['box'])
        color = self.get_class_color(obj_data['class'])
        label = obj_data['class']
        confidence = obj_data['confidence']
        stable_count = obj_data.get('stable_count', 1)
        
        # AI 분석 정보 확인
        ai_analysis = obj_data.get('ai_analysis')
        detailed_name = obj_data.get('detailed_name', label)
        
        # 펄스 애니메이션 효과 (더 미묘하게)
        self.pulse_factor = (math.sin(time.time() * 2) + 1) / 2 * 0.05
          # 안정성에 따른 시각적 효과
        alpha = min(0.15 + (stable_count * 0.01) + self.pulse_factor, 0.4)
        thickness = max(1, min(stable_count // 2, 3))
        
        # GitHub Copilot 분석이 있으면 특별한 테두리
        has_copilot_analysis = ai_analysis and ai_analysis.get('provider') == 'GitHub Copilot'
        if has_copilot_analysis:
            # 이중 테두리로 GitHub Copilot 강조
            cv2.rectangle(frame, (x1-2, y1-2), (x2+2, y2+2), self.color_palette['copilot'], 1)
            self.draw_rounded_rectangle(frame, (x1, y1), (x2, y2), color, thickness, radius=6)
        else:
            # 일반 테두리
            self.draw_rounded_rectangle(frame, (x1, y1), (x2, y2), color, thickness, radius=6)
        
        # 매우 미묘한 배경
        overlay = frame.copy()
        cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)
        cv2.addWeighted(frame, 1-alpha, overlay, alpha, 0, frame)
        
        # GitHub Copilot 분석에 따른 동적 카드 크기 조정
        has_copilot_analysis = ai_analysis and ai_analysis.get('provider') == 'GitHub Copilot'
        
        # GitHub Copilot 분석이 있으면 카드를 더 크게 만들어 상세 정보 표시
        if has_copilot_analysis:
            card_width = 200  # GitHub Copilot 상세 정보용
            card_height = 75
        elif ai_analysis:
            card_width = 180  # 일반 AI 분석용
            card_height = 65
        else:
            card_width = 160  # 기본 크기
            card_height = 55
          # 카드 위치 (객체 위쪽에 표시, 화면 경계 고려)
        card_x = min(x1, frame.shape[1] - card_width)
        card_y = max(card_height + 5, y1 - 5)
        
        # GitHub Copilot 분석에 따른 특별한 카드 배경
        if has_copilot_analysis:
            self._draw_compact_card_background(frame, card_x, card_y, card_width, card_height, 
                                             self.color_palette['copilot'])
        else:
            self._draw_compact_card_background(frame, card_x, card_y, card_width, card_height, color)
        
        # 객체 정보 표시 (AI 분석 정보 포함)
        self._draw_compact_card_content_with_ai(frame, card_x, card_y, card_width, card_height, 
                                              obj_id, detailed_name, confidence, stable_count, 
                                              color, ai_analysis)
          # 더 작은 중심점 표시 (GitHub Copilot은 특별한 색상)
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        pulse_radius = int(3 + self.pulse_factor * 2)
        
        if has_copilot_analysis:
            cv2.circle(frame, (center_x, center_y), pulse_radius, self.color_palette['copilot'], -1)
            cv2.circle(frame, (center_x, center_y), pulse_radius + 1, (255, 255, 255), 1)
        else:
            cv2.circle(frame, (center_x, center_y), pulse_radius, color, -1)
            cv2.circle(frame, (center_x, center_y), pulse_radius + 1, (255, 255, 255), 1)
        
        # 더 작은 ID 텍스트
        self.draw_professional_text(frame, str(obj_id), (center_x-4, center_y-6), 
                                   'tiny', (255, 255, 255), shadow=True)
    
    def _draw_compact_card_background(self, frame, card_x, card_y, card_width, card_height, color):
        """컴팩트한 카드 배경 그리기"""
        # 더 미묘한 그라데이션
        color_dark = tuple(int(c * 0.2) for c in color)
        color_light = tuple(int(c * 0.5) for c in color)
        
        overlay = frame.copy()
        
        # 그라데이션 효과
        for i in range(card_height):
            ratio = i / card_height
            b = int(color_dark[0] * (1 - ratio) + color_light[0] * ratio)
            g = int(color_dark[1] * (1 - ratio) + color_light[1] * ratio)
            r = int(color_dark[2] * (1 - ratio) + color_light[2] * ratio)
            
            cv2.line(overlay, 
                    (card_x, card_y - card_height + i), 
                    (card_x + card_width, card_y - card_height + i), 
                    (b, g, r), 1)
          # 반투명 적용
        cv2.addWeighted(frame, 0.25, overlay, 0.75, 0, frame)
        
        # 더 얇은 테두리
        self.draw_rounded_rectangle(frame, 
                                  (card_x, card_y - card_height), 
                                  (card_x + card_width, card_y),
                                  color, 1, radius=6)
    
    def _draw_compact_card_content_with_ai(self, frame, card_x, card_y, card_width, card_height,
                                         obj_id, detailed_name, confidence, stable_count, 
                                         color, ai_analysis):
        """AI 분석 정보를 포함한 컴팩트한 카드 내용 그리기 - GitHub Copilot 강화"""
        # AI 상태에 따른 아이콘 변경
        icon_x = card_x + 4
        icon_y = card_y - card_height + 4
        
        # GitHub Copilot 분석 시 특별한 아이콘
        if ai_analysis and ai_analysis.get('provider') == 'GitHub Copilot':
            self.draw_icon(frame, "ai", (icon_x, icon_y), size=12, color=(100, 255, 255))  # 청록색 AI 아이콘
        else:
            self.draw_icon(frame, "tracking", (icon_x, icon_y), size=12, color=(255, 255, 255))
        
        # 텍스트 영역 (더 촘촘하게)
        text_x = icon_x + 18
        text_y = icon_y + 8
        
        # GitHub Copilot 상세 분석 결과 우선 표시
        display_name = detailed_name
        if ai_analysis and ai_analysis.get('provider') == 'GitHub Copilot':
            # GitHub Copilot 분석일 때 브랜드+모델 강조
            brand = ai_analysis.get('brand', 'Unknown')
            model = ai_analysis.get('model', 'Unknown')
            if brand != 'Unknown' and model != 'Unknown':
                display_name = f"{brand} {model}"
        
        label_text = f"{display_name} #{obj_id}"
        
        # 더 작은 폰트 사용 (긴 이름 대응)
        font_size = 'tiny' if len(display_name) > 15 else 'small'
        self.draw_professional_text(frame, label_text, (text_x, text_y), 
                                   font_size, (255, 255, 255), shadow=True)
        
        # 신뢰도와 AI 분석 상태
        confidence_text = f"{confidence:.2f}"
        confidence_color = (100, 255, 100) if confidence > 0.7 else (255, 255, 100) if confidence > 0.5 else (255, 200, 100)
        self.draw_professional_text(frame, confidence_text, (text_x, text_y + 12), 
                                   'tiny', confidence_color, shadow=True)
        
        # GitHub Copilot 상세 분석 정보 표시
        if ai_analysis:
            ai_confidence = ai_analysis.get('confidence', 0)
            provider = ai_analysis.get('provider', 'AI')
            
            # GitHub Copilot 특별 표시
            if provider == 'GitHub Copilot':
                ai_text = f"🤖Copilot {ai_confidence:.1f}"
                ai_color = (100, 255, 255)  # 청록색으로 강조
            else:
                ai_text = f"🤖{provider[:4]} {ai_confidence:.1f}"
                ai_color = (255, 255, 100)  # 일반 AI는 노란색
                
            self.draw_professional_text(frame, ai_text, (text_x + 35, text_y + 12), 
                                       'tiny', ai_color, shadow=True)
        
        # GitHub Copilot 추가 분석 정보 (브랜드, 색상, 상태)
        ai_info_y = text_y + 24
        if ai_analysis:
            info_parts = []
            
            # 색상 정보
            if ai_analysis.get('color') and ai_analysis['color'] != 'Unknown':
                info_parts.append(ai_analysis['color'][:8])
            
            # 상태 정보 (GitHub Copilot만)
            if ai_analysis.get('provider') == 'GitHub Copilot' and ai_analysis.get('condition'):
                condition = ai_analysis['condition'][:6]  # 상태 정보 줄임
                info_parts.append(f"[{condition}]")
            
            # 정보 표시
            if info_parts:
                info_text = " ".join(info_parts)
                self.draw_professional_text(frame, info_text, (text_x, ai_info_y), 
                                           'tiny', (255, 255, 150), shadow=True)
        
        # 안정성 정보
        if stable_count >= 3:
            stability_text = f"S:{stable_count}"
            stability_x = text_x + 80  # 위치 조정
            self.draw_professional_text(frame, stability_text, (stability_x, ai_info_y), 
                                       'tiny', (100, 255, 100), shadow=True)
        
        # 더 작은 진행 바
        bar_x = text_x + 75
        bar_y = text_y + 14
        bar_width = 40
        bar_height = 3
        
        # 배경 바
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), 
                     (60, 60, 60), -1)
          # 진행 바 (AI 분석 신뢰도와 안정성 결합)
        if ai_analysis:
            ai_confidence = ai_analysis.get('confidence', 0)
            combined_progress = min(1.0, (stable_count / 10 + ai_confidence) / 2)
        else:
            combined_progress = min(1.0, stable_count / 10)
            
        progress_width = int(bar_width * combined_progress)
        
        # GitHub Copilot은 특별한 색상
        if ai_analysis and ai_analysis.get('provider') == 'GitHub Copilot':
            bar_color = self.color_palette['copilot']
        elif ai_analysis:
            bar_color = (100, 255, 255)
        else:
            bar_color = (100, 255, 100) if combined_progress > 0.5 else (255, 255, 100)
            
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + progress_width, bar_y + bar_height), 
                     bar_color, -1)
    
    def draw_modern_info_panel(self, frame, tracker_info):
        """모던한 정보 패널 그리기 - 전문적이고 컴팩트한 디자인"""
        height, width = frame.shape[:2]
        
        # 더 얇은 패널
        panel_height = 70
        panel = np.zeros((panel_height, width, 3), dtype=np.uint8)
        
        # 더 세련된 그라데이션 배경
        self._draw_professional_gradient(panel, width, panel_height)
        
        # 더 얇은 제목 바
        title_height = 20
        cv2.rectangle(panel, (0, 0), (width, title_height), self.color_palette['primary'], -1)
          # 더 작은 메인 제목 (GitHub Copilot 상태 포함)
        title_text = f"YOLO11 {tracker_info.get('model_name', '').replace('🚀 ', '')} + AI Analysis"
        if tracker_info.get('ai_provider') == 'GitHub Copilot':
            title_text += " 🤖Copilot"
        
        self.draw_professional_text(panel, title_text, (8, 2), 'small', (255, 255, 255), shadow=True)
        
        # 더 컴팩트한 성능 지표들
        self._draw_compact_performance_cards(panel, tracker_info)
        
        # 프레임과 패널 결합
        frame_with_panel = np.vstack([frame, panel])
        return frame_with_panel
    
    def _draw_professional_gradient(self, panel, width, panel_height):
        """전문적인 그라데이션 배경"""
        # 더 미묘한 그라데이션
        dark_color = (20, 20, 30)      # 매우 어두운 배경
        accent_color = (35, 50, 65)    # 미묘한 액센트
        
        for i in range(panel_height):
            ratio = i / panel_height
            b = int(dark_color[0] * (1 - ratio) + accent_color[0] * ratio)
            g = int(dark_color[1] * (1 - ratio) + accent_color[1] * ratio)
            r = int(dark_color[2] * (1 - ratio) + accent_color[2] * ratio)
            
            cv2.line(panel, (0, i), (width, i), (b, g, r), 1)
    
    def _draw_compact_performance_cards(self, panel, tracker_info):
        """컴팩트한 성능 지표 카드들 그리기"""
        card_width = 90
        card_height = 32
        card_spacing = 6
        start_x = 8
        start_y = 25
        
        # FPS 카드
        fps_value = tracker_info.get('fps', 0)
        fps_color = (100, 255, 100) if fps_value > 20 else (255, 255, 100) if fps_value > 10 else (255, 100, 100)
        self._draw_compact_metric_card(panel, start_x, start_y, card_width, card_height,
                                     "FPS", f"{fps_value:.1f}", fps_color)
        
        # 객체 수 카드
        obj_count = tracker_info.get('object_count', 0)
        self._draw_compact_metric_card(panel, start_x + card_width + card_spacing, start_y, 
                                     card_width, card_height,
                                     "Objects", str(obj_count), self.color_palette['info'])
          # 정확도 카드
        accuracy = tracker_info.get('accuracy', 0)
        acc_color = (100, 255, 100) if accuracy > 80 else (255, 255, 100) if accuracy > 60 else (255, 150, 100)
        self._draw_compact_metric_card(panel, start_x + 2 * (card_width + card_spacing), start_y,
                                     card_width, card_height,
                                     "Accuracy", f"{accuracy:.1f}%", acc_color)
        
        # AI 제공자 카드 (GitHub Copilot 강조)
        ai_provider = tracker_info.get('ai_provider', 'None')
        if ai_provider == 'GitHub Copilot':
            ai_color = self.color_palette['copilot']
            ai_text = "Copilot"
        else:
            ai_color = self.color_palette['teal']
            ai_text = ai_provider[:7] if ai_provider != 'None' else 'No AI'
            
        self._draw_compact_metric_card(panel, start_x + 3 * (card_width + card_spacing), start_y,
                                     card_width, card_height,
                                     "AI", ai_text, ai_color)
        
        # 안정적 객체 카드
        stable_count = tracker_info.get('stable_objects', 0)
        self._draw_compact_metric_card(panel, start_x + 4 * (card_width + card_spacing), start_y,
                                     card_width, card_height,
                                     "Stable", str(stable_count), self.color_palette['success'])
        
        # 모델 정보 카드
        model_params = tracker_info.get('model_params', 'N/A')
        self._draw_compact_metric_card(panel, start_x + 5 * (card_width + card_spacing), start_y,
                                     card_width, card_height,
                                     "Model", model_params, self.color_palette['accent'])
    
    def _draw_compact_metric_card(self, panel, x, y, width, height, title, value, color):
        """컴팩트한 개별 지표 카드 그리기"""
        # 더 미묘한 카드 배경
        overlay = panel.copy()
        
        # 둥근 사각형 배경
        self.draw_rounded_rectangle(overlay, (x, y), (x + width, y + height), color, -1, radius=3)
        
        # 반투명 적용
        cv2.addWeighted(panel, 0.85, overlay, 0.15, 0, panel)
        
        # 얇은 테두리
        self.draw_rounded_rectangle(panel, (x, y), (x + width, y + height), color, 1, radius=3)
        
        # 제목 (더 작게)
        self.draw_professional_text(panel, title, (x + 3, y + 2), 'tiny', (180, 180, 180), shadow=True)
        
        # 값 (더 선명하게)
        self.draw_professional_text(panel, value, (x + 3, y + 14), 'small', (255, 255, 255), shadow=True)

