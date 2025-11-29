"""Enemy plane implementation."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING, Optional

import pygame

from . import constants
from .bullet import EnemyBullet

if TYPE_CHECKING:
    from .assets import GameAssets


class EnemyPlane:
    """
    敌机类，处理敌机的移动、射击、生命值、血条显示和类型区分等逻辑。
    
    属性:
        screen: pygame.Surface - 游戏主屏幕
        assets: GameAssets - 游戏资源
        enemy_type: str - 敌机类型（type1/type2/type3）
        health: int - 敌机当前生命值
        max_health: int - 敌机最大生命值
        speed: int - 敌机移动速度
        points: int - 击杀敌机获得的积分
        image: pygame.Surface - 敌机图片
        x: int - 敌机X坐标
        y: int - 敌机Y坐标
        direction: str - 敌机移动方向（right/left）
        bullets: list[EnemyBullet] - 敌机发射的子弹列表
        is_alive: bool - 敌机是否存活
        font: pygame.font.Font - 血条文本字体
    """
    
    def __init__(self, screen: pygame.Surface, assets: "GameAssets", enemy_type: str = "type1") -> None:
        """
        初始化敌机
        
        参数:
            screen: pygame.Surface - 游戏主屏幕
            assets: GameAssets - 游戏资源
            enemy_type: str - 敌机类型，默认为type1
        """
        self.screen = screen
        self.assets = assets
        
        # 敌机类型相关属性
        self.enemy_type = enemy_type
        self.health = constants.ENEMY_TYPES[enemy_type]["health"]  # 敌机生命值
        self.max_health = self.health  # 敌机最大生命值
        self.speed = constants.ENEMY_TYPES[enemy_type]["speed"]  # 敌机速度
        self.points = constants.ENEMY_TYPES[enemy_type]["points"]  # 敌机积分
        
        # 根据敌机类型选择图片
        if enemy_type == "type1":
            self.image = assets.enemy
        elif enemy_type == "type2":
            self.image = assets.enemy2
        elif enemy_type == "type3":
            self.image = assets.enemy3
        else:
            self.image = assets.enemy  # 默认类型1
        
        self.x = random.randint(0, constants.SCREEN_WIDTH - self.image.get_width())
        self.y = 20
        self.direction = "right"
        self.bullets: list[EnemyBullet] = []
        self.is_alive = True  # 敌机是否存活
        # 使用支持中文的字体，这里尝试使用系统字体路径，不同系统可能需要调整
        try:
            # 尝试加载系统中的中文字体
            self.font = pygame.font.Font("/System/Library/Fonts/PingFang.ttc", 14)  # Mac系统
        except FileNotFoundError:
            try:
                self.font = pygame.font.Font("C:/Windows/Fonts/simsun.ttc", 14)  # Windows系统
            except FileNotFoundError:
                self.font = pygame.font.SysFont("SimHei", 14)  # 回退方案

    @property
    def rect(self) -> pygame.Rect:
        """获取敌机的矩形碰撞框"""
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def display(self) -> None:
        """显示敌机、血条和子弹"""
        if self.is_alive:
            self.screen.blit(self.image, (self.x, self.y))
            # 显示血条
            self.display_health_bar()
            
            # 显示子弹
            for bullet in list(self.bullets):
                bullet.display()
                bullet.move()
                if bullet.is_off_screen():
                    self.bullets.remove(bullet)

    def move(self) -> None:
        """敌机左右移动，边界检测并改变方向"""
        if not self.is_alive:
            return
            
        if self.direction == "right":
            self.x += self.speed
        else:
            self.x -= self.speed
        
        # 边界检测
        if self.x > constants.SCREEN_WIDTH - self.image.get_width():
            self.direction = "left"
            self.x = constants.SCREEN_WIDTH - self.image.get_width()
        elif self.x < 0:
            self.direction = "right"
            self.x = 0

    def shoot(self) -> None:
        """敌机随机发射子弹"""
        if not self.is_alive:
            return
            
        random_num = random.randint(1, 100)
        if random_num in constants.ENEMY_SHOOT_ODDS:
            self.bullets.append(EnemyBullet(self.x, self.y, self.screen, self.assets.enemy_bullet))

    def reset_position(self) -> None:
        """重置敌机位置、状态和生命值"""
        self.x = random.randint(0, constants.SCREEN_WIDTH - self.image.get_width())
        self.y = 20
        self.direction = "right"
        self.bullets.clear()
        self.health = self.max_health
        self.is_alive = True

    def take_damage(self, damage: int = 1) -> None:
        """处理敌机受到伤害，生命值减少到0时标记为死亡并播放爆炸音效
        
        参数:
            damage: int - 受到的伤害值，默认为1
        """
        self.health -= damage
        if self.health <= 0:
            self.is_alive = False
            # 播放爆炸音效
            self.assets.explosion_sound.play()

    def display_health_bar(self) -> None:
        """显示敌机血条，包括背景、前景和生命值文本"""
        if self.health <= 0:
            return
            
        # 血条背景
        bar_width = self.image.get_width()
        bar_height = 5
        background_rect = pygame.Rect(self.x, self.y - bar_height - 2, bar_width, bar_height)
        pygame.draw.rect(self.screen, constants.RED, background_rect)
        
        # 血条前景
        health_ratio = self.health / self.max_health
        foreground_width = int(bar_width * health_ratio)
        foreground_rect = pygame.Rect(self.x, self.y - bar_height - 2, foreground_width, bar_height)
        pygame.draw.rect(self.screen, constants.GREEN, foreground_rect)
        
        # 显示生命值文本
        health_text = f"{self.health}/{self.max_health}"
        text_surface = self.font.render(health_text, True, constants.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.centerx = self.x + self.image.get_width() // 2
        text_rect.top = self.y - bar_height - 2 - text_rect.height
        self.screen.blit(text_surface, text_rect)