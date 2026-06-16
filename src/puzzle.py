import pygame
from gear import Gear

class PuzzleManager:
    def __init__(self):
        """퍼즐 스테이지와 톱니바퀴 그룹을 총괄 관리하는 클래스"""
        self.gears = []          
        self.current_level = 1   
        self.is_cleared = False   
        
        self.load_level(self.current_level)

    def load_level(self, level_num):
        """지정한 레벨의 톱니바퀴 배치 데이터와 클리어 조건을 불러오는 함수"""
        self.gears.clear()
        self.is_cleared = False
        self.current_level = level_num

        if level_num == 1:
            driver_gear = Gear(x=300, y=360, radius=80, teeth=24, is_driver=True)
            driver_gear.target_speed = 45.0  
            
            target_gear = Gear(x=450, y=360, radius=60, teeth=18, is_driver=False)
            
            driver_gear.connect(target_gear)
            
            self.gears.append(driver_gear)
            self.gears.append(target_gear)
            
            print(f"Level {level_num} loaded successfully.")
