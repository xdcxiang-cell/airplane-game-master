"""Load and hold pygame surfaces used across the game."""

from dataclasses import dataclass

import pygame


@dataclass(slots=True)
class GameAssets:
    hero: pygame.Surface
    hero_blowup: list[pygame.Surface]
    bullet: pygame.Surface
    enemy: pygame.Surface
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
    return GameAssets(
        hero=pygame.image.load("./feiji/hero.gif"),
        hero_blowup=hero_blowup,
        bullet=pygame.image.load("./feiji/bullet-3.gif"),
        enemy=pygame.image.load("./feiji/enemy-1.gif"),
        enemy_bullet=pygame.image.load("./feiji/bullet1.png"),
        background=pygame.image.load("./feiji/background.png"),
    )

