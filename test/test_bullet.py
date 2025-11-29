import pytest
import pygame
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.bullet import Bullet

@pytest.fixture
def bullet():
    """Fixture to create a Bullet instance for testing."""
    pygame.init()
    screen = pygame.display.set_mode((480, 600))  # Match actual game screen size
    # Create a mock bullet image
    bullet_image = pygame.Surface((10, 20))
    bullet_image.fill((0, 255, 0))
    # Create Bullet instance with correct parameters
    bullet = Bullet(200, 500, screen, bullet_image)
    return bullet

def test_bullet_initial_position(bullet):
    """Test that the bullet is initialized at the correct position."""
    assert bullet.rect.x == 240  # Bullet is centered on screen (480/2)
    assert bullet.rect.y == 480  # Bullet is initialized 20px above the given y position

def test_bullet_movement(bullet):
    """Test that the bullet moves upward."""
    initial_y = bullet.rect.y
    bullet.move()
    assert bullet.rect.y < initial_y

def test_bullet_out_of_screen(bullet):
    """Test that the bullet is marked for removal when it goes out of the screen."""
    bullet.y = -10  # Move bullet above the screen
    bullet.move()
    assert bullet.is_off_screen()

if __name__ == '__main__':
    pytest.main([__file__])