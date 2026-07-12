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
