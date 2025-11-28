import pygame
import pytest
from game.hero import HeroPlane
from game.bullet import Bullet
from game.enemy import EnemyPlane
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT


@pytest.fixture
def mock_screen():
    pygame.init()
    return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


@pytest.fixture
def mock_assets():
    # Create mock assets dataclass
    from game.assets import GameAssets
    return GameAssets(
        hero=pygame.Surface((80, 60)),
        hero_blowup=[pygame.Surface((80, 60))],
        bullet=pygame.Surface((10, 20)),
        enemy=pygame.Surface((60, 50)),
        enemy1=pygame.Surface((80, 70)),
        enemy2=pygame.Surface((100, 90)),
        enemy_bullet=pygame.Surface((10, 20)),
        background=pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    )


def test_hero_initialization(mock_screen, mock_assets):
    hero = HeroPlane(mock_screen, mock_assets)
    assert hero.x == SCREEN_WIDTH // 2 - 40  # Center horizontally
    assert hero.y == SCREEN_HEIGHT - 60 - 20  # Near bottom
    assert hero.current_hp == hero.max_hp
    assert hero.score == 0
    assert len(hero.bullets) == 0
    assert not hero.hit


def test_hero_movement(mock_screen, mock_assets):
    hero = HeroPlane(mock_screen, mock_assets)
    initial_x = hero.x
    
    hero.move_left(dt=1.0)
    assert hero.x == initial_x - 8  # HERO_SPEED = 8
    
    hero.move_right(dt=1.0)
    assert hero.x == initial_x  # Back to original position
    
    # Test boundary checking
    hero.x = 0
    hero.move_left(dt=1.0)
    assert hero.x == 0  # Should not move left beyond screen
    
    hero.x = SCREEN_WIDTH - 80
    hero.move_right(dt=1.0)
    assert hero.x == SCREEN_WIDTH - 80  # Should not move right beyond screen


def test_hero_shooting(mock_screen, mock_assets):
    hero = HeroPlane(mock_screen, mock_assets)
    
    hero.shoot()
    assert len(hero.bullets) == 1
    assert isinstance(hero.bullets[0], Bullet)
    
    # Check bullet position
    bullet = hero.bullets[0]
    assert bullet.x == hero.x + 40
    assert bullet.y == hero.y - 20


def test_bullet_movement(mock_screen, mock_assets):
    hero = HeroPlane(mock_screen, mock_assets)
    hero.shoot()
    bullet = hero.bullets[0]
    initial_y = bullet.y
    
    bullet.move()
    assert bullet.y == initial_y - 18  # BULLET_SPEED = 18
    
    bullet.y = -1
    assert bullet.is_off_screen()


def test_enemy_initialization(mock_screen, mock_assets):
    enemy = EnemyPlane(mock_screen, mock_assets, 'small')
    assert enemy.x >= 0 and enemy.x <= SCREEN_WIDTH - 60  # Small enemy width = 60
    assert enemy.y == -50  # Starts off screen at top
    assert enemy.is_alive
    assert enemy.current_hp == 1


def test_enemy_movement(mock_screen, mock_assets):
    enemy = EnemyPlane(mock_screen, mock_assets, 'small')
    initial_y = enemy.y
    
    enemy.move(dt=1.0)
    assert enemy.y == initial_y + 1  # Small enemy speed * 0.2 * dt = 5 * 0.2 * 1 = 1
    
    enemy.y = SCREEN_HEIGHT + 50  # Small enemy height is 50
    enemy.move(dt=0.1)  # Call move to trigger is_alive update
    assert not enemy.is_alive


if __name__ == '__main__':
    pytest.main([__file__, '-v'])