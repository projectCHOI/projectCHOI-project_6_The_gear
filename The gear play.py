import pygame
import sys
import os

# Pylance 검사기와 파이썬 엔진 모두가 인식 가능한 패키지 절대 경로 임포트 규칙 기법
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
    
    # 대기화면 음악 구동
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
            
                elif event.key == pygame.K_SPACE and puzzle_manager.is_cleared:
                    next_level = puzzle_manager.current_level + 1
                    
                    # 최대 스테이지(5스테이지)를 초과하지 않았는지 체크
                    if next_level <= 5:
                        puzzle_manager.load_level(next_level)
                        # 사운드 상태 및 플래그 초기화 후 배경음 재시작
                        clear_sound_played = False
                        sound_manager.play_bgm("main") 
                    else:
                        print("모든 스테이지를 정복하셨습니다!")
        # 내부 로직 실시간 업데이트
        player_manager.update(dt)  # ◀ 내부에서 마우스 드래그와 애니메이션을 동시에 연산합니다.
        puzzle_manager.update(dt)

        screen.fill(COLOR_BG)
        
        # 렌더링 레이어 출력
        puzzle_manager.draw(screen)
        player_manager.draw(screen)

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

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
