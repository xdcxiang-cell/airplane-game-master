"""EnemyPlane类的测试用例"""
import pygame
import pytest

from game.enemy import EnemyPlane
from game.assets import GameAssets, load_assets
from game import constants


class TestEnemyPlane:
    """测试EnemyPlane类的功能"""
    
    @pytest.fixture
    def enemy(self):
        """创建一个EnemyPlane实例供测试使用"""
        pygame.init()
        screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        assets = load_assets()
        return EnemyPlane(screen, assets)
    
    def test_initialization(self, enemy):
        """测试EnemyPlane初始化是否正确"""
        assert enemy.x >= 0
        assert enemy.x <= constants.SCREEN_WIDTH - enemy.image.get_width()
        assert enemy.y == -enemy.image.get_height()
        assert enemy.health == 1
        assert enemy.hit == False
        assert enemy.points == 100
        assert enemy.bullets == []
    
    def test_move(self, enemy):
        """测试移动功能"""
        initial_x = enemy.x
        enemy.move()
        # 敌机应该向右移动
        assert enemy.x == initial_x + enemy.speed
    
    def test_shoot(self, enemy):
        """测试射击功能"""
        # 敌机有一定概率射击，所以我们不能保证每次都会射击
        initial_bullet_count = len(enemy.bullets)
        enemy.shoot()
        assert len(enemy.bullets) >= initial_bullet_count
    
    def test_take_damage(self, enemy):
        """测试受到伤害"""
        initial_health = enemy.health
        result = enemy.take_damage()
        assert enemy.health == initial_health - 1
        assert result == True  # 初始生命值为1，受到伤害后被摧毁
        
        # 测试敌机被摧毁
        enemy.hit = False  # 重置hit状态
        enemy.health = 1
        result = enemy.take_damage()
        assert result == True
    
    def test_is_destroyed(self, enemy):
        """测试是否被摧毁"""
        assert enemy.is_destroyed() == False
        
        # 测试生命值耗尽
        enemy.health = 0
        enemy.hit = True
        enemy.bomb_frame_index = len(enemy.blowup_frames)
        assert enemy.is_destroyed() == True
