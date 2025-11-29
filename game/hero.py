"""Hero plane implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from . import constants
from .bullet import Bullet

if TYPE_CHECKING:
    from .assets import GameAssets


class HeroPlane:
    """
    英雄飞机类，处理玩家飞机的移动、射击、生命值、护盾和积分等逻辑。
    
    属性:
        screen: pygame.Surface - 游戏主屏幕
        assets: GameAssets - 游戏资源
        image: pygame.Surface - 英雄飞机图片
        x: int - 飞机X坐标
        y: int - 飞机Y坐标
        bullets: list[Bullet] - 玩家发射的子弹列表
        hit: bool - 飞机是否被击中
        bomb_frames: list[pygame.Surface] - 爆炸动画帧
        frame_counter: int - 动画帧计数器
        bomb_frame_index: int - 当前爆炸动画帧索引
        lives: int - 玩家生命值
        shield: bool - 玩家护盾状态
        score: int - 玩家积分
        kill_count: int - 击杀敌机数量
        font: pygame.font.Font - 显示文本的字体
    """
    
    def __init__(self, screen: pygame.Surface, assets: "GameAssets") -> None:
        """
        初始化英雄飞机
        
        参数:
            screen: pygame.Surface - 游戏主屏幕
            assets: GameAssets - 游戏资源
        """
        self.screen = screen
        self.assets = assets
        self.image = assets.hero
        self.x = constants.SCREEN_WIDTH // 2 - self.image.get_width() // 2
        self.y = constants.SCREEN_HEIGHT - self.image.get_height() - 20
        self.bullets: list[Bullet] = []
        self.hit = False
        self.bomb_frames = assets.hero_blowup
        self.frame_counter = 0
        self.bomb_frame_index = 0
        
        # 新添加的属性
        self.lives = constants.HERO_LIVES  # 玩家生命值
        self.shield = constants.HERO_SHIELD  # 玩家护盾状态
        self.score = 0  # 玩家积分
        self.kill_count = 0  # 击杀敌机数量
        # 使用支持中文的字体，这里尝试使用系统字体路径，不同系统可能需要调整
        try:
            # 尝试加载系统中的中文字体
            self.font = pygame.font.Font("/System/Library/Fonts/PingFang.ttc", constants.SCORE_FONT_SIZE)  # Mac系统
        except FileNotFoundError:
            try:
                self.font = pygame.font.Font("C:/Windows/Fonts/simsun.ttc", constants.SCORE_FONT_SIZE)  # Windows系统
            except FileNotFoundError:
                self.font = pygame.font.SysFont("SimHei", constants.SCORE_FONT_SIZE)  # 回退方案

    @property
    def rect(self) -> pygame.Rect:
        """获取飞机的矩形碰撞框"""
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def bomb(self) -> None:
        """触发飞机爆炸动画"""
        self.hit = True

    def display(self) -> None:
        """显示飞机、子弹、生命值、护盾和积分"""
        if self.hit:
            self.screen.blit(self.bomb_frames[self.bomb_frame_index], (self.x, self.y))
            self.frame_counter += 1
            if self.frame_counter == 7:
                self.frame_counter = 0
                self.bomb_frame_index += 1
            if self.bomb_frame_index >= len(self.bomb_frames):
                pygame.time.wait(1000)
                pygame.quit()
                raise SystemExit
        else:
            self.screen.blit(self.image, (self.x, self.y))
        for bullet in list(self.bullets):
            bullet.display()
            bullet.move()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)
        
        # 显示生命值、护盾和积分
        self.display_lives()
        self.display_shield()
        self.display_score()

    def move_left(self) -> None:
        """向左移动飞机"""
        if self.x > constants.SCREEN_RECT.left:
            self.x = max(self.x - constants.HERO_SPEED, constants.SCREEN_RECT.left)

    def move_right(self) -> None:
        """向右移动飞机"""
        max_x = constants.SCREEN_RECT.right - self.image.get_width()
        if self.x < max_x:
            self.x = min(self.x + constants.HERO_SPEED, max_x)

    def shoot(self) -> None:
        """发射子弹并播放音效"""
        if self.hit:
            return
        self.bullets.append(Bullet(self.x, self.y, self.screen, self.assets.bullet))
        # 播放发射子弹音效
        self.assets.shoot_sound.play()

    def display_lives(self) -> None:
        """显示玩家生命值（爱心图标）"""
        for i in range(self.lives):
            # 绘制爱心图标
            heart_rect = pygame.Rect(
                constants.HEART_LEFT_MARGIN + (constants.HEART_SIZE + constants.HEART_SPACING) * i,
                constants.HEART_TOP_MARGIN,
                constants.HEART_SIZE,
                constants.HEART_SIZE
            )
            # 绘制爱心（使用简单的多边形表示，后续可以替换为图片）
            pygame.draw.polygon(self.screen, constants.RED, [
                (heart_rect.centerx, heart_rect.centery - heart_rect.height//4),
                (heart_rect.left, heart_rect.top),
                (heart_rect.left, heart_rect.bottom - heart_rect.height//4),
                (heart_rect.centerx - heart_rect.width//4, heart_rect.bottom),
                (heart_rect.centerx + heart_rect.width//4, heart_rect.bottom),
                (heart_rect.right, heart_rect.bottom - heart_rect.height//4),
                (heart_rect.right, heart_rect.top)
            ])

    def display_shield(self) -> None:
        """显示玩家护盾状态"""
        if self.shield:
            shield_text = "护盾: 开启"
            text_surface = self.font.render(shield_text, True, constants.BLUE)
            self.screen.blit(text_surface, (constants.SHIELD_LEFT_MARGIN, constants.SHIELD_TOP_MARGIN))

    def display_score(self) -> None:
        """显示玩家积分，右对齐显示"""
        score_text = f"积分: {self.score}"
        text_surface = self.font.render(score_text, True, constants.WHITE)
        # 计算文本位置，使其右对齐
        text_rect = text_surface.get_rect()
        text_rect.topright = (constants.SCREEN_WIDTH - constants.SCORE_RIGHT_MARGIN, constants.SCORE_TOP_MARGIN)
        self.screen.blit(text_surface, text_rect)

    def hit_by_enemy(self) -> None:
        """处理玩家被敌机击中的情况
        
        如果有护盾，失去护盾；否则失去一条命，生命值为0时触发爆炸动画。
        """
        if self.shield:
            self.shield = False  # 失去护盾
        else:
            self.lives -= 1  # 失去一条命
            if self.lives <= 0:
                self.bomb()  # 游戏结束

    def add_kill(self, points: int = constants.SCORE_PER_ENEMY) -> None:
        """添加击杀敌机的积分和计数，并检查是否需要恢复护盾
        
        参数:
            points: int - 击杀敌机获得的积分，默认为SCORE_PER_ENEMY
        """
        self.score += points
        self.kill_count += 1
        # 检查是否需要恢复护盾（每击杀指定数量的敌机恢复一次）
        if self.kill_count % constants.SHIELD_RECOVERY_KILLS == 0:
            self.shield = True