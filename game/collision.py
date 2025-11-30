"""Collision helpers between hero/enemy entities."""

import pygame

from .enemy import EnemyPlane
from .hero import HeroPlane


def handle_collisions(hero: HeroPlane, enemies: list[EnemyPlane], explosion_effect: pygame.mixer.Sound = None) -> None:
    """检测敌我子弹碰撞，并触发相应效果（如伤害、积分增加和爆炸音效）。"""
    # 玩家子弹与敌机碰撞检测
    for bullet in list(hero.bullets):
        for enemy in list(enemies):
            # 只有当敌机未被击中且子弹与敌机碰撞时才处理
            if not enemy.hit and bullet.rect.colliderect(enemy.rect):
                # 移除玩家子弹（已命中目标）
                hero.bullets.remove(bullet)
                # 敌机受到伤害，返回是否被摧毁
                if enemy.take_damage():
                    # 敌机被摧毁，增加玩家击杀计数和积分
                    hero.increase_kill_count()
                    hero.increase_score(enemy.points)
                    # 播放爆炸音效（如果提供）
                    if explosion_effect:
                        explosion_effect.play()
                break  # 一个子弹只能击中一个敌机

    # 敌机子弹与玩家碰撞检测
    for enemy in list(enemies):
        for bullet in list(enemy.bullets):
            # 只有当玩家未被击中且子弹与玩家碰撞时才处理
            if not hero.hit and bullet.rect.colliderect(hero.rect):
                # 移除敌机子弹（已命中目标）
                enemy.bullets.remove(bullet)
                # 玩家受到伤害
                hero.take_damage()
                break  # 一个子弹只能击中一个玩家

