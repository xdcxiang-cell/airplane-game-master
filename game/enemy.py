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
    def __init__(self, screen: pygame.Surface, assets: "GameAssets") -> None:
        self.screen = screen
        self.assets = assets
        self.image = assets.enemy
        self.x = 0
        self.y = 20
        self.direction = "right"
        self.bullets: list[EnemyBullet] = []

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def display(self) -> None:
        self.screen.blit(self.image, (self.x, self.y))
        for bullet in list(self.bullets):
            bullet.display()
            bullet.move()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

    def move(self) -> None:
        if self.direction == "right":
            self.x += constants.ENEMY_SPEED
        else:
            self.x -= constants.ENEMY_SPEED
        if self.x > constants.SCREEN_WIDTH - self.image.get_width():
            self.direction = "left"
        elif self.x < constants.SCREEN_RECT.left:
            self.direction = "right"

    def shoot(self) -> None:
        random_num = random.randint(1, 100)
        if random_num in constants.ENEMY_SHOOT_ODDS:
            self.bullets.append(EnemyBullet(self.x, self.y, self.screen, self.assets.enemy_bullet))

    def reset_position(self) -> None:
        self.x = random.randint(0, constants.SCREEN_WIDTH - self.image.get_width())
        self.y = 20
        self.bullets.clear()

