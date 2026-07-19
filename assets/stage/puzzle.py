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
