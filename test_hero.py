"""Test cases for HeroPlane class."""

import pygame
import pytest
import warnings

# 忽略所有DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)

from game.hero import HeroPlane
from game.assets import GameAssets


class MockGameAssets:
    """Mock GameAssets class for testing."""
    def __init__(self):
        self.hero = pygame.Surface((50, 50))
        self.hero_blowup = [pygame.Surface((50, 50)) for _ in range(4)]
        self.bullet = pygame.Surface((10, 20))
        self.shoot_sound = None
        self.explosion_sound = None
        self.main_music = None


@pytest.fixture
def hero():
    """Fixture to create a HeroPlane instance."""
    pygame.init()
    screen = pygame.display.set_mode((480, 650))
    assets = MockGameAssets()
    return HeroPlane(screen, assets)


def test_initial_lives(hero):
    """Test that hero starts with correct number of lives."""
    assert hero.lives == 5


def test_initial_shield(hero):
    """Test that hero starts with shield active."""
    assert hero.shield is True


def test_initial_score(hero):
    """Test that hero starts with zero score."""
    assert hero.score == 0


def test_initial_kill_count(hero):
    """Test that hero starts with zero kill count."""
    assert hero.kill_count == 0


def test_hit_by_enemy_with_shield(hero):
    """Test that hero loses shield when hit with shield active."""
    hero.hit_by_enemy()
    assert hero.shield is False
    assert hero.lives == 5  # Lives should remain the same


def test_hit_by_enemy_without_shield(hero):
    """Test that hero loses a life when hit without shield."""
    hero.shield = False
    hero.hit_by_enemy()
    assert hero.lives == 4


def test_add_kill_increases_score(hero):
    """Test that adding a kill increases the score."""
    initial_score = hero.score
    hero.add_kill(10)
    assert hero.score == initial_score + 10


def test_add_kill_increases_kill_count(hero):
    """Test that adding a kill increases the kill count."""
    initial_kill_count = hero.kill_count
    hero.add_kill()
    assert hero.kill_count == initial_kill_count + 1


def test_shield_recovery_after_five_kills(hero):
    """Test that shield recovers after every five kills."""
    hero.shield = False
    hero.kill_count = 4  # One more kill to reach 5
    hero.add_kill()
    assert hero.shield is True