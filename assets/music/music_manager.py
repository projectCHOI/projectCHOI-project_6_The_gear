import pygame
import os
import random

class MusicManager:
    def __init__(self):
        self.base_path = os.path.dirname(__file__)
        self.effects = {}
        self.install_sounds = []  # 5개의 설치 효과음을 담을 리스트
        self._load_assets()
