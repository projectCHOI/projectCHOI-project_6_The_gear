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
            
                def update(self, dt):
                    if not self.gears:
                        return
            
                    for gear in self.gears:
                        if gear.is_driver:
                            gear.update_rotation(dt)
                            break  
            
                    self.check_clear_condition()
                    
                def check_clear_condition(self):
                        if self.current_level == 1 and len(self.gears) >= 2:
                            target_gear = self.gears[1]  
                            if abs(target_gear.angle) >= 360.0:
                                if not self.is_cleared:
                                    self.is_cleared = True
                                    print("Level 1 Cleared!")
                
                    def draw(self, screen):
                        for gear in self.gears:
                            gear.draw(screen)
