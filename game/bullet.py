"""Bullet entities used by hero and enemy."""

import pygame

from .constants import BULLET_SPEED, ENEMY_BULLET_SPEED, SCREEN_RECT


class Bullet:
    def __init__(self, x: int, y: int, screen: pygame.Surface, sprite: pygame.Surface) -> None:
        self.screen = screen
        self.image = sprite
        self.x = x + 40
        self.y = y - 20

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def move(self) -> None:
        self.y -= BULLET_SPEED

    def display(self) -> None:
        self.screen.blit(self.image, (self.x, self.y))

    def is_off_screen(self) -> bool:
        return self.y < SCREEN_RECT.top


class EnemyBullet:
    def __init__(self, x: int, y: int, screen: pygame.Surface, sprite: pygame.Surface) -> None:
        self.screen = screen
        self.image = sprite
        self.x = x + 22
        self.y = y + 40

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def move(self) -> None:
        self.y += ENEMY_BULLET_SPEED

    def display(self) -> None:
        self.screen.blit(self.image, (self.x, self.y))

    def is_off_screen(self) -> bool:
        return self.y > SCREEN_RECT.bottom

