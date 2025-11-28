"""Test cases for the airplane game."""

import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.assets import load_assets
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from game.hero import HeroPlane
from game.enemy import EnemyPlane


def test_hero_creation():
    """Test if the hero plane can be created successfully."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    assets = load_assets()
    hero = HeroPlane(screen, assets)
    
    assert hero is not None
    assert hero.health == 5
    assert hero.score == 0
    assert hero.x == SCREEN_WIDTH // 2 - hero.image.get_width() // 2
    assert hero.y == SCREEN_HEIGHT - hero.image.get_height() - 20
    
    print("✓ Hero creation test passed")


def test_enemy_creation():
    """Test if different types of enemy planes can be created successfully."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    assets = load_assets()
    
    # Test all enemy types
    for enemy_type in range(3):
        enemy = EnemyPlane(screen, assets, enemy_type)
        assert enemy is not None
        assert enemy.enemy_type == enemy_type
        assert enemy.health == enemy_type + 1
        
    print("✓ Enemy creation test passed")


def test_hero_movement():
    """Test hero plane movement functionality."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    assets = load_assets()
    hero = HeroPlane(screen, assets)
    
    initial_x = hero.x
    
    # Test left movement
    hero.move_left()
    assert hero.x < initial_x
    
    # Test right movement
    hero.move_right()
    hero.move_right()
    assert hero.x > initial_x
    
    print("✓ Hero movement test passed")


def test_collision_detection():
    """Test basic collision detection functionality."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    assets = load_assets()
    hero = HeroPlane(screen, assets)
    enemy = EnemyPlane(screen, assets, 0)
    
    # Position hero and enemy to collide
    enemy.x = hero.x
    enemy.y = hero.y
    
    # Check collision
    hero_rect = hero.rect
    enemy_rect = enemy.rect
    
    assert hero_rect.colliderect(enemy_rect)
    
    print("✓ Collision detection test passed")


def test_health_system():
    """Test hero and enemy health systems."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    assets = load_assets()
    hero = HeroPlane(screen, assets)
    enemy = EnemyPlane(screen, assets, 1)  # 2 health
    
    # Test hero health
    initial_hero_health = hero.health
    hero.take_damage()
    assert hero.health == initial_hero_health - 1
    
    # Test enemy health
    initial_enemy_health = enemy.health
    enemy.take_damage()
    assert enemy.health == initial_enemy_health - 1
    
    print("✓ Health system test passed")


def run_all_tests():
    """Run all test cases."""
    print("Running game tests...\n")
    
    test_hero_creation()
    test_enemy_creation()
    test_hero_movement()
    test_collision_detection()
    test_health_system()
    
    print("\n✅ All tests passed!")


if __name__ == "__main__":
    run_all_tests()
    pygame.quit()
