import pygame
from gear import Gear

class PuzzleManager:
    def __init__(self):
        """퍼즐 스테이지와 톱니바퀴 그룹을 총괄 관리하는 클래스"""
        self.gears = []          
        self.current_level = 1   
        self.is_cleared = False   
        
        self.load_level(self.current_level)
