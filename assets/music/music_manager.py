import pygame
import os
import random

class MusicManager:
    def __init__(self):
        self.base_path = os.path.dirname(__file__)
        self.effects = {}
        self.install_sounds = []  # 5개의 설치 효과음을 담을 리스트
        self._load_assets()

def _load_assets(self):
        try:
            # 1. 일반 효과음 등록
            clear_path = os.path.join(self.base_path, "stage_clear.wav")
            fail_path = os.path.join(self.base_path, "game_over.wav")
            
            if os.path.exists(clear_path):
                self.effects["clear"] = pygame.mixer.Sound(clear_path)
            if os.path.exists(fail_path):
                self.effects["fail"] = pygame.mixer.Sound(fail_path)
                
            # 2. ⚙️ 톱니바퀴 설치 효과음 5개 연속 등록 규칙
            for i in range(1, 6):
                install_path = os.path.join(self.base_path, f"gear_install{i}.wav")
                if os.path.exists(install_path):
                    sound_obj = pygame.mixer.Sound(install_path)
                    self.install_sounds.append(sound_obj)
                    
            print(f"오디오 시스템 로드 완료: 설치 효과음 {len(self.install_sounds)}개 대기 중.")
                
        except pygame.error as e:
            print(f"사운드 시스템 로드 오류: {e}")

def play_bgm(self, state="play"):
        if state == "main":
            filename = "main_menu.mp3"
        elif state == "play":
            filename = "play_bgm.mp3"
        else:
            return

        bgm_path = os.path.join(self.base_path, filename)
        
        if os.path.exists(bgm_path):
            pygame.mixer.music.load(bgm_path)
            pygame.mixer.music.play(-1)  
            print(f"🎵 배경음악 재생: {filename}")
        else:
            print(f"안내: {bgm_path} 파일이 없습니다.")

def stop_bgm(self):
        pygame.mixer.music.stop()

def play_effect(self, name):
    """일반 효과음 재생"""
    if name in self.effects:
        self.effects[name].play()

def play_install_sound(self):
    """5개의 설치 효과음 중 하나를 무작위로 골라 재생하는 함수"""
    if self.install_sounds:
        # 리스트에 담긴 5개 소리 중 무작위 하나 선택
        chosen_sound = random.choice(self.install_sounds)
        chosen_sound.play()