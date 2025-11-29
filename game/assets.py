"""Load and hold pygame surfaces and sounds used across the game."""

from dataclasses import dataclass

import pygame
import numpy as np
import pygame.sndarray


@dataclass
class GameAssets:
    hero: pygame.Surface
    hero_blowup: list[pygame.Surface]
    bullet: pygame.Surface
    enemy: pygame.Surface
    enemy1: pygame.Surface
    enemy_bullet: pygame.Surface
    enemy_bullet1: pygame.Surface
    background: pygame.Surface
    shoot_sound: pygame.mixer.Sound
    explode_sound: pygame.mixer.Sound
    game_over_sound: pygame.mixer.Sound


def load_assets() -> GameAssets:
    """集中加载所有图片和声音资源，避免重复 IO。"""
    hero_blowup = [
        pygame.image.load("./feiji/hero_blowup_n1.png"),
        pygame.image.load("./feiji/hero_blowup_n2.png"),
        pygame.image.load("./feiji/hero_blowup_n3.png"),
        pygame.image.load("./feiji/hero_blowup_n4.png"),
    ]
    
    # Generate simple sound effects using pygame.sndarray
    shoot_sound = None
    explode_sound = None
    game_over_sound = None
    try:
        import numpy as np
        import pygame.sndarray
        
        # Function to create sound using numpy arrays
        def create_sound(freq, duration):
            sample_rate = 22050
            num_samples = int(sample_rate * duration)
            
            # Generate sine wave
            t = np.linspace(0, duration, num_samples, endpoint=False)
            wave = np.sin(2 * np.pi * freq * t)
            
            # Convert to 16-bit PCM
            wave = (wave * 32767).astype(np.int16)
            
            return pygame.sndarray.make_sound(wave)
        
        # Create sounds
        shoot_sound = create_sound(440, 0.1)  # A4 note
        explode_sound = create_sound(880, 0.1)  # A5 note
        game_over_sound = create_sound(220, 0.2)  # A3 note
    except ImportError:
        print("警告：无法导入numpy或pygame.sndarray，游戏将没有声音效果。")
    except pygame.error as e:
        print(f"警告：无法创建音效，游戏将没有声音效果。错误：{e}")
    
    return GameAssets(
        hero=pygame.image.load("./feiji/hero.gif"),
        hero_blowup=hero_blowup,
        bullet=pygame.image.load("./feiji/bullet-3.gif"),
        enemy=pygame.image.load("./feiji/enemy-1.gif"),
        enemy1=pygame.image.load("./feiji/enemy1.png"),
        enemy_bullet=pygame.image.load("./feiji/bullet1.png"),
        enemy_bullet1=pygame.image.load("./feiji/bullet2.png"),
        background=pygame.image.load("./feiji/background.png"),
        shoot_sound=shoot_sound,
        explode_sound=explode_sound,
        game_over_sound=game_over_sound
    )