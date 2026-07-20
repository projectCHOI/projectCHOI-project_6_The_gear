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
