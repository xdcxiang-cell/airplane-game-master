"""Centralised constants for game configuration."""

import pygame

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 650
SCREEN_RECT = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

HERO_SPEED = 15
ENEMY_SPEED = 5
BULLET_SPEED = 18
ENEMY_BULLET_SPEED = 12
ENEMY_SHOOT_ODDS = (10, 20)
FPS = 60

# Health and score constants
HERO_MAX_HP = 5
ENEMY_MAX_HP = 3
ENEMY_SCORE = 100

# UI constants
FONT_SIZE = 24
UI_MARGIN = 10
UI_COLOR = (255, 255, 255)
UI_BACKGROUND = (0, 0, 0, 128)

