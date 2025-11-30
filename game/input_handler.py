"""Keyboard input helpers."""

import pygame
from pygame.locals import K_LEFT, K_RIGHT, K_SPACE, K_a, K_d, KEYDOWN, QUIT

from .hero import HeroPlane


def key_control(hero: HeroPlane, shoot_effect: pygame.mixer.Sound = None) -> None:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == KEYDOWN:
            if event.key in (K_a, K_LEFT):
                hero.move_left()
            elif event.key in (K_d, K_RIGHT):
                hero.move_right()
            elif event.key == K_SPACE:
                hero.shoot(shoot_effect)

    pressed = pygame.key.get_pressed()
    if pressed[K_LEFT] or pressed[K_a]:
        hero.move_left()
    if pressed[K_RIGHT] or pressed[K_d]:
        hero.move_right()

