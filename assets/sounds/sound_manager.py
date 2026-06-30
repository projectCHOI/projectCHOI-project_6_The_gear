import pygame
import os

class SoundManager:
    def __init__(self):
        self.base_path = os.path.dirname(__file__)
        self.effects = {}
        self._load_assets()

    def _load_assets(self):
        try:
            clear_path = os.path.join(self.base_path, "stage_clear.mp3")
            fail_path = os.path.join(self.base_path, "game_over.mp3")
            
            if os.path.exists(clear_path):
                self.effects["clear"] = pygame.mixer.Sound(clear_path)
            if os.path.exists(fail_path):
                self.effects["fail"] = pygame.mixer.Sound(fail_path)
                
        except pygame.error as e:
            print(f"SoundManager 로드 오류: {e}")
