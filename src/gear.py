import pygame
import math


class Gear:
    def __init__(
        self,
        x,
        y,
        radius,
        teeth,
        image_path=None,
        is_driver=False
    ):
        self.x = x
        self.y = y
        self.radius = radius
        self.teeth = teeth
        self.is_driver = is_driver

        # 현재 회전 각도
        self.angle = 0.0

        # 이전 프레임의 회전 각도
        self.prev_angle = 0.0

        # 자동 회전 속도
        self.target_speed = 0.0

        # 연결된 톱니바퀴
        self.connected_gears = []

        # 이미지
        self.original_image = None

        if image_path:
            try:
                raw_image = pygame.image.load(
                    image_path
                ).convert_alpha()

                self.original_image = pygame.transform.smoothscale(
                    raw_image,
                    (radius * 2, radius * 2)
                )

            except pygame.error:
                print(
                    f"경고: {image_path} 이미지를 로드할 수 없습니다. "
                    "기본 도형으로 대체합니다."
                )

                self.original_image = None

    def connect(self, other_gear):

        if other_gear not in self.connected_gears:
            self.connected_gears.append(other_gear)

        if self not in other_gear.connected_gears:
            other_gear.connected_gears.append(self)

    def update_rotation(self, dt, visited=None):
        if visited is None:
            visited = set()

        if self in visited:
            return

        visited.add(self)

        # 자동 회전이 설정된 Driver인 경우
        if self.is_driver and self.target_speed != 0:
            self.angle += self.target_speed * dt

        # 이번 프레임에서 움직인 각도
        angle_delta = self.angle - self.prev_angle

        # 연결된 톱니바퀴로 전달
        for next_gear in self.connected_gears:

            if next_gear in visited:
                continue

            transmitted_delta = (
                -angle_delta
                * (self.teeth / next_gear.teeth)
            )

            next_gear.angle += transmitted_delta

            next_gear.update_rotation(
                dt,
                visited
            )

        self.prev_angle = self.angle

    def draw(self, screen):
        if self.original_image:

            rotated_image = pygame.transform.rotate(
                self.original_image,
                self.angle
            )

            new_rect = rotated_image.get_rect(
                center=(self.x, self.y)
            )

            screen.blit(
                rotated_image,
                new_rect.topleft
            )

        else:
            pygame.draw.circle(
                screen,
                (150, 150, 150),
                (self.x, self.y),
                self.radius,
                2
            )

            rad = math.radians(self.angle)

            end_x = (
                self.x
                + self.radius * math.cos(rad)
            )

            end_y = (
                self.y
                - self.radius * math.sin(rad)
            )

            pygame.draw.line(
                screen,
                (255, 100, 100),
                (self.x, self.y),
                (end_x, end_y),
                3
            )

            if self.is_driver:
                pygame.draw.circle(
                    screen,
                    (255, 215, 0),
                    (self.x, self.y),
                    8
                )