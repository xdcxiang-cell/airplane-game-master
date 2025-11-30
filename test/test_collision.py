"""碰撞检测功能的测试用例"""
import pygame
import pytest

from game.collision import handle_collisions
from game.hero import HeroPlane
from game.enemy import EnemyPlane
from game.assets import GameAssets
from game import constants


class TestCollision:
    """测试碰撞检测功能"""
    
    @pytest.fixture
    def setup(self):
        """创建测试所需的游戏对象"""
        pygame.init()
        screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        assets = GameAssets()
        hero = HeroPlane(screen, assets)
        enemy = EnemyPlane(screen, assets, 100, 100)
        return screen, assets, hero, enemy
    
    def test_player_bullet_enemy_collision(self, setup):
        """测试玩家子弹与敌机碰撞"""
        screen, assets, hero, enemy = setup
        
        # 让玩家射击并移动子弹到敌机位置
        hero.shoot()
        bullet = hero.bullets[0]
        bullet.x = enemy.x
        bullet.y = enemy.y
        
        initial_enemy_hp = enemy.hp
        initial_hero_kill_count = hero.kill_count
        initial_hero_score = hero.score
        
        handle_collisions(hero, [enemy])
        
        assert enemy.hp == initial_enemy_hp - 1
        assert len(hero.bullets) == 0  # 子弹应该被移除
    
    def test_enemy_bullet_player_collision(self, setup):
        """测试敌机子弹与玩家碰撞"""
        screen, assets, hero, enemy = setup
        
        # 让敌机射击并移动子弹到玩家位置
        enemy.shoot()
        bullet = enemy.bullets[0]
        bullet.x = hero.x
        bullet.y = hero.y + hero.image.get_height()
        
        initial_hero_shield_health = hero.shield_health
        
        handle_collisions(hero, [enemy])
        
        assert hero.shield_health == initial_hero_shield_health - 1
        assert len(enemy.bullets) == 0  # 子弹应该被移除
    
    def test_no_collision(self, setup):
        """测试没有碰撞的情况"""
        screen, assets, hero, enemy = setup
        
        # 让玩家和敌机射击，但子弹不相交
        hero.shoot()
        enemy.shoot()
        
        initial_hero_bullet_count = len(hero.bullets)
        initial_enemy_bullet_count = len(enemy.bullets)
        initial_enemy_hp = enemy.hp
        initial_hero_shield_health = hero.shield_health
        
        handle_collisions(hero, [enemy])
        
        assert len(hero.bullets) == initial_hero_bullet_count
        assert len(enemy.bullets) == initial_enemy_bullet_count
        assert enemy.hp == initial_enemy_hp
        assert hero.shield_health == initial_hero_shield_health
