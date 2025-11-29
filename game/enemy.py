"""Enemy plane implementation.

This module defines the EnemyPlane and EnemyPlaneType1 classes which represent
enemy aircraft in the game.
"""

from __future__ import annotations

import random
from typing import TYPE_CHECKING

import pygame

from . import constants
from .bullet import EnemyBullet

if TYPE_CHECKING:
    from .assets import GameAssets


class EnemyPlane:
    def __init__(self, screen: pygame.Surface, assets: "GameAssets") -> None:
        """Initialize the enemy plane.
        
        Args:
            screen: The pygame surface to draw on.
            assets: The game assets containing images and sounds.
        """
        self.screen = screen
        self.assets = assets
        self.image = assets.enemy
        self.x = 0
        self.y = 20
        self.direction = "right"
        self.bullets: list[EnemyBullet] = []
        self.max_health = 1  # 敌机初始生命值
        self.current_health = self.max_health
        self.dead = False

    @property
    def rect(self) -> pygame.Rect:
        """Get the rectangular bounding box of the enemy plane.
        
        Returns:
            A pygame.Rect object representing the enemy's position and size.
        """
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def display(self) -> None:
        """Display the enemy plane and its current state on the screen.
        
        This method also displays the enemy's health bar and bullets.
        """
        if not self.dead:
            self.screen.blit(self.image, (self.x, self.y))
            
            # Draw health bar
            health_bar_width = self.image.get_width()
            health_bar_height = 5
            health_ratio = self.current_health / self.max_health
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x, self.y - 10, health_bar_width, health_bar_height))
            pygame.draw.rect(self.screen, (0, 255, 0), (self.x, self.y - 10, health_bar_width * health_ratio, health_bar_height))
            
            for bullet in list(self.bullets):
                bullet.display()
                bullet.move()
                if bullet.is_off_screen():
                    self.bullets.remove(bullet)

    def move(self) -> None:
        """Move the enemy plane according to its movement pattern."""
        if self.direction == "right":
            self.x += constants.ENEMY_SPEED
        else:
            self.x -= constants.ENEMY_SPEED
        if self.x > constants.SCREEN_WIDTH - self.image.get_width():
            self.direction = "left"
        elif self.x < constants.SCREEN_RECT.left:
            self.direction = "right"

        # Move down slowly
        self.y += constants.ENEMY_SPEED * 0.2

    def shoot(self) -> None:
        """Shoot a bullet from the enemy plane with a certain probability."""
        random_num = random.randint(1, 100)
        if random_num in constants.ENEMY_SHOOT_ODDS:
            self.bullets.append(EnemyBullet(self.x, self.y, self.screen, self.assets.enemy_bullet))

    def take_damage(self, damage: int) -> None:
        """Handle the enemy plane taking damage.
        
        Args:
            damage: The amount of damage to apply to the enemy.
        """
        self.current_health -= damage
        if self.current_health <= 0:
            self.dead = True

    def reset_position(self) -> None:
        """Reset the enemy plane's position and state for a new wave."""
        self.x = random.randint(0, constants.SCREEN_WIDTH - self.image.get_width())
        self.y = 20
        self.bullets.clear()
        self.current_health = self.max_health
        self.dead = False


class EnemyPlaneType1(EnemyPlane):
    def __init__(self, screen: pygame.Surface, assets: "GameAssets") -> None:
        """Initialize the type 1 enemy plane.
        
        Args:
            screen: The pygame surface to draw on.
            assets: The game assets containing images and sounds.
        """
        super().__init__(screen, assets)
        self.image = assets.enemy1
        self.max_health = 3  # Type 1 enemy has higher health
        self.current_health = self.max_health
        self.direction = "left" if random.random() < 0.5 else "right"
        self.speed = constants.ENEMY_SPEED * 1.2  # Type 1 enemy is faster

    def move(self) -> None:
        """Move the type 1 enemy plane according to its movement pattern."""
        if self.direction == "right":
            self.x += self.speed
        else:
            self.x -= self.speed
        if self.x > constants.SCREEN_WIDTH - self.image.get_width():
            self.direction = "left"
        elif self.x < constants.SCREEN_RECT.left:
            self.direction = "right"

        # Move down slowly
        self.y += self.speed * 0.15