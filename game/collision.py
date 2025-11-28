"""Collision helpers between hero/enemy entities."""

from .enemy import EnemyPlane
from .hero import HeroPlane


def handle_collisions(hero: HeroPlane, enemy: EnemyPlane) -> None:
    """检测敌我子弹碰撞, 并触发相应效果。"""
    for bullet in list(hero.bullets):
        if bullet.rect.colliderect(enemy.rect):
            hero.bullets.remove(bullet)
            enemy.reset_position()
            break

    for bullet in list(enemy.bullets):
        if bullet.rect.colliderect(hero.rect):
            hero.bomb()
            enemy.bullets.remove(bullet)
            break

