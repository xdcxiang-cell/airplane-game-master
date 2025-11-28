"""Enemy plane implementation."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING

import pygame

from . import constants
from .bullet import EnemyBullet

if TYPE_CHECKING:
    from .assets import GameAssets


class EnemyPlane:
    def __init__(self, screen: pygame.Surface, assets: "GameAssets", enemy_type: str = 'small') -> None:
        self.screen = screen
        self.assets = assets
        self.enemy_type = enemy_type
        
        # Get enemy configuration based on type
        enemy_config = constants.ENEMY_TYPES.get(enemy_type, constants.ENEMY_TYPES['small'])
        self.speed = enemy_config['speed']
        self.max_hp = enemy_config['hp']
        self.score_value = enemy_config['score']
        self.width, self.height = enemy_config['size']
        
        # Load appropriate image based on type
        if enemy_type == 'small':
            self.image = assets.enemy
        elif enemy_type == 'medium':
            self.image = assets.enemy1  # Assuming assets has medium enemy image
        elif enemy_type == 'large':
            self.image = assets.enemy2  # Assuming assets has large enemy image
        else:
            self.image = assets.enemy
        
        # Initialize position and direction
        self.x = random.randint(0, constants.SCREEN_WIDTH - self.width)
        self.y = -self.height  # Start above the screen
        self.direction = "right" if random.random() > 0.5 else "left"
        
        # Health and state
        self.current_hp = self.max_hp
        self.is_alive = True
        
        # Bullets
        self.bullets: list[EnemyBullet] = []
        
        # Font for HP display
        self.font = pygame.font.SysFont(None, 20)

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def display(self) -> None:
        if self.is_alive:
            self.screen.blit(self.image, (self.x, self.y))
            
            # Display enemy HP
            hp_text = f"HP: {self.current_hp}/{self.max_hp}"
            text_surface = self.font.render(hp_text, True, (255, 0, 0))  # Red text
            text_rect = text_surface.get_rect()
            text_rect.centerx = self.x + self.width // 2
            text_rect.top = self.y - 20  # Above the enemy
            self.screen.blit(text_surface, text_rect)
        
        for bullet in list(self.bullets):
            bullet.display()
            bullet.move()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

    def move(self, dt: float = 1.0) -> None:
        if not self.is_alive:
            return
        
        # Update position based on direction and delta time
        if self.direction == "right":
            self.x += self.speed * dt
        else:
            self.x -= self.speed * dt
        
        # Keep enemy within screen bounds
        if self.x > constants.SCREEN_WIDTH - self.width:
            self.direction = "left"
            self.x = constants.SCREEN_WIDTH - self.width
        elif self.x < constants.SCREEN_RECT.left:
            self.direction = "right"
            self.x = constants.SCREEN_RECT.left
        
        # Move down gradually
        self.y += self.speed * 0.2 * dt
        
        # Check if enemy is off screen
        if self.y > constants.SCREEN_HEIGHT + self.height:
            self.is_alive = False

    def shoot(self) -> None:
        if not self.is_alive:
            return
        
        random_num = random.randint(1, 100)
        if random_num in constants.ENEMY_SHOOT_ODDS:
            self.bullets.append(EnemyBullet(self.x, self.y, self.screen, self.assets.enemy_bullet))

    def take_damage(self, damage: int = 1) -> None:
        if not self.is_alive:
            return
        
        self.current_hp -= damage
        if self.current_hp <= 0:
            self.is_alive = False
            # Add explosion animation here if available

    def reset(self) -> None:
        """Reset enemy to initial state."""
        self.x = random.randint(0, constants.SCREEN_WIDTH - self.width)
        self.y = -self.height  # Start above the screen
        self.direction = "right" if random.random() > 0.5 else "left"
        self.current_hp = self.max_hp
        self.is_alive = True
        self.bullets.clear()

