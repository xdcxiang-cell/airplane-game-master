"""Load and hold pygame surfaces used across the game."""

from dataclasses import dataclass

import pygame


@dataclass(slots=True)
class GameAssets:
    hero: pygame.Surface
    hero_blowup: list[pygame.Surface]
    bullet: pygame.Surface
    enemy: pygame.Surface
    enemy1: pygame.Surface
    enemy2: pygame.Surface
    enemy_blowup: list[list[pygame.Surface]]
    enemy_bullet: pygame.Surface
    background: pygame.Surface


def load_assets() -> GameAssets:
    """集中加载所有图片资源，避免重复 IO。"""
    hero_blowup = [
        pygame.image.load("./feiji/hero_blowup_n1.png"),
        pygame.image.load("./feiji/hero_blowup_n2.png"),
        pygame.image.load("./feiji/hero_blowup_n3.png"),
        pygame.image.load("./feiji/hero_blowup_n4.png"),
    ]
    enemy_blowup = [
        # Enemy 0 blowup frames
        [
            pygame.image.load("./feiji/enemy0_down1.png"),
            pygame.image.load("./feiji/enemy0_down2.png"),
            pygame.image.load("./feiji/enemy0_down3.png"),
            pygame.image.load("./feiji/enemy0_down4.png"),
        ],
        # Enemy 1 blowup frames
        [
            pygame.image.load("./feiji/enemy1_down1.png"),
            pygame.image.load("./feiji/enemy1_down2.png"),
            pygame.image.load("./feiji/enemy1_down3.png"),
            pygame.image.load("./feiji/enemy1_down4.png"),
        ],
        # Enemy 2 blowup frames
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
        enemy=pygame.image.load("./feiji/enemy-1.gif"),
        enemy1=pygame.image.load("./feiji/enemy-2.gif"),
        enemy2=pygame.image.load("./feiji/enemy-3.gif"),
        enemy_blowup=enemy_blowup,
        enemy_bullet=pygame.image.load("./feiji/bullet1.png"),
        background=pygame.image.load("./feiji/background.png"),
    )

