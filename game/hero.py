"""Hero plane implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from . import constants
from .bullet import Bullet

if TYPE_CHECKING:
    from .assets import GameAssets


class HeroPlane:
    """玩家飞机类，处理玩家飞机的显示、移动、射击和生命值/护盾系统。"""
    
    def __init__(self, screen: pygame.Surface, assets: "GameAssets") -> None:
        """初始化玩家飞机。"""
        self.screen = screen
        self.assets = assets
        self.image = assets.hero
        # 初始位置：屏幕底部中央
        self.x = constants.SCREEN_WIDTH // 2 - self.image.get_width() // 2
        self.y = constants.SCREEN_HEIGHT - self.image.get_height() - 20
        # 玩家子弹列表
        self.bullets: list[Bullet] = []
        
        # 生命值和护盾系统
        self.lives = constants.INITIAL_LIVES  # 初始生命值
        self.shield = True  # 初始有护盾
        self.shield_health = 2  # 护盾能承受2次攻击
        self.max_shield_health = 2  # 最大护盾值
        self.hit = False  # 是否被击中
        self.bomb_frames = assets.hero_blowup  # 爆炸动画帧
        self.frame_counter = 0  # 爆炸动画帧计数器
        self.bomb_frame_index = 0  # 当前爆炸动画帧索引
        
        # 击杀计数（用于恢复护盾）
        self.kill_count = 0
        
        # 积分
        self.score = 0

    @property
    def rect(self) -> pygame.Rect:
        """获取玩家飞机的碰撞矩形。"""
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def take_damage(self) -> None:
        """受到伤害，先消耗护盾，再消耗生命。"""
        if self.shield:
            self.shield_health -= 1
            if self.shield_health <= 0:
                self.shield = False  # 护盾被打破
        else:
            self.lives -= 1
            if self.lives <= 0:
                self.hit = True  # 玩家被击中

    def increase_kill_count(self) -> None:
        """增加击杀计数，每击杀5个敌人恢复护盾。"""
        self.kill_count += 1
        if self.kill_count % constants.SHIELD_RESTORE_KILLS == 0:
            # 恢复护盾
            self.shield = True
            self.shield_health = self.max_shield_health

    def increase_score(self, points: int) -> None:
        """增加积分。"""
        self.score += points

    def display(self) -> None:
        """显示玩家飞机和子弹。"""
        if self.hit:
            # 播放爆炸动画
            self.screen.blit(self.bomb_frames[self.bomb_frame_index], (self.x, self.y))
            self.frame_counter += 1
            # 控制爆炸动画播放速度
            if self.frame_counter == 7:
                self.frame_counter = 0
                self.bomb_frame_index += 1
            # 爆炸动画播放完毕，游戏结束
            if self.bomb_frame_index >= len(self.bomb_frames):
                font = pygame.font.Font(None, 72)
                text = font.render("游戏结束", True, (255, 0, 0))
                self.screen.blit(text, (constants.SCREEN_WIDTH//2 - text.get_width()//2, constants.SCREEN_HEIGHT//2 - text.get_height()//2))
                pygame.display.update()
                pygame.time.wait(2000)
                pygame.quit()
                raise SystemExit
        else:
            # 显示玩家飞机
            self.screen.blit(self.image, (self.x, self.y))
            
            # 显示护盾（如果有）
            if self.shield:
                self._draw_shield()
        
        # 显示和移动子弹
        for bullet in list(self.bullets):
            bullet.display()
            bullet.move()
            # 移除屏幕外的子弹
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

    def move_left(self) -> None:
        """向左移动玩家飞机。"""
        if not self.hit and self.x > constants.SCREEN_RECT.left:
            self.x = max(self.x - constants.HERO_SPEED, constants.SCREEN_RECT.left)

    def move_right(self) -> None:
        """向右移动玩家飞机。"""
        if not self.hit:
            max_x = constants.SCREEN_RECT.right - self.image.get_width()
            if self.x < max_x:
                self.x = min(self.x + constants.HERO_SPEED, max_x)

    def shoot(self, shoot_effect: pygame.mixer.Sound = None) -> None:
        """发射子弹，并播放射击音效（如果提供）。"""
        if not self.hit:
            # 创建子弹并添加到子弹列表
            self.bullets.append(Bullet(self.x, self.y, self.screen, self.assets.bullet))
            # 播放射击音效
            if shoot_effect:
                shoot_effect.play()

    def _draw_shield(self) -> None:
        """绘制玩家护盾，包括外圈和闪烁的内圈。"""
        # 计算护盾半径（比飞机稍大）
        shield_radius = max(self.image.get_width(), self.image.get_height()) // 2 + 10
        center_x = self.x + self.image.get_width() // 2
        center_y = self.y + self.image.get_height() // 2
        
        # 绘制护盾外圈（蓝色）
        pygame.draw.circle(self.screen, (0, 255, 255), (center_x, center_y), shield_radius, 2)
        
        # 绘制护盾内圈（闪烁效果）
        if self.frame_counter % 30 < 15:
            pygame.draw.circle(self.screen, (0, 255, 255), (center_x, center_y), shield_radius - 5, 1)

