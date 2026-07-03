import pygame
import os

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
