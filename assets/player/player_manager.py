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

    def update(self, dt):
            if self.is_dragging and self.selected_gear:
                self.current_state = "ROTATING"
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # 현재 마우스가 톱니바퀴 중심을 기준으로 몇 도 위치에 있는지 계산
                current_mouse_angle = self.calculate_angle(mouse_x, mouse_y, self.selected_gear)
                
                # 직전 프레임 각도와 현재 각도의 차이(변화량) 계산
                angle_delta = current_mouse_angle - self.last_mouse_angle
                
                # 각도가 180도에서 -180도로 급격하게 바뀌는 경계선 보정 (-360도 평활화)
                if angle_delta > 180:
                    angle_delta -= 360
                elif angle_delta < -180:
                    angle_delta += 360
                    
                # 계산된 변화량만큼 동력원 톱니바퀴를 직접 회전시킴
                self.selected_gear.angle += angle_delta
                
                # 다음 프레임 연산을 위해 현재 각도를 백업
                self.last_mouse_angle = current_mouse_angle
            else:
                self.current_state = "IDLE"

            # B. 상태별 렌더링 애니메이션 처리
            if self.raw_image:
                self.animation_timer += dt
                if self.current_state == "ROTATING":
                    # 톱니바퀴를 돌릴 때 캐릭터가 역동적으로 힘을 쓰듯 미세하게 들썩이는 효과 (사인파 활용)
                    self.current_image = self.raw_image
                else:
                    self.current_image = self.raw_image

    def calculate_angle(self, m_x, m_y, gear):
        radians = math.atan2(gear.y - m_y, m_x - gear.x)
        return math.degrees(radians)

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
        if self.current_image:
            draw_y = self.y
            if self.current_state == "ROTATING":
                draw_y += int(math.sin(self.animation_timer * 20) * 3)
            screen.blit(self.current_image, (self.x, draw_y))
        else:
            pygame.draw.rect(screen, (50, 200, 50), (self.x, self.y, 96, 96))