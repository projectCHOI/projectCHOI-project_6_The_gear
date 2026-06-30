import pygame
import os
import random

class MusicManager:
    def __init__(self):
        """assets/music 폴더 내부에서 5개의 설치 효과음을 총괄하는 클래스"""
        # 현재 파일이 위치한 assets/music 폴더를 기준 경로로 잡습니다.
        self.base_path = os.path.dirname(__file__)
        self.install_sounds = []
        self._load_assets()
