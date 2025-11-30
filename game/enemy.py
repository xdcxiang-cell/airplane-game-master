"""Enemy plane implementation."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING, Literal

import pygame

from . import constants
from .bullet import EnemyBullet

if TYPE_CHECKING:
    from .assets import GameAssets


EnemyType = Literal["enemy1", "enemy2", "enemy3"]


class EnemyPlane:
    """敌机类，处理敌机的显示、移动、射击和生命值系统。"""
    
    def __init__(self, screen: pygame.Surface, assets: "GameAssets", enemy_type: EnemyType = "enemy1") -> None:
        """初始化敌机，根据敌机类型设置不同属性。"""
        self.screen = screen
        self.assets = assets
        self.enemy_type = enemy_type  # 敌机类型
        self.bullets: list[EnemyBullet] = []  # 敌机子弹列表
        self.hit = False  # 是否被击中
        self.bomb_frame_index = 0  # 爆炸动画帧索引
        self.frame_counter = 0  # 爆炸动画帧计数器
        
        # 根据敌机类型设置属性
        if enemy_type == "enemy1":
            self.image = assets.enemy1
            self.blowup_frames = assets.enemy1_blowup
            self.speed = constants.ENEMY_SPEED
            self.health = 1
            self.max_health = 1
            self.points = 100
        elif enemy_type == "enemy2":
            self.image = assets.enemy2
            self.blowup_frames = assets.enemy2_blowup
            self.speed = constants.ENEMY_SPEED - 1
            self.health = 3
            self.max_health = 3
            self.points = 300
        elif enemy_type == "enemy3":
            self.image = assets.enemy3
            self.blowup_frames = assets.enemy3_blowup
            self.speed = constants.ENEMY_SPEED - 2
            self.health = 5
            self.max_health = 5
            self.points = 500
        
        # 初始位置：从屏幕外顶部随机位置进入
        self.x = random.randint(0, constants.SCREEN_WIDTH - self.image.get_width())
        self.y = -self.image.get_height()  # 从屏幕外顶部进入
        self.direction = "right"  # 初始移动方向

    @property
    def rect(self) -> pygame.Rect:
        """获取敌机的碰撞矩形。"""
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def display(self) -> None:
        """显示敌机、爆炸动画和子弹。"""
        if self.hit:
            # 播放爆炸动画（确保不越界）
            if self.bomb_frame_index < len(self.blowup_frames):
                self.screen.blit(self.blowup_frames[self.bomb_frame_index], (self.x, self.y))
                self.frame_counter += 1
                # 控制爆炸动画播放速度
                if self.frame_counter == 7:
                    self.frame_counter = 0
                    self.bomb_frame_index += 1
        else:
            # 显示敌机
            self.screen.blit(self.image, (self.x, self.y))
            
            # 显示血条
            self._draw_health_bar()
            
            # 显示和移动子弹
            for bullet in list(self.bullets):
                bullet.display()
                bullet.move()
                # 移除屏幕外的子弹
                if bullet.is_off_screen():
                    self.bullets.remove(bullet)

    def move(self) -> None:
        """移动敌机，左右移动并随机向下移动。"""
        if not self.hit:
            # 左右移动
            if self.direction == "right":
                self.x += self.speed
            else:
                self.x -= self.speed
            
            # 左右边界检测，碰到边界改变方向
            if self.x > constants.SCREEN_WIDTH - self.image.get_width():
                self.direction = "left"
            elif self.x < constants.SCREEN_RECT.left:
                self.direction = "right"
            
            # 随机向下移动（5%概率）
            if random.randint(1, 100) < 5:
                self.y += 10

    def shoot(self) -> None:
        """敌机射击，根据敌机类型有不同的射击概率。"""
        if not self.hit and random.randint(1, 100) < constants.ENEMY_SHOOT_ODDS[self.enemy_type]:
            self.bullets.append(EnemyBullet(self.x, self.y, self.screen, self.assets.enemy_bullet))

    def take_damage(self, damage: int = 1) -> bool:
        """受到伤害，返回是否被摧毁。"""
        if not self.hit:
            self.health -= damage
            if self.health <= 0:
                self.hit = True
                return True
        return False

    def is_destroyed(self) -> bool:
        """检查敌机是否已经完全爆炸。"""
        return self.hit and self.bomb_frame_index >= len(self.blowup_frames)

    def _draw_health_bar(self) -> None:
        """绘制敌机血条，显示当前生命值与最大生命值的比例。"""
        bar_width = self.image.get_width()
        bar_height = 5
        x = self.x
        y = self.y - 10  # 血条显示在敌机上方
        
        # 血条背景（红色）
        pygame.draw.rect(self.screen, (255, 0, 0), (x, y, bar_width, bar_height))
        
        # 血条进度（绿色）
        health_percent = self.health / self.max_health
        fill_width = int(bar_width * health_percent)
        pygame.draw.rect(self.screen, (0, 255, 0), (x, y, fill_width, bar_height))

