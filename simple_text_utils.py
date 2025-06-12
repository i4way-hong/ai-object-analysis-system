# -*- coding: utf-8 -*-
"""
Simple Text Utils
간단한 텍스트 처리 유틸리티 함수들
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os


def put_korean_text(image, text, position, font_size=16, color=(255, 255, 255), 
                   background_color=None, font_path=None):
    """
    이미지에 한글 텍스트를 추가하는 함수
    
    Args:
        image: OpenCV 이미지 (numpy array)
        text: 표시할 텍스트
        position: (x, y) 좌표
        font_size: 폰트 크기
        color: 텍스트 색상 (BGR)
        background_color: 배경 색상 (선택사항)
        font_path: 폰트 파일 경로 (선택사항)
    
    Returns:
        텍스트가 추가된 이미지
    """
    try:
        # OpenCV BGR -> PIL RGB 변환
        img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)
        
        # 폰트 설정
        if font_path and os.path.exists(font_path):
            font = ImageFont.truetype(font_path, font_size)
        else:
            # 시스템 기본 폰트 사용 시도
            try:
                # Windows용 기본 한글 폰트
                font = ImageFont.truetype("malgun.ttf", font_size)
            except:
                try:
                    font = ImageFont.truetype("NanumGothic.ttf", font_size)
                except:
                    # 기본 폰트 사용
                    font = ImageFont.load_default()
        
        # 색상 변환 (BGR -> RGB)
        text_color = (color[2], color[1], color[0]) if len(color) == 3 else color
        
        # 배경 박스 그리기 (선택사항)
        if background_color:
            bbox = draw.textbbox(position, text, font=font)
            bg_color = (background_color[2], background_color[1], background_color[0]) if len(background_color) == 3 else background_color
            draw.rectangle(bbox, fill=bg_color)
        
        # 텍스트 그리기
        draw.text(position, text, fill=text_color, font=font)
        
        # PIL RGB -> OpenCV BGR 변환
        img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        return img_cv
        
    except Exception as e:
        print(f"한글 텍스트 렌더링 오류: {e}")
        # 오류 발생 시 OpenCV 기본 함수 사용
        cv2.putText(image, text, position, cv2.FONT_HERSHEY_SIMPLEX, 
                   font_size/20, color, 1, cv2.LINE_AA)
        return image


def get_text_size(text, font_size=16, font_path=None):
    """
    텍스트의 크기를 계산하는 함수
    
    Args:
        text: 측정할 텍스트
        font_size: 폰트 크기
        font_path: 폰트 파일 경로 (선택사항)
    
    Returns:
        (width, height) 튜플
    """
    try:
        # 임시 이미지 생성
        temp_img = Image.new('RGB', (1, 1))
        draw = ImageDraw.Draw(temp_img)
        
        # 폰트 설정
        if font_path and os.path.exists(font_path):
            font = ImageFont.truetype(font_path, font_size)
        else:
            try:
                font = ImageFont.truetype("malgun.ttf", font_size)
            except:
                try:
                    font = ImageFont.truetype("NanumGothic.ttf", font_size)
                except:
                    font = ImageFont.load_default()
        
        # 텍스트 크기 계산
        bbox = draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        
        return (width, height)
        
    except Exception as e:
        print(f"텍스트 크기 계산 오류: {e}")
        # 오류 발생 시 대략적인 크기 반환
        return (len(text) * font_size // 2, font_size)


def wrap_text(text, max_width, font_size=16, font_path=None):
    """
    텍스트를 지정된 너비에 맞게 줄바꿈하는 함수
    
    Args:
        text: 원본 텍스트
        max_width: 최대 너비 (픽셀)
        font_size: 폰트 크기
        font_path: 폰트 파일 경로 (선택사항)
    
    Returns:
        줄바꿈된 텍스트 리스트
    """
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + " " + word if current_line else word
        width, _ = get_text_size(test_line, font_size, font_path)
        
        if width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
                current_line = word
            else:
                lines.append(word)
    
    if current_line:
        lines.append(current_line)
    
    return lines


if __name__ == "__main__":
    # 테스트 코드
    print("Simple Text Utils 테스트")
    
    # 텍스트 크기 테스트
    text = "안녕하세요 Hello World"
    size = get_text_size(text, 16)
    print(f"텍스트 '{text}' 크기: {size}")
    
    # 텍스트 줄바꿈 테스트
    long_text = "이것은 매우 긴 텍스트입니다 줄바꿈이 필요할 수 있습니다"
    wrapped = wrap_text(long_text, 100, 16)
    print(f"줄바꿈 결과: {wrapped}")
