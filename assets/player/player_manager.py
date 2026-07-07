import pygame
import os
import math

class PlayerManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        # 1. 플레이어 데이터 및 재화 관리
        self.score = 0
        self.gold = 0
        self.current_state = "IDLE"  # "IDLE" (대기), "ROTATING" (톱니 돌리는 중)
        # 2. 인벤토리 관리 (가방에 소지한 톱니바퀴 종류별 개수)
        self.inventory = {
            "small_gear": 3,   # 소형 톱니바퀴
            "medium_gear": 2,  # 중형 톱니바퀴
            "large_gear": 1    # 대형 톱니바퀴
        }
        # 3. 이미지 및 애니메이션 제어 설정
        self.base_path = os.path.dirname(__file__)
        # project_6_The gear/assets/images/player.png 경로 조립
        self.image_path = os.path.join(self.base_path, "..", "assets", "images", "player.png")
        self.raw_image = self._load_player_image()
        self.current_image = self.raw_image
        # 플레이어 캐릭터 렌더링 위치 설정 (화면 좌측 하단 배치)
        self.x = 80
        self.y = screen_height - 160
        # 상태별 애니메이션 처리를 위한 타이머 변수
        self.animation_timer = 0.0

    def _load_player_image(self):
        if os.path.exists(self.image_path):
            try:
                img = pygame.image.load(self.image_path).convert_alpha()
                # 캐릭터에 적합한 사이즈(예: 가로 96 x 세로 96 픽셀)로 부드럽게 스케일링
                return pygame.transform.smoothscale(img, (96, 96))
            except pygame.error:
                print(f"경고: {self.image_path} 파일 손상 또는 로드 불가. 기본 사각형으로 대체합니다.")
                return None
        else:
            print(f"안내: {self.image_path} 이미지가 존재하지 않습니다. 기본 사각형으로 대체합니다.")
        return None

    def _load_player_image(self):
        if os.path.exists(self.image_path):
            try:
                img = pygame.image.load(self.image_path).convert_alpha()
                # 캐릭터에 적합한 사이즈(예: 가로 96 x 세로 96 픽셀)로 부드럽게 스케일링
                return pygame.transform.smoothscale(img, (96, 96))
            except pygame.error:
                print(f"경고: {self.image_path} 파일 손상 또는 로드 불가. 기본 사각형으로 대체합니다.")
                return None
        else:
            print(f"안내: {self.image_path} 이미지가 존재하지 않습니다. 기본 사각형으로 대체합니다.")
        return None

    def update(self, dt, is_player_dragging):
        # A. 마우스 드래그 상태에 따라 실시간 상태 전환 (IDLE <-> ROTATING)
        if is_player_dragging:
            self.current_state = "ROTATING"
        else:
            self.current_state = "IDLE"

        # B. 상태별 렌더링 이미지 제어 (애니메이션 연출)
        if self.raw_image:
            self.animation_timer += dt
            if self.current_state == "ROTATING":
                # 톱니바퀴를 돌릴 때 캐릭터가 역동적으로 힘을 쓰듯 미세하게 들썩이는 효과 (사인파 활용)
                bounce = int(math.sin(self.animation_timer * 15) * 4) if 'math' in globals() else 0
                # 회전 액션을 시각적으로 표현하기 위해 약간 기울이거나 오프셋을 줄 수 있습니다.
                self.current_image = self.raw_image
            else:
                # 대기 상태일 때는 기본 이미지 유지
                self.current_image = self.raw_image

    def add_gold(self, amount):
        if amount > 0:
            self.gold += amount

    def add_score(self, amount):
        if amount > 0:
            self.score += amount

    def use_gear_from_inventory(self, gear_type):
        if gear_type in self.inventory and self.inventory[gear_type] > 0:
            self.inventory[gear_type] -= 1
            print(f"⚙️ {gear_type} 1개 사용됨. 남은 개수: {self.inventory[gear_type]}")
            return True
        print(f"❌ {gear_type} 부품이 부족합니다!")
        return False

    def draw(self, screen):
        # 1. 캐릭터 이미지 그리기
        if self.current_image:
            # 톱니 조작 중일 때 미세한 바운스 효과가 적용된 좌표로 드로우
            draw_y = self.y
            if self.current_state == "ROTATING":
                import math
                draw_y += int(math.sin(self.animation_timer * 20) * 3)
            screen.blit(self.current_image, (self.x, draw_y))
        else:
            # player.png가 없을 때 영역 식별을 위한 임시 초록색 사각형
            pygame.draw.rect(screen, (50, 200, 50), (self.x, self.y, 96, 96))
