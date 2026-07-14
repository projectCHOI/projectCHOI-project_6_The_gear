import pygame
import sys
import os

class PuzzleManager:
    def __init__(self):
        self.gears = []          
        self.current_level = 1   
        self.is_cleared = False   
        self.clear_condition = None
        
        self.load_level(self.current_level)

def load_level(self, level_num):
        self.gears.clear()
        self.is_cleared = False
        self.current_level = level_num

        # 문자열 포맷팅을 통해 stage01, stage02 등의 파일을 가변적으로 매핑
        stage_module_name = f"stage{level_num:02d}_manager"

        try:
            # 실시간으로 해당 스테이지 모듈을 불러옵니다.
            stage_module = __import__(stage_module_name)
            # 설계도 함수를 실행하여 톱니바퀴들과 클리어 조건을 이식받습니다.
            self.gears, self.clear_condition = stage_module.get_stage_data()
            print(f"📦 레벨 {level_num} 데이터 팩 로드 성우!")
        except Exception as e:
            print(f"❌ 레벨 {level_num} 데이터 팩을 로드하는 중 오류 발생: {e}")

def update(self, dt):
        if not self.gears:
            return
        
        # 동력원 톱니바퀴를 찾아 회전력을 전파시킵니다.
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
                if not self.is_cleared:
                    self.is_cleared = True
                    print(f"🎉 Level {self.current_level} Cleared!")

def draw(self, screen):
        for gear in self.gears:
            gear.draw(screen)
