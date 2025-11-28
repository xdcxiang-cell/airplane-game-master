"""Load and hold pygame surfaces used across the game."""

from dataclasses import dataclass

import pygame


@dataclass(slots=True)
class GameAssets:
    # Hero assets
    hero: pygame.Surface
    hero_blowup: list[pygame.Surface]
    
    # Hero bullets
    bullet: pygame.Surface
    
    # Enemy assets
    enemy_small: pygame.Surface
    enemy_medium: pygame.Surface
    enemy_large: pygame.Surface
    
    # Enemy explosions
    enemy_small_explosion: list[pygame.Surface]
    enemy_medium_explosion: list[pygame.Surface]
    enemy_large_explosion: list[pygame.Surface]
    
    # Enemy bullets
    enemy_bullet_small: pygame.Surface
    enemy_bullet_medium: pygame.Surface
    enemy_bullet_large: pygame.Surface
    
    # Background
    background: pygame.Surface


def load_assets() -> GameAssets:
    """集中加载所有图片资源，避免重复 IO。"""
    # Load hero explosion frames
    hero_blowup = [
        pygame.image.load("./feiji/hero_blowup_n1.png"),
        pygame.image.load("./feiji/hero_blowup_n2.png"),
        pygame.image.load("./feiji/hero_blowup_n3.png"),
        pygame.image.load("./feiji/hero_blowup_n4.png"),
    ]
    
    # Load enemy explosion frames
    enemy_small_explosion = [
        pygame.image.load("./feiji/enemy0_down1.png"),
        pygame.image.load("./feiji/enemy0_down2.png"),
        pygame.image.load("./feiji/enemy0_down3.png"),
        pygame.image.load("./feiji/enemy0_down4.png"),
    ]
    
    enemy_medium_explosion = [
        pygame.image.load("./feiji/enemy1_down1.png"),
        pygame.image.load("./feiji/enemy1_down2.png"),
        pygame.image.load("./feiji/enemy1_down3.png"),
        pygame.image.load("./feiji/enemy1_down4.png"),
    ]
    
    enemy_large_explosion = [
        pygame.image.load("./feiji/enemy2_down1.png"),
        pygame.image.load("./feiji/enemy2_down2.png"),
        pygame.image.load("./feiji/enemy2_down3.png"),
        pygame.image.load("./feiji/enemy2_down4.png"),
        pygame.image.load("./feiji/enemy2_down5.png"),
        pygame.image.load("./feiji/enemy2_down6.png"),
    ]
    
    return GameAssets(
        # Hero assets
        hero=pygame.image.load("./feiji/hero.gif"),
        hero_blowup=hero_blowup,
        
        # Hero bullets
        bullet=pygame.image.load("./feiji/bullet-3.gif"),
        
        # Enemy assets
        enemy_small=pygame.image.load("./feiji/enemy-1.gif"),
        enemy_medium=pygame.image.load("./feiji/enemy-2.gif"),
        enemy_large=pygame.image.load("./feiji/enemy-3.gif"),
        
        # Enemy explosions
        enemy_small_explosion=enemy_small_explosion,
        enemy_medium_explosion=enemy_medium_explosion,
        enemy_large_explosion=enemy_large_explosion,
        
        # Enemy bullets
        enemy_bullet_small=pygame.image.load("./feiji/bullet1.png"),
        enemy_bullet_medium=pygame.image.load("./feiji/bullet2.png"),
        enemy_bullet_large=pygame.image.load("./feiji/bullet.png"),
        
        # Background
        background=pygame.image.load("./feiji/background.png"),
    )

