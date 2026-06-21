import pygame
import os

class SoundManager:
    def __init__(self):
        """게임 내 모든 사운드 자원(BGM, 효과음)을 로드하고 관리하는 클래스"""
        # 사운드 파일이 모여있는 기본 경로 설정
        self.base_path = os.path.join("assets", "sounds")
        
        # 효과음들을 저장할 딕셔너리 주머니
        self.effects = {}
        
        # 초기화와 동시에 파일들을 메모리에 로드
        self._load_assets()

    def _load_assets(self):
        """지정된 경로에서 사운드 파일들을 안전하게 불러오는 내부 함수"""
        try:
            # 1. 효과음 등록 (메모리에 미리 올려두고 즉시 뿜어내는 방식)
            install_path = os.path.join(self.base_path, "gear_install.wav")
            clear_path = os.path.join(self.base_path, "stage_clear.wav")
            
            if os.path.exists(install_path):
                self.effects["install"] = pygame.mixer.Sound(install_path)
            else:
                print(f"안내: {install_path} 파일이 없어 임시 무음 처리됩니다.")
                
            if os.path.exists(clear_path):
                self.effects["clear"] = pygame.mixer.Sound(clear_path)
            else:
                print(f"안내: {clear_path} 파일이 없어 임시 무음 처리됩니다.")
                
        except pygame.error as e:
            print(f"사운드 시스템 로드 중 오류 발생: {e}")

    def play_bgm(self, filename="bgm.mp3"):
        """배경음악을 스트리밍 방식으로 무한 반복 재생하는 함수"""
        bgm_path = os.path.join(self.base_path, filename)
        if os.path.exists(bgm_path):
            pygame.mixer.music.load(bgm_path)
            pygame.mixer.music.play(-1)  # -1은 무한 루프 반복
            print(f"🎵 배경음악 재생 시작: {filename}")
        else:
            print(f"안내: {bgm_path} 배경음악 파일이 없습니다.")