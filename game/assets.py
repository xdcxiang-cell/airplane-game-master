"""Load and hold pygame surfaces used across the game."""

from dataclasses import dataclass

import pygame


@dataclass
class GameAssets:
    """
    游戏资源数据类，包含所有图片和音频资源
    
    属性:
        hero: pygame.Surface - 英雄飞机图片
        hero_blowup: list[pygame.Surface] - 英雄爆炸动画帧
        bullet: pygame.Surface - 英雄子弹图片
        enemy: pygame.Surface - 1型敌机图片
        enemy2: pygame.Surface - 2型敌机图片
        enemy3: pygame.Surface - 3型敌机图片
        enemy_bullet: pygame.Surface - 敌机子弹图片
        background: pygame.Surface - 游戏背景图片
        shoot_sound: pygame.mixer.Sound - 射击音效
        explosion_sound: pygame.mixer.Sound - 爆炸音效
        main_music: pygame.mixer.Sound - 游戏主背景音乐
    """
    hero: pygame.Surface
    hero_blowup: list[pygame.Surface]
    bullet: pygame.Surface
    enemy: pygame.Surface
    enemy2: pygame.Surface
    enemy3: pygame.Surface
    enemy_bullet: pygame.Surface
    background: pygame.Surface
    shoot_sound: pygame.mixer.Sound
    explosion_sound: pygame.mixer.Sound
    main_music: pygame.mixer.Sound


def load_assets() -> GameAssets:
    """
    集中加载所有游戏资源，避免重复IO操作
    
    返回:
        GameAssets - 包含所有加载完成的游戏资源对象
    """
    # 加载英雄爆炸动画帧（共4帧）
    hero_blowup = [
        pygame.image.load("./feiji/hero_blowup_n1.png"),
        pygame.image.load("./feiji/hero_blowup_n2.png"),
        pygame.image.load("./feiji/hero_blowup_n3.png"),
        pygame.image.load("./feiji/hero_blowup_n4.png"),
    ]
    
    # 初始化音频系统并加载音效
    pygame.mixer.init()
    shoot_sound = pygame.mixer.Sound("./feiji/shoot.mp3")  # 射击音效
    explosion_sound = pygame.mixer.Sound("./feiji/explosion.mp3")  # 爆炸音效
    main_music = pygame.mixer.Sound("./feiji/main.mp3")  # 主背景音乐
    
    # 创建并返回GameAssets对象，包含所有加载的资源
    return GameAssets(
        hero=pygame.image.load("./feiji/hero.gif"),
        hero_blowup=hero_blowup,
        bullet=pygame.image.load("./feiji/bullet-3.gif"),
        enemy=pygame.image.load("./feiji/enemy-1.gif"),
        enemy2=pygame.image.load("./feiji/enemy-2.gif"),
        enemy3=pygame.image.load("./feiji/enemy-3.gif"),
        enemy_bullet=pygame.image.load("./feiji/bullet1.png"),
        background=pygame.image.load("./feiji/background.png"),
        shoot_sound=shoot_sound,
        explosion_sound=explosion_sound,
        main_music=main_music
    )