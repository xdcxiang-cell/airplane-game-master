"""HeroPlane类的测试用例"""
import pygame
import pytest

from game.hero import HeroPlane
from game.assets import GameAssets, load_assets
from game import constants


class TestHeroPlane:
    """测试HeroPlane类的功能"""
    
    @pytest.fixture
    def hero(self):
        """创建一个HeroPlane实例供测试使用"""
        pygame.init()
        screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        assets = load_assets()
        return HeroPlane(screen, assets)
    
    def test_initialization(self, hero):
        """测试HeroPlane初始化是否正确"""
        assert hero.lives == constants.INITIAL_LIVES
        assert hero.shield == True
        assert hero.shield_health == 2
        assert hero.kill_count == 0
        assert hero.score == 0
        assert hero.hit == False
    
    def test_move_left(self, hero):
        """测试向左移动功能"""
        initial_x = hero.x
        hero.move_left()
        assert hero.x == initial_x - constants.HERO_SPEED
        
        # 测试边界检测（不能移出屏幕左侧）
        hero.x = 0
        hero.move_left()
        assert hero.x == 0
    
    def test_move_right(self, hero):
        """测试向右移动功能"""
        initial_x = hero.x
        hero.move_right()
        assert hero.x == initial_x + constants.HERO_SPEED
        
        # 测试边界检测（不能移出屏幕右侧）
        hero.x = constants.SCREEN_WIDTH - hero.image.get_width()
        hero.move_right()
        assert hero.x == constants.SCREEN_WIDTH - hero.image.get_width()
    
    def test_shoot(self, hero):
        """测试射击功能"""
        initial_bullet_count = len(hero.bullets)
        hero.shoot()
        assert len(hero.bullets) == initial_bullet_count + 1
    
    def test_take_damage_with_shield(self, hero):
        """测试有护盾时受到伤害"""
        initial_shield_health = hero.shield_health
        hero.take_damage()
        assert hero.shield_health == initial_shield_health - 1
        assert hero.lives == constants.INITIAL_LIVES
        
        # 测试护盾被打破
        hero.shield_health = 1
        hero.take_damage()
        assert hero.shield == False
        assert hero.shield_health == 0
    
    def test_take_damage_without_shield(self, hero):
        """测试无护盾时受到伤害"""
        hero.shield = False
        initial_lives = hero.lives
        hero.take_damage()
        assert hero.lives == initial_lives - 1
        
        # 测试生命值耗尽
        hero.lives = 1
        hero.take_damage()
        assert hero.hit == True
    
    def test_increase_kill_count(self, hero):
        """测试增加击杀计数"""
        initial_kill_count = hero.kill_count
        hero.increase_kill_count()
        assert hero.kill_count == initial_kill_count + 1
        
        # 测试击杀5个敌人后恢复护盾
        hero.kill_count = constants.SHIELD_RESTORE_KILLS - 1
        hero.shield = False
        hero.increase_kill_count()
        assert hero.shield == True
        assert hero.shield_health == 2
    
    def test_increase_score(self, hero):
        """测试增加积分"""
        initial_score = hero.score
        points = 100
        hero.increase_score(points)
        assert hero.score == initial_score + points
