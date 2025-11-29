"""Collision helpers between hero/enemy entities."""

from .enemy import EnemyPlane
from .hero import HeroPlane
from . import constants


def handle_collisions(hero: HeroPlane, enemies: list[EnemyPlane]) -> None:
    """检测敌我子弹碰撞, 并触发相应效果。"""
    # Check hero bullets against enemies
    for bullet in list(hero.bullets):
        for enemy in list(enemies):
            if bullet.rect.colliderect(enemy.rect) and not enemy.exploding:
                hero.bullets.remove(bullet)
                enemy.take_damage()
                if enemy.health <= 0:
                    hero.add_score(constants.ENEMY_SCORE[enemy.enemy_type])
                break

    # Check enemy bullets against hero
    for enemy in enemies:
        for bullet in list(enemy.bullets):
            if bullet.rect.colliderect(hero.rect) and not hero.hit:
                hero.take_damage()
                enemy.bullets.remove(bullet)
                break

