"""Collision helpers between hero/enemy entities."""

from typing import List
from .enemy import EnemyPlane
from .hero import HeroPlane


def handle_collisions(hero: HeroPlane, enemies: List[EnemyPlane]) -> None:
    """检测敌我子弹碰撞, 并触发相应效果。"""
    # Handle hero bullets hitting enemies
    for bullet in list(hero.bullets):
        for enemy in enemies:
            if not enemy.destroyed and bullet.rect.colliderect(enemy.rect):
                # Remove bullet
                hero.bullets.remove(bullet)
                
                # Damage enemy
                enemy.take_damage()
                
                # Add score if enemy is destroyed
                if enemy.destroyed:
                    hero.add_score(enemy.score_value)
                break

    # Handle enemy bullets hitting hero
    for enemy in enemies:
        for bullet in list(enemy.bullets):
            if not hero.hit and bullet.rect.colliderect(hero.rect):
                # Damage hero
                hero.take_damage()
                
                # Remove bullet
                enemy.bullets.remove(bullet)
                break

