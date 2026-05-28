import pygame
import sys
import math

# 1. 초기화 및 상수가정
pygame.init()

# 화면 설정
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pulley & Gear Puzzle Prototype")

# FPS 및 시계 설정
FPS = 60
clock = pygame.time.Clock()

# 색상 정의 (RGB)
COLOR_BG = (30, 32, 40)       # 어두운 배경색
COLOR_GEAR = (212, 140, 60)   # 톱니바퀴 (구리/황동 느낌)
COLOR_PULLEY = (100, 149, 237) # 도르레 (강철/블루 느낌)
COLOR_ROPE = (220, 220, 210)   # 줄/프레임
COLOR_TEXT = (255, 255, 255)

# 게임 상태 변수들
gear_angle = 0.0
gear_speed = 2.0  # 초당 회전 각도 (도 단위)

# 메인 게임 루프
running = True
while running:
    # --- 2. 이벤트 처리 (Input) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # --- 3. 게임 상태 업데이트 (Update) ---
    # 톱니바퀴 회전 각도 누적
    gear_angle = (gear_angle + gear_speed) % 360
    
    # 마우스 좌표 얻기 (움직 도르레의 위치로 가상 활용)
    mouse_pos = pygame.mouse.get_pos()

    # --- 4. 화면 그리기 (Render/Draw) ---
    screen.fill(COLOR_BG)

    # [오브젝트 1] 고정된 톱니바퀴 (중앙 좌측)
    gear_center = (400, 384)
    gear_radius = 60
    pygame.draw.circle(screen, COLOR_GEAR, gear_center, gear_radius, 4)
    
    # 톱니바퀴 회전을 시각적으로 보여주기 위한 가이드선 (스포크)
    rad = math.radians(gear_angle)
    line_end_x = gear_center[0] + gear_radius * math.cos(rad)
    line_end_y = gear_center[1] + gear_radius * math.sin(rad)
    pygame.draw.line(screen, COLOR_GEAR, gear_center, (line_end_x, line_end_y), 4)

    # [오브젝트 2] 마우스를 따라다니는 도르레
    pulley_radius = 30
    pygame.draw.circle(screen, COLOR_PULLEY, mouse_pos, pulley_radius, 4)
    pygame.draw.circle(screen, COLOR_PULLEY, mouse_pos, 5) # 중심축

    # [오브젝트 3] 두 장치를 연결하는 줄 (Rope)
    # 실제 게임에서는 접선(Tangent)을 계산해야 하지만, 구조 확인을 위해 중심을 연결
    pygame.draw.line(screen, COLOR_ROPE, gear_center, mouse_pos, 2)

    # 안내 텍스트 출력
    font = pygame.font.SysFont("malgungothic", 20) # 윈도우 기본 맑은고딕 활용
    text_surface = font.render("마우스를 움직여 도르레 위치를 조절하세요. (ESC: 종료)", True, COLOR_TEXT)
    screen.blit(text_surface, (20, 20))

    # 화면 업데이트 (버퍼 플립)
    pygame.display.flip()

    # 프레임 레이트 고정
    clock.tick(FPS)

# 게임 종료 처리
pygame.quit()
sys.exit()