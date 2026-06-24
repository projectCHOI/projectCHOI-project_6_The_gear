import pygame
import sys
import os

# 1. 시스템 경로 등록 규칙 유지
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'assets', 'music'))

from stage import PuzzleManager
from player import PlayerController
from sound_manager import SoundManager

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
    # 대기화면 음악을 먼저 켜고 싶다면 "main"
    # 바로 인게임 음악을 켜고 싶다면 "play"
    sound_manager.play_bgm("main")
    
    # 효과음 중복 재생 방지용 플래그
    clear_sound_played = False
    fail_sound_played = False    
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
            
            # 마우스 클릭으로 톱니바퀴를 잡는 이벤트 순간 감시
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # 톱니바퀴를 붙잡았는지 체크하기 전 개수 백업
                player_controller.handle_event(event, puzzle_manager.gears)
                if player_controller.is_dragging:
                    # 성공적으로 톱니를 조작하기 시작하면 설치/체결 효과음 재생
                    sound_manager.play_effect("install")

        player_controller.update(puzzle_manager.gears)
        puzzle_manager.update(dt)
        screen.fill((30, 30, 35))
        puzzle_manager.draw(screen)

        level_text = font.render(f"STAGE {puzzle_manager.current_level} : 우물 속의 열쇠", True, (220, 220, 220))
        screen.blit(level_text, (30, 30))
        
        # 스테이지가 클리어된 순간 딱 한 번만 클리어 음악 재생
        if puzzle_manager.is_cleared:
            if not clear_sound_played:
                sound_manager.stop_bgm()           # 배경음악을 끄고
                sound_manager.play_effect("clear") # 클리어 음악 분출
                clear_sound_played = True
                
            clear_text = font.render("🎉 STAGE CLEAR! (ESC를 눌러 종료)", True, (100, 255, 100))
            screen.blit(clear_text, (SCREEN_WIDTH // 2 - 180, 50))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
