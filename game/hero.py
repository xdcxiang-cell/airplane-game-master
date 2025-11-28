"""Hero plane implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from . import constants
from .bullet import Bullet

if TYPE_CHECKING:
    from .assets import GameAssets


class HeroPlane:
    def __init__(self, screen: pygame.Surface, assets: "GameAssets") -> None:
        self.screen = screen
        self.assets = assets
        self.image = assets.hero
        self.x = constants.SCREEN_WIDTH // 2 - self.image.get_width() // 2
        self.y = constants.SCREEN_HEIGHT - self.image.get_height() - 20
        self.bullets: list[Bullet] = []
        self.hit = False
        self.bomb_frames = assets.hero_blowup
        self.frame_counter = 0
        self.bomb_frame_index = 0
        # New health and score system
        self.health = constants.HERO_MAX_HEALTH
        self.score = 0

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def take_damage(self) -> None:
        """Take 1 damage and handle game over if health reaches 0."""
        if not self.hit:  # Prevent multiple damage while exploding
            self.health -= 1
            if self.health <= 0:
                self.hit = True

    def display(self) -> None:
        if self.hit:
            self.screen.blit(self.bomb_frames[self.bomb_frame_index], (self.x, self.y))
            self.frame_counter += 1
            if self.frame_counter == 7:
                self.frame_counter = 0
                self.bomb_frame_index += 1
            if self.bomb_frame_index >= len(self.bomb_frames):
                pygame.time.wait(1000)
                pygame.quit()
                raise SystemExit
        else:
            self.screen.blit(self.image, (self.x, self.y))
        for bullet in list(self.bullets):
            bullet.display()
            bullet.move()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

    def move_left(self) -> None:
        if self.x > constants.SCREEN_RECT.left:
            self.x = max(self.x - constants.HERO_SPEED, constants.SCREEN_RECT.left)

    def move_right(self) -> None:
        max_x = constants.SCREEN_RECT.right - self.image.get_width()
        if self.x < max_x:
            self.x = min(self.x + constants.HERO_SPEED, max_x)

    def shoot(self) -> None:
        if self.hit:
            return
        self.bullets.append(Bullet(self.x, self.y, self.screen, self.assets.bullet))
    
    def add_score(self, amount: int) -> None:
        """Add score when enemy is destroyed."""
        self.score += amount

