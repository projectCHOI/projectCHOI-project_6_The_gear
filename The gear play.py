import pygame
import sys
import os

from assets.stage.puzzle import PuzzleManager
from assets.player.player_manager import PlayerManager
from assets.sounds.sound_manager import SoundManager
from assets.music.music_manager import MusicManager

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
    player_manager = PlayerManager(SCREEN_WIDTH, SCREEN_HEIGHT)
    sound_manager = SoundManager()
    music_manager = MusicManager()
    
    sound_manager.play_bgm("main")
    clear_sound_played = False
    font = pygame.font.SysFont("malgungothic", 28)
    sub_font = pygame.font.SysFont("malgungothic", 20)
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0 
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE and puzzle_manager.is_cleared:
                    next_level = puzzle_manager.current_level + 1
                    if next_level <= 5:
                        puzzle_manager.load_level(next_level)
                        clear_sound_played = False
                        sound_manager.play_bgm("main") 
                    else:
                        print("전체 캠페인 완수!")
            
            # 마우스 제어 감시 규칙 명형 분기
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # A. 톱니바퀴 연동 조작 시도 (상자가 닫혀있을 때만)
                if not puzzle_manager.is_box_open:
                    player_manager.handle_event(event, puzzle_manager.gears)
                    if player_manager.is_dragging:
                        music_manager.play_install_sound()
                
                # B. 서사 아이템 월드 클릭 스캔 연동
                interaction = puzzle_manager.handle_clicks(event.pos)
                if interaction == "get_key":
                    # 열쇠를 주우면 가방 데이터에 박아 넣고 효과음 믹싱 가능
                    player_manager.gain_gear_to_inventory("key_item", 1)
                    music_manager.play_install_sound() 
                elif interaction == "unlock_door":
                    # 문이 열리는 짜릿한 연출 효과음
                    pass

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                player_manager.handle_event(event, puzzle_manager.gears)
