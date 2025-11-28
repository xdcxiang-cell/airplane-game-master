"""Centralised constants for game configuration."""

import pygame

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 650
SCREEN_RECT = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

# Gameplay constants
HERO_SPEED = 60
HERO_INITIAL_HP = 5
HERO_INVINCIBLE_DURATION = 180  # Frames of invincibility after being hit

# Enemy constants
ENEMY_TYPES = {
    "small": {"speed": 40, "health": 1, "score": 100, "shoot_odds": (10, 20)},  # Fast, weak, low score
    "medium": {"speed": 30, "health": 3, "score": 300, "shoot_odds": (50, 60)},  # Medium speed, medium health
    "large": {"speed": 20, "health": 5, "score": 500, "shoot_odds": (80, 90)}   # Slow, strong, high score
}

ENEMY_SPAWN_RATE = 120  # Spawn new enemy every 2 seconds at 60 FPS

# Bullet constants
HERO_BULLET_SPEED = 120
ENEMY_BULLET_SPEED = 90

# Display constants
FPS = 60
FONT_SIZE = 24
FONT_COLOR = (255, 255, 255)
FONT_SHADOW_COLOR = (0, 0, 0)

