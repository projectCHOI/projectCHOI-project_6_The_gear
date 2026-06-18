import pygame
import math

class PlayerController:
    def __init__(self):
        """플레이어의 마우스 입력 및 톱니바퀴 드래그 조작을 관리하는 클래스"""
        self.selected_gear = None  # 현재 마우스로 붙잡고 있는 톱니바퀴 객체
        self.is_dragging = False   # 드래그 중인지 여부
        self.last_mouse_angle = 0.0 # 직전 프레임의 마우스 각도
        
            def handle_event(self, event, gears):
                """메인 루프에서 마우스 이벤트를 받아 처리하는 함수"""
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 마우스 왼쪽 버튼 클릭
                        mouse_x, mouse_y = event.pos
                
                # 배치된 톱니바퀴 중 플레이어가 직접 돌릴 수 있는 '동력원(Driver)'을 찾습니다.
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

    def update(self, gears):
        """마우스를 드래그하고 있을 때 실시간으로 톱니바퀴 각도를 변화시키는 함수"""
        if self.is_dragging and self.selected_gear:
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
