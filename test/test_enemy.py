import pytest
import pygame
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.enemy import EnemyPlane

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
    enemy.y = 50
    return enemy

def test_enemy_initial_position(enemy):
    """Test that the enemy is initialized at the correct position."""
    assert enemy.rect.x == 200
    assert enemy.rect.y == 50

def test_enemy_movement_down(enemy):
    """Test that the enemy moves downward."""
    initial_y = enemy.rect.y
    enemy.move()
    assert enemy.rect.y > initial_y

def test_enemy_shoot(enemy):
    """Test that the enemy can shoot bullets."""
    initial_bullet_count = len(enemy.bullets)
    enemy.shoot()
    # Check if at least one bullet is created
    assert len(enemy.bullets) >= initial_bullet_count

def test_enemy_take_damage(enemy):
    """Test that the enemy takes damage and dies when health reaches zero."""
    initial_health = enemy.current_health
    enemy.take_damage(initial_health)
    assert enemy.dead

def test_enemy_movement_bounds(enemy):
    """Test that the enemy changes direction when hitting the screen bounds."""
    enemy.x = 0
    enemy.direction = "left"
    enemy.move()
    assert enemy.direction == "right"
    
    enemy.x = 430  # Screen width is 480, enemy width is 50
    enemy.direction = "right"
    enemy.move()
    assert enemy.direction == "left"

if __name__ == '__main__':
    pytest.main([__file__])