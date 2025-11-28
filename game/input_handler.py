"""Keyboard input helpers."""

import pygame
from pygame.locals import K_LEFT, K_RIGHT, K_SPACE, K_a, K_d, KEYDOWN, QUIT

from .hero import HeroPlane
from . import constants


def key_control(hero: HeroPlane, dt: float = 1.0) -> None:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == KEYDOWN:
            if event.key in (K_a, K_LEFT):
                hero.move_left(dt)
            elif event.key in (K_d, K_RIGHT):
                hero.move_right(dt)
            elif event.key == K_SPACE:
                hero.shoot()
            elif event.key == constants.LANGUAGE_SWITCH_KEY:
                # Switch language
                if hasattr(hero, 'language_manager'):
                    if hero.language_manager.current_language == 'zh':
                        hero.language_manager.switch_language('en')
                    else:
                        hero.language_manager.switch_language('zh')

    pressed = pygame.key.get_pressed()
    if pressed[K_LEFT] or pressed[K_a]:
        hero.move_left(dt)
    if pressed[K_RIGHT] or pressed[K_d]:
        hero.move_right(dt)

