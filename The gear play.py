import pygame
import sys
import os

# [★최신 경로 반영] 각 제어 스크립트들이 흩어진 폴더 주소들을 명부에 등록합니다.
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'assets', 'sounds'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'assets', 'music'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'assets', 'player'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'assets', 'stage'))

# [★최신 이름 반영] 새롭게 정착된 위치에서 모듈들을 안전하게 불러옵니다.
from puzzle import PuzzleManager          # assets/stage/puzzle.py 에서 로드
from player import PlayerController       # assets/player/player.py 에서 로드
from player_manager import PlayerManager  # assets/player/player_manager.py 에서 로드
from sound_manager import SoundManager    # assets/sounds/sound_manager.py 에서 로드
from music_manager import MusicManager    # assets/music/music_manager.py 에서 로드

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
    
    # 플레이어의 이미지, 인벤토리, 재화를 관리할 매니저 인스턴스 생성
    player_manager = PlayerManager(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    sound_manager = SoundManager()
    music_manager = MusicManager()
    
    # [SoundManager] 대기화면 음악 구동
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
            
            # 마우스 클릭 감시
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                player_controller.handle_event(event, puzzle_manager.gears)
                if player_controller.is_dragging:
                    # [MusicManager] ⚙️ 톱니 조작 시 5개 효과음 중 무작위 출력
                    music_manager.play_install_sound()

        # 각 매니저들 상태 실시간 업데이트
        player_controller.update(puzzle_manager.gears)
        
        # 플레이어 매니저에게 현재 드래그 중인 상태(True/False)를 전달하여 애니메이션 연동
        player_manager.update(dt, player_controller.is_dragging)
        
        puzzle_manager.update(dt)

        # 렌더링 (그리기) 순서 제어
        screen.fill(COLOR_BG)
        
        # 1. 톱니바퀴들 그리기
        puzzle_manager.draw(screen)
        
        # 2. 플레이어 캐릭터 및 UI 그리기
        player_manager.draw(screen)

        level_text = font.render(f"STAGE {puzzle_manager.current_level} : 우물 속의 열쇠", True, COLOR_TEXT)
        screen.blit(level_text, (30, 30))
        
        # 스테이지 클리어 연출
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