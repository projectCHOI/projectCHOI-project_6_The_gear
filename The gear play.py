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
    sound_manager = SoundManager()
    music_manager = MusicManager()
    sound_manager.play_bgm("main")
    clear_sound_played = False
    font = pygame.font.SysFont("malgungothic", 28)
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                player_controller.handle_event(event, puzzle_manager.gears)
                if player_controller.is_dragging:
                    music_manager.play_install_sound()
