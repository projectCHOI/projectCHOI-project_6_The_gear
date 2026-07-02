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

        player_controller.update(puzzle_manager.gears)
        puzzle_manager.update(dt)

        screen.fill(COLOR_BG)
        puzzle_manager.draw(screen)

        level_text = font.render(f"STAGE {puzzle_manager.current_level} : 우물 속의 열쇠", True, COLOR_TEXT)
        screen.blit(level_text, (30, 30))
        
        if puzzle_manager.is_cleared:
            if not clear_sound_played:
                sound_manager.stop_bgm()           
                sound_manager.play_effect("clear") 
                clear_sound_played = True
                
            clear_text = font.render("🎉 STAGE CLEAR! (ESC를 눌러 종료)", True, (100, 255, 100))
            screen.blit(clear_text, (1280 // 2 - 180, 50))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
