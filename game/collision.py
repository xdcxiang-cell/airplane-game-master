"""Collision helpers between hero/enemy entities."""

from typing import List

from .enemy import EnemyPlane
from .hero import HeroPlane


def handle_collisions(hero: HeroPlane, enemies: List[EnemyPlane]) -> None:
    """检测敌我子弹碰撞, 并触发相应效果。"""
    # 处理英雄子弹击中敌人
    for bullet in list(hero.bullets):
        for enemy in list(enemies):
            if enemy.dead:
                continue
            if bullet.rect.colliderect(enemy.rect):
                hero.bullets.remove(bullet)
                enemy.take_damage(1)
                break

    # 处理敌人子弹击中英雄
    for enemy in list(enemies):
        if enemy.dead:
            continue
        for bullet in list(enemy.bullets):
            if bullet.rect.colliderect(hero.rect):
                hero.bomb()
                enemy.bullets.remove(bullet)
                break

    # 移除死亡敌人并添加分数
    for enemy in list(enemies):
        if enemy.dead:
            enemies.remove(enemy)
            hero.score += 10  # 杀死敌人加分

