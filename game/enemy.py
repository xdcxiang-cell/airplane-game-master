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
    def __init__(self, screen: pygame.Surface, assets: "GameAssets", enemy_type: int = 0) -> None:
        self.screen = screen
        self.assets = assets
        self.enemy_type = enemy_type
        self.image = assets.enemies[enemy_type]
        self.x = 0
        self.y = 20
        self.direction = "right"
        self.bullets: list[EnemyBullet] = []
        # New health system
        self.health = constants.ENEMY_HEALTH[enemy_type]
        self.exploding = False
        self.explosion_frames = assets.enemy_explosions[enemy_type]
        self.explosion_frame_index = 0
        self.explosion_frame_counter = 0

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def display(self) -> None:
        if self.exploding:
            # Display explosion animation
            if self.explosion_frame_index < len(self.explosion_frames):
                self.screen.blit(self.explosion_frames[self.explosion_frame_index], (self.x, self.y))
                self.explosion_frame_counter += 1
                if self.explosion_frame_counter == 5:
                    self.explosion_frame_counter = 0
                    self.explosion_frame_index += 1
        else:
            # Display regular enemy
            self.screen.blit(self.image, (self.x, self.y))
        
        # Update bullets
        for bullet in list(self.bullets):
            bullet.display()
            bullet.move()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

    def move(self) -> None:
        if not self.exploding:
            speed = constants.ENEMY_SPEEDS[self.enemy_type]
            if self.direction == "right":
                self.x += speed
            else:
                self.x -= speed
            if self.x > constants.SCREEN_WIDTH - self.image.get_width():
                self.direction = "left"
            elif self.x < constants.SCREEN_RECT.left:
                self.direction = "right"

    def shoot(self) -> None:
        if not self.exploding:
            odds = constants.ENEMY_SHOOT_ODDS[self.enemy_type]
            random_num = random.randint(1, 100)
            if odds[0] <= random_num <= odds[1]:
                self.bullets.append(EnemyBullet(self.x, self.y, self.screen, self.assets.enemy_bullet))

    def reset_position(self) -> None:
        """Reset enemy position and state."""
        self.x = random.randint(0, constants.SCREEN_WIDTH - self.image.get_width())
        self.y = 20
        self.bullets.clear()
        self.health = constants.ENEMY_HEALTH[self.enemy_type]
        self.exploding = False
        self.explosion_frame_index = 0
        self.explosion_frame_counter = 0
    
    def take_damage(self) -> None:
        """Take 1 damage and start explosion if health reaches 0."""
        if not self.exploding:
            self.health -= 1
            if self.health <= 0:
                self.exploding = True

