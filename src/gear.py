# 객체의 속성과 회전 로직
import pygame
import math

class Gear:
    def __init__(self, x, y, radius, teeth, image_path=None, is_driver=False):
        self.x = x
        self.y = y
        self.radius = radius
        self.teeth = teeth
        self.is_driver = is_driver
        # 현재 회전 각도 (도 단위, Degree)
        self.angle = 0.0
        # 회전 속도 (초당 회전 각도, 동력원인 경우 사용)
        self.target_speed = 0.0  
        # 맞물려 있는 다른 톱니바퀴 객체들의 리스트
        self.connected_gears = []
        # 이미지 로드 및 크기 조정
        self.original_image = None
        if image_path:
            try:
                # 이미지를 불러오고 투명도(Alpha)를 유지하도록 설정
                raw_image = pygame.image.load(image_path).convert_alpha()
                # 톱니바퀴 반지름에 맞게 이미지 크기를 지름(radius * 2) 크기로 맞춤
                self.original_image = pygame.transform.smoothscale(raw_image, (radius * 2, radius * 2))
            except pygame.error:
                print(f"경고: {image_path} 이미지를 로드할 수 없습니다. 기본 도형으로 대체합니다.")
                self.original_image = None
