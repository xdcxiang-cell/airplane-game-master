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
        
        # Game state attributes
        self.hp = constants.HERO_INITIAL_HP
        self.score = 0
        self.hit = False
        self.invincible = False
        self.invincible_timer = 0
        
        # Animation attributes
        self.bomb_frames = assets.hero_blowup
        self.frame_counter = 0
        self.bomb_frame_index = 0

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def take_damage(self, amount: int = 1) -> None:
        """Handle hero taking damage with invincibility frames."""
        if self.invincible or self.hit:
            return
        
        self.hp -= amount
        if self.hp <= 0:
            self.hit = True
        else:
            # Activate invincibility frames
            self.invincible = True
            self.invincible_timer = constants.HERO_INVINCIBLE_DURATION

    def update_invincibility(self) -> None:
        """Update invincibility timer and state."""
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

    def display(self, dt: float = 1.0) -> None:
        self.update_invincibility()
        
        if self.hit:
            # Show explosion animation
            self.screen.blit(self.bomb_frames[self.bomb_frame_index], (self.x, self.y))
            self.frame_counter += 1
            if self.frame_counter == 7:
                self.frame_counter = 0
                self.bomb_frame_index += 1
            if self.bomb_frame_index >= len(self.bomb_frames):
                # Game over - display final score
                font = pygame.font.Font(None, 48)
                game_over_text = font.render("Game Over", True, (255, 0, 0))
                score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
                self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
                self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
                pygame.display.update()
                pygame.time.wait(3000)
                pygame.quit()
                raise SystemExit
        else:
            # Blink hero when invincible
            if not self.invincible or (self.invincible and pygame.time.get_ticks() % 100 < 50):
                self.screen.blit(self.image, (self.x, self.y))
        
        # Update bullets
        for bullet in list(self.bullets):
            bullet.display()
            bullet.move(dt)
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

    def add_score(self, points: int) -> None:
        """Add points to hero's score."""
        self.score += points

    def move_left(self, dt: float = 1.0) -> None:
        if self.x > constants.SCREEN_RECT.left and not self.hit:
            self.x -= constants.HERO_SPEED * dt

    def move_right(self, dt: float = 1.0) -> None:
        max_x = constants.SCREEN_RECT.right - self.image.get_width()
        if self.x < max_x and not self.hit:
            self.x += constants.HERO_SPEED * dt

    def shoot(self) -> None:
        if self.hit:
            return
        self.bullets.append(Bullet(self.x, self.y, self.screen, self.assets.bullet))

