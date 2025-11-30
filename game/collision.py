"""Collision helpers between hero/enemy entities."""

from .enemy import EnemyPlane
from .hero import HeroPlane


def handle_collisions(hero: HeroPlane, enemies: list[EnemyPlane]) -> None:
    """检测敌我子弹碰撞, 并触发相应效果。"""
    for enemy in enemies:
        if enemy.is_blowing_up:
            continue

        # Hero bullets hitting enemy
        for bullet in list(hero.bullets):
            if bullet.rect.colliderect(enemy.rect):
                hero.bullets.remove(bullet)
                enemy.take_damage()
                if enemy.hp <= 0:
                    hero.add_score(enemy.score)
                break

        # Enemy bullets hitting hero
        for bullet in list(enemy.bullets):
            if bullet.rect.colliderect(hero.rect):
                hero.take_damage()
                enemy.bullets.remove(bullet)
                break

