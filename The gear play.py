import pygame
import sys
import os

# src 폴더 내부의 모듈을 안전하게 불러오기 위한 경로 설정
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from stage import PuzzleManager

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

def main():
    """게임의 메인 루프를 담당하는 함수"""
    # [★추가] 퍼즐 매니저 객체 생성 (레벨 1을 자동으로 불러옵니다)
    puzzle_manager = PuzzleManager()
    
    running = True
    print("Core 3.12 Engine & Pygame initialized successfully!")

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

        # B. 게임 상태 업데이트 (로직 처리)
        # [★추가] 매 프레임마다 톱니바퀴들의 회전각을 계산하고 클리어 조건을 검사합니다.
        puzzle_manager.update(dt)

        # C. 화면 그리기 (렌더링)
        screen.fill(COLOR_BG)

        # [★추가] 퍼즐 매니저가 관리하는 모든 톱니바퀴들을 화면에 그립니다.
        puzzle_manager.draw(screen)

        # 최종적으로 그린 화면을 모니터에 반영
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()