"""Collision helpers between hero/enemy entities."""

from .enemy import EnemyPlane
from .hero import HeroPlane
from typing import List


def handle_collisions(hero: HeroPlane, enemies: List[EnemyPlane]) -> None:
    """检测敌我子弹碰撞, 并触发相应效果。"""
    # Check hero bullets hitting enemies
    for bullet in list(hero.bullets):
        for enemy in list(enemies):
            if enemy.is_alive and bullet.rect.colliderect(enemy.rect):
                # Enemy takes damage
                enemy.take_damage()
                
                # Remove bullet
                if bullet in hero.bullets:
                    hero.bullets.remove(bullet)
                
                # If enemy is destroyed, add score to hero
                if not enemy.is_alive:
                    hero.add_score(enemy.score_value)
                
                # Each bullet can hit only one enemy
                break
    
    # Check enemy bullets hitting hero
    for enemy in list(enemies):
        for bullet in list(enemy.bullets):
            if not hero.hit and bullet.rect.colliderect(hero.rect):
                # Hero takes damage
                hero.take_damage()
                
                # Remove bullet
                if bullet in enemy.bullets:
                    enemy.bullets.remove(bullet)
                
                # Hero can be hit by multiple bullets, but only one per frame
                break

