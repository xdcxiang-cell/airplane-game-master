"""Test cases for EnemyPlane class."""

import pygame
import pytest
import warnings

# 忽略所有DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)

from game.enemy import EnemyPlane


class MockGameAssets:
    """Mock GameAssets class for testing."""
    def __init__(self):
        self.enemy = pygame.Surface((50, 50))
        self.enemy2 = pygame.Surface((60, 60))
        self.enemy3 = pygame.Surface((70, 70))
        self.enemy_bullet = pygame.Surface((10, 20))
        # 添加一个mock的explosion_sound属性，避免AttributeError
        class MockSound:
            def play(self):
                pass
        self.explosion_sound = MockSound()


@pytest.fixture
def enemy_type1():
    """Fixture to create a type1 EnemyPlane instance."""
    pygame.init()
    screen = pygame.display.set_mode((480, 650))
    assets = MockGameAssets()
    return EnemyPlane(screen, assets, "type1")


@pytest.fixture
def enemy_type2():
    """Fixture to create a type2 EnemyPlane instance."""
    pygame.init()
    screen = pygame.display.set_mode((480, 650))
    assets = MockGameAssets()
    return EnemyPlane(screen, assets, "type2")


@pytest.fixture
def enemy_type3():
    """Fixture to create a type3 EnemyPlane instance."""
    pygame.init()
    screen = pygame.display.set_mode((480, 650))
    assets = MockGameAssets()
    return EnemyPlane(screen, assets, "type3")


def test_initial_health_type1(enemy_type1):
    """Test that type1 enemy starts with correct health."""
    assert enemy_type1.health == 1


def test_initial_health_type2(enemy_type2):
    """Test that type2 enemy starts with correct health."""
    assert enemy_type2.health == 2


def test_initial_health_type3(enemy_type3):
    """Test that type3 enemy starts with correct health."""
    assert enemy_type3.health == 3


def test_initial_speed_type1(enemy_type1):
    """Test that type1 enemy starts with correct speed."""
    assert enemy_type1.speed == 5


def test_initial_speed_type2(enemy_type2):
    """Test that type2 enemy starts with correct speed."""
    assert enemy_type2.speed == 4


def test_initial_speed_type3(enemy_type3):
    """Test that type3 enemy starts with correct speed."""
    assert enemy_type3.speed == 3


def test_initial_points_type1(enemy_type1):
    """Test that type1 enemy gives correct points."""
    assert enemy_type1.points == 10


def test_initial_points_type2(enemy_type2):
    """Test that type2 enemy gives correct points."""
    assert enemy_type2.points == 20


def test_initial_points_type3(enemy_type3):
    """Test that type3 enemy gives correct points."""
    assert enemy_type3.points == 30


def test_initial_alive_status(enemy_type1):
    """Test that enemy starts alive."""
    assert enemy_type1.is_alive is True


def test_take_damage_reduces_health(enemy_type2):
    """Test that taking damage reduces enemy health."""
    initial_health = enemy_type2.health
    enemy_type2.take_damage()
    assert enemy_type2.health == initial_health - 1


def test_die_when_health_zero(enemy_type1):
    """Test that enemy dies when health reaches zero."""
    enemy_type1.take_damage()
    assert enemy_type1.is_alive is False


def test_reset_position_respawns_enemy(enemy_type1):
    """Test that reset_position respawns enemy with full health."""
    enemy_type1.take_damage()  # Enemy dies
    enemy_type1.reset_position()
    assert enemy_type1.is_alive is True
    assert enemy_type1.health == enemy_type1.max_health