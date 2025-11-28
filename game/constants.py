"""Centralised constants for game configuration."""

import pygame

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 650
SCREEN_RECT = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

# Hero configuration
HERO_SPEED = 8
HERO_INITIAL_HP = 5
HERO_SCORE_PER_ENEMY = 100

# Enemy configuration
ENEMY_SPEED = 5
ENEMY_INITIAL_HP = 3
ENEMY_TYPES = {
    'small': {'speed': 5, 'hp': 1, 'score': 100, 'size': (60, 50)},  # Small enemy
    'medium': {'speed': 4, 'hp': 3, 'score': 300, 'size': (80, 70)},  # Medium enemy
    'large': {'speed': 3, 'hp': 5, 'score': 500, 'size': (100, 90)}   # Large enemy
}
ENEMY_SHOOT_ODDS = (10, 20)
ENEMY_SPAWN_INTERVAL = 2000  # Milliseconds between enemy spawns
ENEMY_MAX_ON_SCREEN = 5  # Maximum number of enemies allowed on screen at once

# Bullet configuration
BULLET_SPEED = 18
ENEMY_BULLET_SPEED = 12

# Game configuration
FPS = 60
SCORE_FONT_SIZE = 32
SCORE_POSITION = (10, 10)
HP_POSITION = (10, 45)
HP_FONT_SIZE = 30
GAME_OVER_FONT_SIZE = 72
GAME_OVER_SCORE_FONT_SIZE = 48
BUTTON_FONT_SIZE = 48

# Language
DEFAULT_LANGUAGE = 'zh'
LANGUAGE_SWITCH_KEY = 'l'  # Key to switch between languages

