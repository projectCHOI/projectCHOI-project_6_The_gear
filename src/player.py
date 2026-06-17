import pygame
import math

class PlayerController:
    def __init__(self):
        """플레이어의 마우스 입력 및 톱니바퀴 드래그 조작을 관리하는 클래스"""
        self.selected_gear = None  # 현재 마우스로 붙잡고 있는 톱니바퀴 객체
        self.is_dragging = False   # 드래그 중인지 여부
        self.last_mouse_angle = 0.0 # 직전 프레임의 마우스 각도
