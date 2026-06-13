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

        def connect(self, other_gear):
                if other_gear not in self.connected_gears:
                    self.connected_gears.append(other_gear)
                    other_gear.connected_gears.append(self)  # 양방향 연결

    def update_rotation(self, dt, visited=None):
        """
        동력 전달 법칙에 따라 연결된 모든 톱니바퀴의 회전각을 업데이트하는 재귀 함수
        """
        if visited is None:
            visited = set()
            
        visited.add(self)

        # 동력원(Driver)인 경우 스스로 지정된 속도만큼 회전
        if self.is_driver and len(visited) == 1:
            self.angle += self.target_speed * dt

        # 연결된 다른 톱니바퀴들에게 동력과 회전각 전달
        for next_gear in self.connected_gears:
            if next_gear not in visited:
                # [동력 전달 핵심 공식]
                # 1. 방향은 반대 (-1)
                # 2. 회전각 변화량은 이빨 개수 비율에 반비례 (내 이빨 수 / 상대 이빨 수)
                angle_delta = (self.target_speed * dt) if self.is_driver and len(visited) == 1 else (self.angle - getattr(self, 'prev_angle', self.angle))
                
                # 상대방의 이전 각도를 백업하고 새로운 각도 계산
                next_gear.prev_angle = next_gear.angle
                next_gear.angle -= angle_delta * (self.teeth / next_gear.teeth)
                
                # 연쇄적으로 다음 톱니바퀴 업데이트 (그래프 탐색)
                next_gear.update_rotation(dt, visited)
                
        # 다음 프레임 계산을 위해 현재 각도를 저장
        self.prev_angle = self.angle
