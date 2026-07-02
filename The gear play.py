import pygame
import sys
import os

# 1. 서브 모듈들이 상주하는 올바른 하위 폴더 경로들을 시스템 명부에 추가
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'assets', 'sounds'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'assets', 'music'))

# 2. 명부에 등록된 경로에서 각 클래스 안전하게 임포트
from stage import PuzzleManager
from player import PlayerController
from sound_manager import SoundManager  # assets/sounds 폴더에서 로드
from music_manager import MusicManager  # assets/music 폴더에서 로드

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Gear : The Puzzler")

clock = pygame.time.Clock()
FPS = 60
COLOR_BG = (30, 30, 35)
COLOR_TEXT = (220, 220, 220)

def main():
    puzzle_manager = PuzzleManager()
    player_controller = PlayerController()
    
    # 3. 양대 사운드 자산 관리 시스템 인스턴스 생성
    sound_manager = SoundManager()
    music_manager = MusicManager()
    
    # [SoundManager 담당] 대기화면 음악 구동
    sound_manager.play_bgm("main")
