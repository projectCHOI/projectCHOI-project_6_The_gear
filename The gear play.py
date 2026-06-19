import pygame
import sys
import os

# src 폴더 내부의 모듈을 안전하게 불러오기 위한 경로 설정
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from stage import PuzzleManager
from player import PlayerController  # [★최종 조립] 플레이어 컨트롤러 추가

# 1. 초기화 및 기본 설정
pygame.init()
pygame.mixer.init()

# 화면 크기 설정
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Gear : The Puzzler")

# 2. 게임 상태 및 프레임 제어 시간 설정
clock = pygame.time.Clock()
FPS = 60

# 색상 정의
COLOR_BG = (30, 30, 35)
COLOR_TEXT = (220, 220, 220)

def main():
    """게임의 메인 루프를 담당하는 함수"""
    puzzle_manager = PuzzleManager()
    player_controller = PlayerController()  # [★최종 조립] 인스턴스 생성
    
    # 폰트 설정 (서평원 꺾깎체 파일 패스가 완성되기 전까지 쓸 시스템 기본 폰트 백업)
    font = pygame.font.SysFont("malgungothic", 28) # 윈도우 기본 맑은 고딕 임시 사용
    
    running = True
    print("Core 3.12 Engine & Game Components fully integrated!")

    # 3. 메인 게임 루프 시작
    while running:
        # 프레임 제한 및 delta time 계산
        dt = clock.tick(FPS) / 1000.0 

        # A. 이벤트 핸들링 (입력 처리)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
            # [★최종 조립] 마우스 클릭 입력을 플레이어 컨트롤러로 전달
            player_controller.handle_event(event, puzzle_manager.gears)

        # B. 게임 상태 업데이트 (로직 처리)
        # [★최종 조립] 마우스 드래그에 따른 동력원 회전 처리
        player_controller.update(puzzle_manager.gears)
        
        # 톱니바퀴 연쇄 회전 및 클리어 판정 계산
        puzzle_manager.update(dt)

        # C. 화면 그리기 (렌더링)
        screen.fill(COLOR_BG)

        # 퍼즐 매니저가 관리하는 모든 톱니바퀴들을 화면에 그립니다.
        puzzle_manager.draw(screen)

        # 기본 UI 정보 출력 (현재 스테이지 및 클리어 문구)
        level_text = font.render(f"STAGE {puzzle_manager.current_level} : 우물 속의 열쇠", True, COLOR_TEXT)
        screen.blit(level_text, (30, 30))
        
        if puzzle_manager.is_cleared:
            clear_text = font.render("🎉 STAGE CLEAR! (ESC를 눌러 종료)", True, (100, 255, 100))
            screen.blit(clear_text, (SCREEN_WIDTH // 2 - 180, 50))

        # 최종적으로 그린 화면을 모니터에 반영
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
