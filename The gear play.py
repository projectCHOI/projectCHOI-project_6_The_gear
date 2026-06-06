import pygame
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
