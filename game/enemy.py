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
        if enemy_type == 0:
            self.image = assets.enemy
            self.max_hp = constants.ENEMY_MAX_HP
            self.score = constants.ENEMY_SCORE
            self.speed = constants.ENEMY_SPEED
        elif enemy_type == 1:
            self.image = assets.enemy1
            self.max_hp = constants.ENEMY_MAX_HP * 2
            self.score = constants.ENEMY_SCORE * 2
            self.speed = constants.ENEMY_SPEED * 1.2
        elif enemy_type == 2:
            self.image = assets.enemy2
            self.max_hp = constants.ENEMY_MAX_HP * 3
            self.score = constants.ENEMY_SCORE * 3
            self.speed = constants.ENEMY_SPEED * 1.5
        else:
            self.image = assets.enemy
            self.max_hp = constants.ENEMY_MAX_HP
            self.score = constants.ENEMY_SCORE
            self.speed = constants.ENEMY_SPEED
        self.hp = self.max_hp
        self.x = random.randint(0, constants.SCREEN_WIDTH - self.image.get_width())
        self.y = 20
        self.direction = "right"
        self.bullets: list[EnemyBullet] = []
        self.blowup_frames = assets.enemy_blowup[self.enemy_type]
        self.is_blowing_up = False
        self.blowup_frame_index = 0
        self.blowup_frame_counter = 0

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def display(self) -> None:
        if self.is_blowing_up:
            self.screen.blit(self.blowup_frames[self.blowup_frame_index], (self.x, self.y))
            self.blowup_frame_counter += 1
            if self.blowup_frame_counter == 7:
                self.blowup_frame_counter = 0
                self.blowup_frame_index += 1
            if self.blowup_frame_index >= len(self.blowup_frames):
                self.reset_position()
        else:
            self.screen.blit(self.image, (self.x, self.y))
        for bullet in list(self.bullets):
            bullet.display()
            bullet.move()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

    def move(self, dt: float) -> None:
        if self.is_blowing_up:
            return
        if self.direction == "right":
            self.x += self.speed * dt
        else:
            self.x -= self.speed * dt
        if self.x > constants.SCREEN_WIDTH - self.image.get_width():
            self.direction = "left"
        elif self.x < constants.SCREEN_RECT.left:
            self.direction = "right"

    def shoot(self) -> None:
        if self.is_blowing_up:
            return
        random_num = random.randint(1, 100)
        if random_num in constants.ENEMY_SHOOT_ODDS:
            bullet_x = self.x + self.image.get_width() // 2 - self.assets.enemy_bullet.get_width() // 2
            bullet_y = self.y + self.image.get_height()
            self.bullets.append(EnemyBullet(bullet_x, bullet_y, self.screen, self.assets.enemy_bullet))

    def take_damage(self, damage: int = 1) -> None:
        if self.is_blowing_up:
            return
        self.hp -= damage
        if self.hp <= 0:
            self.is_blowing_up = True
            self.blowup_frame_index = 0
            self.blowup_frame_counter = 0

    def reset_position(self) -> None:
        self.x = random.randint(0, constants.SCREEN_WIDTH - self.image.get_width())
        self.y = 20
        self.hp = self.max_hp
        self.bullets.clear()
        self.is_blowing_up = False
        self.blowup_frame_index = 0
        self.blowup_frame_counter = 0

