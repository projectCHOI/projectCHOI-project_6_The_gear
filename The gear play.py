

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# 1. 초기화 및 기본 설정
pygame.init()
pygame.mixer.init()  # 사운드 시스템 초기화

# 화면 크기 설정 (톱니바퀴 퍼즐에 적합한 16:9 해상도)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Gear : The Puzzler")

# 2. 게임 상태 및 프레임 제어 시간 설정
clock = pygame.time.Clock()
FPS = 60  # 초당 60프레임 고정

# 색상 정의 (RGB 방식)
COLOR_BG = (30, 30, 35)       # 어두운 스팀 펑크 풍의 배경색
COLOR_WHITE = (255, 255, 255)

def main():
    running = True
# 3. 메인 게임 루프 시작
    while running:
        # 프레임 제한 (60 FPS)
        # delta_time은 나중에 프레임 독립적인 회전 애니메이션을 구현할 때 사용됩니다.
        dt = clock.tick(FPS) / 1000.0 

        # A. 이벤트 핸들링 (입력 처리)
        for event in pygame.event.get():
            # 게임 종료 이벤트 (우측 상단 X 버튼 클릭)
            if event.type == pygame.QUIT:
                running = False
            
            # 키보드 입력 처리
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESC 누르면 종료
                    running = False

            # 마우스 클릭/드래그 이벤트는 나중에 src/player.py에서 처리하여 연결할 예정입니다.

        # B. 게임 상태 업데이트 (로직 처리)
        # TODO: 톱니바퀴들의 회전각 계산, 퍼즐 정답 판정 등을 여기에 연결할 예정입니다.

        # C. 화면 그리기 (렌더링)
        screen.fill(COLOR_BG)  # 배경을 어두운 색으로 먼저 채우기

        # TODO: 톱니바퀴 스프라이트, UI, 한글 텍스트(서평원 꺾깎체) 등을 여기에 그릴 예정입니다.

        # 최종적으로 그린 화면을 모니터에 반영
        pygame.display.flip()

    # 루프 탈출 시 게임 안전하게 종료
        pygame.quit()
        sys.exit()
        dt = clock.tick(FPS) / 1000.0 

        # A. 이벤트 핸들링 (입력 처리)
        for event in pygame.event.get():
            # 게임 종료 이벤트 (우측 상단 X 버튼 클릭)
            if event.type == pygame.QUIT:
                running = False

    # 루프 탈출 시 게임 안전하게 종료
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
