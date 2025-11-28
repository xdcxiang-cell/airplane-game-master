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
    def __init__(self, screen: pygame.Surface, assets: "GameAssets", enemy_type: str = "small") -> None:
        self.screen = screen
        self.assets = assets
        self.enemy_type = enemy_type
        self.type_data = constants.ENEMY_TYPES[enemy_type]
        
        # Set image based on enemy type
        if enemy_type == "small":
            self.image = assets.enemy_small
        elif enemy_type == "medium":
            self.image = assets.enemy_medium
        else:  # large
            self.image = assets.enemy_large
        
        # Initialize position and movement
        self.x = 0
        self.y = -self.image.get_height()  # Start off screen
        self.direction = "right"
        self.speed = self.type_data["speed"]
        self.health = self.type_data["health"]
        self.max_health = self.type_data["health"]
        self.score_value = self.type_data["score"]
        self.bullets: list[EnemyBullet] = []
        self.destroyed = False
        self.frame_counter = 0
        self.animation_frame = 0

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def display(self, dt: float = 1.0) -> None:
        self.screen.blit(self.image, (self.x, self.y))
        for bullet in list(self.bullets):
            bullet.display()
            bullet.move(dt)
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

    def move(self, dt: float = 1.0) -> None:
        if self.destroyed:
            return
        
        # Horizontal movement (side to side)
        if self.direction == "right":
            self.x += self.speed * dt
        else:
            self.x -= self.speed * dt
        
        # Bounce off screen edges
        if self.x > constants.SCREEN_WIDTH - self.image.get_width():
            self.direction = "left"
            self.x = constants.SCREEN_WIDTH - self.image.get_width()
        elif self.x < constants.SCREEN_RECT.left:
            self.direction = "right"
            self.x = constants.SCREEN_RECT.left
        
        # Vertical movement down
        self.y += self.speed * dt * 0.5

    def shoot(self) -> None:
        if self.destroyed:
            return
        
        random_num = random.randint(1, 100)
        if random_num in self.type_data["shoot_odds"]:
            # Determine bullet position based on enemy type
            if self.enemy_type == "small":
                bullet_x = self.x + self.image.get_width() // 2
                bullet_y = self.y + self.image.get_height()
            elif self.enemy_type == "medium":
                bullet_x = self.x + self.image.get_width() // 2
                bullet_y = self.y + self.image.get_height() // 2
            else:  # large
                bullet_x = self.x + self.image.get_width() // 2
                bullet_y = self.y + self.image.get_height() // 3
            
            # Use appropriate bullet image based on enemy type
            if self.enemy_type == "small":
                bullet_image = self.assets.enemy_bullet_small
            elif self.enemy_type == "medium":
                bullet_image = self.assets.enemy_bullet_medium
            else:  # large
                bullet_image = self.assets.enemy_bullet_large
            
            self.bullets.append(EnemyBullet(bullet_x, bullet_y, self.screen, bullet_image))

    def take_damage(self, amount: int = 1) -> None:
        """Handle enemy taking damage."""
        if self.destroyed:
            return
        
        self.health -= amount
        if self.health <= 0:
            self.destroyed = True
            self.frame_counter = 0
            self.animation_frame = 0

    def display(self, dt: float = 1.0) -> None:
        if self.destroyed:
            # Display explosion animation based on enemy type
            if self.enemy_type == "small":
                explosion_frames = self.assets.enemy_small_explosion
            elif self.enemy_type == "medium":
                explosion_frames = self.assets.enemy_medium_explosion
            else:  # large
                explosion_frames = self.assets.enemy_large_explosion
            
            self.screen.blit(explosion_frames[self.animation_frame], (self.x, self.y))
            self.frame_counter += 1
            if self.frame_counter == 5:
                self.frame_counter = 0
                self.animation_frame += 1
            if self.animation_frame >= len(explosion_frames):
                # Remove enemy when animation completes
                return
        else:
            self.screen.blit(self.image, (self.x, self.y))
            
            # Draw health bar for medium and large enemies
            if self.enemy_type != "small":
                bar_width = self.image.get_width()
                bar_height = 4
                health_ratio = self.health / self.max_health
                
                # Draw background
                pygame.draw.rect(self.screen, (100, 100, 100), 
                                (self.x, self.y - 10, bar_width, bar_height))
                # Draw health bar
                pygame.draw.rect(self.screen, (255, 0, 0), 
                                (self.x, self.y - 10, int(bar_width * health_ratio), bar_height))
        
        # Update bullets
        for bullet in list(self.bullets):
            bullet.display()
            bullet.move(dt)
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

    def is_off_screen(self) -> bool:
        """Check if enemy is completely off screen."""
        return self.y > constants.SCREEN_HEIGHT

    def reset(self) -> None:
        """Reset enemy to initial state."""
        self.x = random.randint(0, constants.SCREEN_WIDTH - self.image.get_width())
        self.y = -self.image.get_height()
        self.direction = "right"
        self.health = self.max_health
        self.destroyed = False
        self.bullets.clear()

