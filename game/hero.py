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
        self.max_hp = constants.HERO_MAX_HP
        self.hp = self.max_hp
        self.score = 0
        self.is_blowing_up = False
        self.bomb_frames = assets.hero_blowup
        self.frame_counter = 0
        self.bomb_frame_index = 0
        self.game_over = False

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def take_damage(self, damage: int = 1) -> None:
        if self.is_blowing_up or self.game_over:
            return
        self.hp -= damage
        if self.hp <= 0:
            self.is_blowing_up = True

    def add_score(self, points: int) -> None:
        if not self.game_over:
            self.score += points

    def display(self) -> None:
        if self.is_blowing_up:
            if self.bomb_frame_index < len(self.bomb_frames):
                self.screen.blit(self.bomb_frames[self.bomb_frame_index], (self.x, self.y))
                self.frame_counter += 1
                if self.frame_counter == 7:
                    self.frame_counter = 0
                    self.bomb_frame_index += 1
            else:
                self.game_over = True
        elif not self.game_over:
            self.screen.blit(self.image, (self.x, self.y))
        for bullet in list(self.bullets):
            bullet.display()
            bullet.move()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

    def move_left(self, dt: float) -> None:
        if self.is_blowing_up or self.game_over:
            return
        if self.x > constants.SCREEN_RECT.left:
            self.x = max(self.x - constants.HERO_SPEED * dt, constants.SCREEN_RECT.left)

    def move_right(self, dt: float) -> None:
        if self.is_blowing_up or self.game_over:
            return
        max_x = constants.SCREEN_RECT.right - self.image.get_width()
        if self.x < max_x:
            self.x = min(self.x + constants.HERO_SPEED * dt, max_x)

    def shoot(self) -> None:
        if self.is_blowing_up or self.game_over:
            return
        bullet_x = self.x + self.image.get_width() // 2 - self.assets.bullet.get_width() // 2
        bullet_y = self.y - self.assets.bullet.get_height()
        self.bullets.append(Bullet(bullet_x, bullet_y, self.screen, self.assets.bullet))

