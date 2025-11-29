import pytest
import pygame
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.hero import HeroPlane
from game.enemy import EnemyPlane
from game.bullet import Bullet, EnemyBullet

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
    hero.x = 200
    hero.y = 500
    return hero

@pytest.fixture
def enemy():
    """Fixture to create an EnemyPlane instance for testing."""
    pygame.init()
    screen = pygame.display.set_mode((400, 600))
    # Create a mock GameAssets object
    class MockAssets:
        enemy = pygame.Surface((50, 50))
        enemy.fill((0, 0, 255))
        enemy_bullet = pygame.Surface((10, 20))
        enemy_bullet.fill((255, 0, 0))
    assets = MockAssets()
    enemy = EnemyPlane(screen, assets)
    enemy.x = 200
    enemy.y = 300
    return enemy

@pytest.fixture

def bullet(hero):
    """Fixture to create a Bullet instance for testing."""
    bullet_sprite = pygame.Surface((20, 20))
    return Bullet(hero.rect.centerx, hero.rect.y, hero.screen, bullet_sprite)

def test_bullet_enemy_collision(bullet, enemy):
    """Test that a bullet collides with an enemy."""
    # Position bullet to collide with enemy
    bullet.x = enemy.rect.x
    bullet.y = enemy.rect.y
    
    # Check collision
    assert bullet.rect.colliderect(enemy.rect)

def test_hero_enemy_collision(hero, enemy):
    """Test that the hero collides with an enemy."""
    # Position enemy to collide with hero
    enemy.x = hero.x
    enemy.y = hero.y
    
    # Check collision
    assert hero.rect.colliderect(enemy.rect)

def test_enemy_bullet_hero_collision(hero, enemy):
    """Test that an enemy bullet collides with the hero."""
    # Create enemy bullet
    enemy_bullet = EnemyBullet(enemy.x, enemy.y, enemy.screen, enemy.assets.enemy_bullet)
    
    # Position enemy bullet to collide with hero
    enemy_bullet.x = hero.rect.x
    enemy_bullet.y = hero.rect.y
    
    # Check collision
    assert enemy_bullet.rect.colliderect(hero.rect)

def test_no_collision(hero, enemy):
    """Test that there's no collision when objects are not overlapping."""
    # Position enemy far away from hero
    enemy.rect.x = 1000  # Outside the screen
    enemy.rect.y = 1000
    
    # Check no collision
    assert not hero.rect.colliderect(enemy.rect)

if __name__ == '__main__':
    pytest.main([__file__])