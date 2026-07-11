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
