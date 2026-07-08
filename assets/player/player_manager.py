import pygame
import os
import math

class PlayerManager:
    def __init__(self, screen_width, screen_height):
        """
        플레이어의 상태, 재화, 인벤토리 및 마우스 조작(드래그)을 총괄 관리하는 통합 클래스
        """
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
        
        # 3. 마우스 입력 및 조작 제어 설정 (기존 player.py 흡수)
        self.selected_gear = None    # 현재 마우스로 붙잡고 있는 톱니바퀴 객체
        self.is_dragging = False     # 드래그 중인지 여부
        self.last_mouse_angle = 0.0  # 직전 프레임의 마우스 각도
        
        # 4. 이미지 및 애니메이션 제어 설정
        self.base_path = os.path.dirname(__file__)
        self.image_path = os.path.join(self.base_path, "..", "images", "player.png")
        
        self.raw_image = self._load_player_image()
        self.current_image = self.raw_image
        
        # 플레이어 캐릭터 렌더링 위치 설정 (화면 좌측 하단 배치)
        self.x = 80
        self.y = screen_height - 160
        self.animation_timer = 0.0

    def _load_player_image(self):
        """지정된 경로에서 player.png 이미지를 안전하게 로드하는 내부 함수"""
        if os.path.exists(self.image_path):
            try:
                img = pygame.image.load(self.image_path).convert_alpha()
                return pygame.transform.smoothscale(img, (96, 96))
            except pygame.error:
                print(f"경고: {self.image_path} 파일 손상 또는 로드 불가. 기본 사각형으로 대체합니다.")
                return None
        else:
            print(f"안내: {self.image_path} 이미지가 존재하지 않습니다. 기본 사각형으로 대체합니다.")
        return None

    def handle_event(self, event, gears):
        """[통합] 메인 루프에서 마우스 이벤트를 받아 직접 드래그 상호작용을 처리하는 함수"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 마우스 왼쪽 버튼 클릭
                mouse_x, mouse_y = event.pos
                
                # 배치된 톱니바퀴 중 플레이어가 직접 돌릴 수 있는 '동력원(Driver)'을 탐색
                for gear in gears:
                    if gear.is_driver:
                        # 마우스 클릭 위치가 톱니바퀴 반지름 안에 있는지 거리 계산 (피타고라스)
                        distance = math.hypot(mouse_x - gear.x, mouse_y - gear.y)
                        if distance <= gear.radius:
                            self.selected_gear = gear
                            self.is_dragging = True
                            # 클릭한 순간의 마우스 중심각 계산
                            self.last_mouse_angle = self.calculate_angle(mouse_x, mouse_y, gear)
                            # 수동 조작을 시작하므로 기존 자동 회전 속도는 0으로 초기화
                            gear.target_speed = 0.0
                            break

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # 마우스 왼쪽 버튼을 떼면 조작 해제
                self.is_dragging = False
                self.selected_gear = None