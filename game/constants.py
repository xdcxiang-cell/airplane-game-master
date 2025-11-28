"""Centralised constants for game configuration."""

import pygame

# Screen dimensions
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 650
SCREEN_RECT = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

# Movement speeds
HERO_SPEED = 8
BULLET_SPEED = 18
ENEMY_BULLET_SPEED = 12
FPS = 60

# Enemy settings
ENEMY_SPEEDS = [3, 5, 7]  # Speeds for different enemy types
ENEMY_SHOOT_ODDS = [(5, 10), (10, 20), (15, 25)]  # Shoot odds for different enemy types
ENEMY_MAX_COUNT = 3  # Maximum number of enemies on screen at once
ENEMY_SPAWN_RATE = 200  # Spawn a new enemy every X frames

# Health settings
HERO_MAX_HEALTH = 5
ENEMY_HEALTH = [1, 2, 3]  # Health for different enemy types

# Score settings
ENEMY_SCORE = [10, 20, 30]  # Score for different enemy types

