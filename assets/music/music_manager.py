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
def _load_assets(self):
        try:
            # music01.wav ~ music05.wav 파일을 반복문으로 안전하게 등록
            for i in range(1, 6):
                filename = f"music05.wav" if i < 10 else f"music{i}.wav" # 형식 보정
                filename = f"music0{i}.wav" # 올려주신 music01 규칙 적용
                install_path = os.path.join(self.base_path, filename)
                
                if os.path.exists(install_path):
                    self.install_sounds.append(pygame.mixer.Sound(install_path))
                    
            print(f"MusicManager 로드 완료: 설치 효과음 {len(self.install_sounds)}개 대기 중.")
        except pygame.error as e:
            print(f"MusicManager 로드 오류: {e}")
