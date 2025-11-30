"""Load and hold pygame surfaces used across the game."""

from dataclasses import dataclass

import pygame


@dataclass
class GameAssets:
    hero: pygame.Surface
    hero_blowup: list[pygame.Surface]
    bullet: pygame.Surface
    enemy1: pygame.Surface
    enemy1_blowup: list[pygame.Surface]
    enemy2: pygame.Surface
    enemy2_blowup: list[pygame.Surface]
    enemy3: pygame.Surface
    enemy3_blowup: list[pygame.Surface]
    enemy_bullet: pygame.Surface
    background: pygame.Surface
    # 音效文件
    main_music: str
    shoot_sound: str
    explosion_sound: str


def load_assets() -> GameAssets:
    """集中加载所有图片资源，避免重复 IO。"""
    hero_blowup = [
        pygame.image.load("./feiji/hero_blowup_n1.png"),
        pygame.image.load("./feiji/hero_blowup_n2.png"),
        pygame.image.load("./feiji/hero_blowup_n3.png"),
        pygame.image.load("./feiji/hero_blowup_n4.png"),
    ]
    
    # 敌机1爆炸动画
    enemy1_blowup = [
        pygame.image.load("./feiji/enemy1_down1.png"),
        pygame.image.load("./feiji/enemy1_down2.png"),
        pygame.image.load("./feiji/enemy1_down3.png"),
        pygame.image.load("./feiji/enemy1_down4.png"),
    ]
    
    # 敌机2爆炸动画
    enemy2_blowup = [
        pygame.image.load("./feiji/enemy2_down1.png"),
        pygame.image.load("./feiji/enemy2_down2.png"),
        pygame.image.load("./feiji/enemy2_down3.png"),
        pygame.image.load("./feiji/enemy2_down4.png"),
        pygame.image.load("./feiji/enemy2_down5.png"),
        pygame.image.load("./feiji/enemy2_down6.png"),
    ]
    
    # 敌机3爆炸动画（暂时使用敌机2的爆炸动画）
    enemy3_blowup = enemy2_blowup
    
    return GameAssets(
        hero=pygame.image.load("./feiji/hero.gif"),
        hero_blowup=hero_blowup,
        bullet=pygame.image.load("./feiji/bullet-3.gif"),
        enemy1=pygame.image.load("./feiji/enemy-1.gif"),
        enemy1_blowup=enemy1_blowup,
        enemy2=pygame.image.load("./feiji/enemy-2.gif"),
        enemy2_blowup=enemy2_blowup,
        enemy3=pygame.image.load("./feiji/enemy-3.gif"),
        enemy3_blowup=enemy3_blowup,
        enemy_bullet=pygame.image.load("./feiji/bullet1.png"),
        background=pygame.image.load("./feiji/background.png"),
        main_music="./feiji/main.mp3",
        shoot_sound="./feiji/shoot.mp3",
        explosion_sound="./feiji/explosion.mp3",
    )

