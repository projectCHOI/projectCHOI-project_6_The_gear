import pygame
import os

class SoundManager:
    def __init__(self):
        self.base_path = os.path.dirname(__file__)
        
        self.effects = {}
        self._load_assets()

    def _load_assets(self):
        try:
            install_path = os.path.join(self.base_path, "gear_install.wav")
            clear_path = os.path.join(self.base_path, "stage_clear.wav")
            fail_path = os.path.join(self.base_path, "game_over.wav")
            
            if os.path.exists(install_path):
                self.effects["install"] = pygame.mixer.Sound(install_path)
            if os.path.exists(clear_path):
                self.effects["clear"] = pygame.mixer.Sound(clear_path)
            if os.path.exists(fail_path):
                self.effects["fail"] = pygame.mixer.Sound(fail_path)
                
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
        if name in self.effects:
            self.effects[name].play()