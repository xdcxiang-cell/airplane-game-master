"""Centralised constants for game configuration."""

import pygame

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 650
SCREEN_RECT = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

HERO_SPEED = 8
ENEMY_SPEED = 5
BULLET_SPEED = 18
ENEMY_BULLET_SPEED = 12
ENEMY_SHOOT_ODDS = {"enemy1": 10, "enemy2": 15, "enemy3": 20}
FPS = 60

# 游戏设置
INITIAL_LIVES = 5
SHIELD_RESTORE_KILLS = 5
SCORE_INCREMENT = 100
LIFE_ICON_SIZE = 30
SCORE_FONT_SIZE = 24
HEART_ICON_PATH = "./feiji/prop_type_1.png"  # 爱心图标
SHIELD_ICON_PATH = "./feiji/prop_type_0.png"  # 护盾图标

