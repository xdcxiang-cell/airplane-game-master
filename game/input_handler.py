"""Keyboard input helpers."""

import pygame
from pygame.locals import K_LEFT, K_RIGHT, K_SPACE, K_a, K_d, KEYDOWN, QUIT

from .hero import HeroPlane


def key_control(hero: HeroPlane, dt: float = 1.0) -> None:
    # Note: Event handling is now done in main.py to avoid duplicate processing
    pressed = pygame.key.get_pressed()
    if pressed[K_LEFT] or pressed[K_a]:
        hero.move_left(dt)
    if pressed[K_RIGHT] or pressed[K_d]:
        hero.move_right(dt)

