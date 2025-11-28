"""Load and hold pygame surfaces used across the game."""

from dataclasses import dataclass

import pygame


@dataclass(slots=True)
class GameAssets:
    hero: pygame.Surface
    hero_blowup: list[pygame.Surface]
    bullet: pygame.Surface
    enemies: list[pygame.Surface]
    enemy_bullet: pygame.Surface
    enemy_explosions: list[list[pygame.Surface]]  # Explosion animations for different enemy types
    background: pygame.Surface


def load_assets() -> GameAssets:
    """集中加载所有图片资源，避免重复 IO。"""
    hero_blowup = [
        pygame.image.load("./feiji/hero_blowup_n1.png"),
        pygame.image.load("./feiji/hero_blowup_n2.png"),
        pygame.image.load("./feiji/hero_blowup_n3.png"),
        pygame.image.load("./feiji/hero_blowup_n4.png"),
    ]
    
    # Load enemy sprites
    enemies = [
        pygame.image.load("./feiji/enemy-1.gif"),
        pygame.image.load("./feiji/enemy-2.gif"),
        pygame.image.load("./feiji/enemy-3.gif"),
    ]
    
    # Load enemy explosion animations
    enemy_explosions = [
        # Enemy 0 explosion
        [
            pygame.image.load("./feiji/enemy0_down1.png"),
            pygame.image.load("./feiji/enemy0_down2.png"),
            pygame.image.load("./feiji/enemy0_down3.png"),
            pygame.image.load("./feiji/enemy0_down4.png"),
        ],
        # Enemy 1 explosion
        [
            pygame.image.load("./feiji/enemy1_down1.png"),
            pygame.image.load("./feiji/enemy1_down2.png"),
            pygame.image.load("./feiji/enemy1_down3.png"),
            pygame.image.load("./feiji/enemy1_down4.png"),
        ],
        # Enemy 2 explosion
        [
            pygame.image.load("./feiji/enemy2_down1.png"),
            pygame.image.load("./feiji/enemy2_down2.png"),
            pygame.image.load("./feiji/enemy2_down3.png"),
            pygame.image.load("./feiji/enemy2_down4.png"),
            pygame.image.load("./feiji/enemy2_down5.png"),
            pygame.image.load("./feiji/enemy2_down6.png"),
        ],
    ]
    
    return GameAssets(
        hero=pygame.image.load("./feiji/hero.gif"),
        hero_blowup=hero_blowup,
        bullet=pygame.image.load("./feiji/bullet-3.gif"),
        enemies=enemies,
        enemy_bullet=pygame.image.load("./feiji/bullet1.png"),
        enemy_explosions=enemy_explosions,
        background=pygame.image.load("./feiji/background.png"),
    )

