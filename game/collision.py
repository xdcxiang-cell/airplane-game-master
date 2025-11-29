"""Collision helpers between hero/enemy entities."""

from .enemy import EnemyPlane
from .hero import HeroPlane


def handle_collisions(hero: HeroPlane, enemy: EnemyPlane) -> None:
    """
    处理英雄和敌机之间的子弹碰撞
    
    参数:
        hero: HeroPlane - 英雄飞机对象
        enemy: EnemyPlane - 敌机对象
    """
    # 英雄子弹击中敌机：遍历英雄子弹，检测是否与敌机碰撞
    for bullet in list(hero.bullets):
        if enemy.is_alive and bullet.rect.colliderect(enemy.rect):
            hero.bullets.remove(bullet)  # 移除击中敌机的子弹
            enemy.take_damage()  # 敌机受到伤害
            if not enemy.is_alive:
                hero.add_kill(enemy.points)  # 敌机被摧毁，为英雄添加积分和计数
            break  # 避免同一子弹击中多架敌机

    # 敌机子弹击中英雄：遍历敌机子弹，检测是否与英雄碰撞
    for bullet in list(enemy.bullets):
        if bullet.rect.colliderect(hero.rect):
            hero.hit_by_enemy()  # 英雄受到伤害
            enemy.bullets.remove(bullet)  # 移除击中英雄的子弹
            break  # 避免同一子弹击中英雄多次