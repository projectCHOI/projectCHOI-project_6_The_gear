import pygame
import sys
import os

class PuzzleManager:
    def __init__(self):
        self.gears = []          
        self.current_level = 1   
        self.is_cleared = False   
        self.clear_condition = None
        
        # 🔑 서사 가젯 상태 규칙 변수 추가
        self.is_box_open = False    # 상자가 열렸는가?
        self.has_key = False        # 플레이어가 열쇠를 주웠는가?
        self.door_unlocked = False  # 문을 열었는가?
        
        # 상자, 열쇠, 문의 가상 영역 (X, Y, 가로, 세로)
        self.box_rect = pygame.Rect(750, 310, 100, 100)
        self.key_rect = pygame.Rect(775, 335, 50, 30)   # 상자 안쪽에 위치
        self.door_rect = pygame.Rect(1050, 260, 120, 200) # 화면 우측 끝 배치
        
        self.load_level(self.current_level)

    def load_level(self, level_num):
        self.gears.clear()
        self.is_cleared = False
        self.is_box_open = False
        self.has_key = False
        self.door_unlocked = False
        self.current_level = level_num

        stage_module_name = f"stage{level_num:02d}_manager"
        try:
            stage_module = __import__(stage_module_name)
            self.gears, self.clear_condition = stage_module.get_stage_data()
            print(f"📦 레벨 {level_num} 스토리 동기 팩 이식 완료.")
        except Exception as e:
            print(f"❌ 로드 오류: {e}")

    def update(self, dt):
        if not self.gears:
            return
        
        # 1단계: 문이 완전히 열리기 전까지만 톱니 물리 연산 가동
        if not self.is_box_open:
            for gear in self.gears:
                if gear.is_driver:
                    gear.update_rotation(dt)
                    break  
            self.check_clear_condition()
        
    def check_clear_condition(self):
        if not self.clear_condition or not self.gears:
            return

        target_idx = self.clear_condition["target_index"]
        req_angle = self.clear_condition["required_angle"]

        if len(self.gears) > target_idx:
            target_gear = self.gears[target_idx]  
            if abs(target_gear.angle) >= req_angle:
                if not self.is_box_open:
                    self.is_box_open = True
                    print("🔓 톱니바퀴 연동 완료! 보물상자가 찰칵하며 열렸습니다.")

    def handle_clicks(self, mouse_pos):
        """[★스토리 클릭 감시 규칙] 메인에서 마우스 클릭 좌표를 넘겨받아 상호작용"""
        # 상자가 열린 상태에서 열쇠 영역을 클릭하면 열쇠 획득
        if self.is_box_open and not self.has_key:
            if self.key_rect.collidepoint(mouse_pos):
                self.has_key = True
                print("🔑 열쇠를 획득했습니다! 인벤토리에 보관합니다.")
                return "get_key"
                
        # 열쇠를 가진 상태에서 닫힌 문을 클릭하면 문 열림
        if self.has_key and not self.door_unlocked:
            if self.door_rect.collidepoint(mouse_pos):
                self.door_unlocked = True
                self.is_cleared = True # 최종 스테이지 클리어 처리 권한 이관
                print("🚪 문에 열쇠를 꽂고 돌렸습니다! 다음 구역으로 통하는 문이 열립니다.")
                return "unlock_door"
        return None

    def draw(self, screen):
        # 기존 톱니바퀴 드로우
        for gear in self.gears:
            gear.draw(screen)
            
        # 🎨 인라인 도형 렌더링으로 상자/열쇠/문 시각화
        font = pygame.font.SysFont("malgungothic", 16)
        
        # A. 문(Door) 그리기
        door_color = (150, 75, 0) if not self.door_unlocked else (100, 200, 255)
        pygame.draw.rect(screen, door_color, self.door_rect, 0 if self.door_unlocked else 4)
        door_lbl = font.render("🚪 굳게 닫힌 문" if not self.door_unlocked else "✨ 열린 통로", True, (220, 220, 220))
        screen.blit(door_lbl, (self.door_rect.x, self.door_rect.y - 25))

        # B. 보물상자(Box) 그리기
        box_color = (139, 69, 19) if not self.is_box_open else (205, 133, 63)
        pygame.draw.rect(screen, box_color, self.box_rect, 4 if not self.is_box_open else 0)
        box_lbl = font.render("🧰 잠긴 상자" if not self.is_box_open else "🔓 열린 상자", True, (220, 220, 220))
        screen.blit(box_lbl, (self.box_rect.x, self.box_rect.y - 25))

        # C. 열쇠(Key) 그리기 (상자가 열렸고, 아직 주우지 않았을 때만 노출)
        if self.is_box_open and not self.has_key:
            pygame.draw.rect(screen, (255, 215, 0), self.key_rect)
            key_lbl = font.render("🔑 KEY", True, (255, 215, 0))
            screen.blit(key_lbl, (self.key_rect.x, self.key_rect.y - 20))
