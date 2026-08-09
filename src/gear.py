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
        self.prev_angle = 0.0
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
def update_rotation(self, dt, visited=None):
    if visited is None:
        visited = set()

    if self in visited:
        return

    visited.add(self)

    if self.is_driver:

        # 자동 회전 속도가 있는 경우
        if self.target_speed != 0:
            self.angle += self.target_speed * dt

        # 이번 프레임의 실제 회전량
        angle_delta = self.angle - self.prev_angle

    else:

        # 일반 기어는 자신의 이전 각도와 비교
        angle_delta = self.angle - self.prev_angle

    for next_gear in self.connected_gears:

        if next_gear in visited:
            continue

        # 이빨 수 비율에 따른 회전량
        transmitted_delta = (
            -angle_delta *
            (self.teeth / next_gear.teeth)
        )

        next_gear.angle += transmitted_delta

        next_gear.update_rotation(
            dt,
            visited
        )

    self.prev_angle = self.angle

    def draw(self, screen):
        """화면에 톱니바퀴를 그리는 함수"""
        if self.original_image:
            # Pygame에서 이미지를 회전하면 이미지가 커지므로, 중심축이 틀어지지 않도록 보정 렌더링
            rotated_image = pygame.transform.rotate(self.original_image, self.angle)
            new_rect = rotated_image.get_rect(center=(self.x, self.y))
            screen.blit(rotated_image, new_rect.topleft)
        else:
            # 이미지가 없을 경우 개발용 임시 원형 도형 그리기
            # 중심원
            pygame.draw.circle(screen, (150, 150, 150), (self.x, self.y), self.radius, 2)
            # 회전하는 것을 눈으로 확인하기 위한 기준선(바늘) 그리기
            rad = math.radians(self.angle)
            end_x = self.x + self.radius * math.cos(rad)
            end_y = self.y - self.radius * math.sin(rad)  # Y축은 아래가 +이므로 빼줍니다.
            pygame.draw.line(screen, (255, 100, 100), (self.x, self.y), (end_x, end_y), 3)
            
            # 동력원인 경우 중심에 작은 노란 점 표시
            if self.is_driver:
                pygame.draw.circle(screen, (255, 215, 0), (self.x, self.y), 8)
