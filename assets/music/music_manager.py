import pygame
import os
import random

class MusicManager:
    def __init__(self):
        self.base_path = os.path.dirname(__file__)
        self.install_sounds = []
        self._load_assets()
def _load_assets(self):
        try:
            for i in range(1, 6):
                filename = f"music05.wav" if i < 10 else f"music{i}.wav" # 형식 보정
                filename = f"music0{i}.wav" # 올려주신 music01 규칙 적용
                install_path = os.path.join(self.base_path, filename)
                
                if os.path.exists(install_path):
                    self.install_sounds.append(pygame.mixer.Sound(install_path))
                    
            print(f"MusicManager 로드 완료: 설치 효과음 {len(self.install_sounds)}개 대기 중.")
        except pygame.error as e:
            print(f"MusicManager 로드 오류: {e}")
            
def play_install_sound(self):
        if self.install_sounds:
            chosen_sound = random.choice(self.install_sounds)
            chosen_sound.play()
