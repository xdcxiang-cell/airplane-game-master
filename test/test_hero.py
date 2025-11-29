import pytest
import pygame
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.hero import HeroPlane
from game.bullet import Bullet

@pytest.fixture
def hero():
    """Fixture to create a HeroPlane instance for testing."""
    pygame.init()
    screen = pygame.display.set_mode((400, 600))
    # Create a mock GameAssets object
    class MockAssets:
        hero = pygame.Surface((50, 50))
        hero.fill((255, 0, 0))
        hero_blowup = [pygame.Surface((50, 50)) for _ in range(4)]
        for i, surf in enumerate(hero_blowup):
            surf.fill((255, i*50, 0))
        bullet = pygame.Surface((10, 20))
        bullet.fill((0, 255, 0))
        shoot_sound = None
        explode_sound = None
        game_over_sound = None
    assets = MockAssets()
    hero = HeroPlane(screen, assets)
    return hero

def test_hero_initial_position(hero):
    """Test that the hero is initialized at the correct position."""
    assert hero.rect.x == 215  # (480/2) - (50/2) = 215
    assert hero.rect.y == 580  # 650 - 50 - 20 = 580

def test_hero_movement_left(hero):
    """Test hero movement to the left."""
    initial_x = hero.rect.x
    hero.move_left()
    assert hero.rect.x < initial_x

def test_hero_movement_right(hero):
    """Test hero movement to the right."""
    initial_x = hero.rect.x
    hero.move_right()
    assert hero.rect.x > initial_x

def test_hero_shoot(hero):
    """Test that the hero can shoot bullets."""
    initial_bullet_count = len(hero.bullets)
    hero.shoot()
    assert len(hero.bullets) == initial_bullet_count + 1
    assert isinstance(hero.bullets[0], Bullet)
    assert hero.bullets[0].rect.y < hero.rect.y

def test_hero_blowup(hero):
    """Test that the hero enters blowup state when hit."""
    initial_lives = hero.lives
    hero.bomb()
    assert hero.hit
    assert hero.lives == initial_lives - 1

if __name__ == '__main__':
    pytest.main([__file__])