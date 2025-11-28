"""Hero plane implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from . import constants
from .bullet import Bullet
from .language import LanguageManager

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
        self.game_over = False  # Track if game over screen should be shown
        self.bomb_frames = assets.hero_blowup
        self.frame_counter = 0
        self.bomb_frame_index = 0
        
        # Health and score
        self.max_hp = constants.HERO_INITIAL_HP
        self.current_hp = self.max_hp
        self.score = 0
        
        # Language support
        self.language_manager = LanguageManager(constants.DEFAULT_LANGUAGE)
        
        # Fonts for UI display
        self.font = pygame.font.SysFont(None, constants.SCORE_FONT_SIZE)
        self.game_over_font = pygame.font.SysFont(None, constants.GAME_OVER_FONT_SIZE)
        self.game_over_score_font = pygame.font.SysFont(None, constants.GAME_OVER_SCORE_FONT_SIZE)
        self.button_font = pygame.font.SysFont(None, constants.BUTTON_FONT_SIZE)

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def bomb(self) -> None:
        self.hit = True
        self.game_over = False  # Track if game over screen should be shown

    def display(self) -> None:
        if self.hit:
            self.screen.blit(self.bomb_frames[self.bomb_frame_index], (self.x, self.y))
            self.frame_counter += 1
            if self.frame_counter == 7:
                self.frame_counter = 0
                self.bomb_frame_index += 1
            if self.bomb_frame_index >= len(self.bomb_frames):
                self.game_over = True
                self.bomb_frame_index = 0  # Reset to prevent index error in subsequent calls
        else:
            self.screen.blit(self.image, (self.x, self.y))
        
        # Display UI elements
        self.display_ui()
        
        # Display bullets
        for bullet in list(self.bullets):
            bullet.display()
            bullet.move()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)
        
        # Display game over screen if needed
        if self.game_over:
            self.display_game_over()

    def display_ui(self) -> None:
        """Display hero's HP and score on the screen."""
        # Display score
        score_text = self.language_manager.translate('score') + f": {self.score}"
        score_surface = self.font.render(score_text, True, (255, 255, 255))  # White text
        self.screen.blit(score_surface, constants.SCORE_POSITION)
        
        # Display HP
        hp_text = self.language_manager.translate('hp') + f": {self.current_hp}/{self.max_hp}"
        hp_surface = self.font.render(hp_text, True, (255, 255, 255))  # White text
        self.screen.blit(hp_surface, constants.HP_POSITION)

    def move_left(self, dt: float = 1.0) -> None:
        if self.hit:
            return
        
        self.x = max(self.x - constants.HERO_SPEED * dt, constants.SCREEN_RECT.left)

    def move_right(self, dt: float = 1.0) -> None:
        if self.hit:
            return
        
        max_x = constants.SCREEN_RECT.right - self.image.get_width()
        self.x = min(self.x + constants.HERO_SPEED * dt, max_x)

    def shoot(self) -> None:
        if self.hit:
            return
        self.bullets.append(Bullet(self.x, self.y, self.screen, self.assets.bullet))

    def take_damage(self, damage: int = 1) -> None:
        """Hero takes damage."""
        if self.hit:
            return
        
        self.current_hp -= damage
        if self.current_hp <= 0:
            self.bomb()  # Trigger explosion and game over

    def add_score(self, points: int = 100) -> None:
        """Add points to hero's score."""
        self.score += points

    def restart(self) -> None:
        """Restart the game by resetting hero state."""
        self.hit = False
        self.game_over = False
        self.frame_counter = 0
        self.bomb_frame_index = 0
        self.max_hp = constants.HERO_INITIAL_HP
        self.current_hp = self.max_hp
        self.score = 0
        self.x = constants.SCREEN_WIDTH // 2 - self.image.get_width() // 2
        self.y = constants.SCREEN_HEIGHT - self.image.get_height() - 20
        self.bullets.clear()

    def display_game_over(self) -> None:
        """Display game over screen with restart and quit options."""
        # Create a semi-transparent overlay
        overlay = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)  # Semi-transparent
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.game_over_font.render(self.language_manager.translate('game_over'), True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(constants.SCREEN_WIDTH//2, constants.SCREEN_HEIGHT//2 - 100))
        self.screen.blit(game_over_text, text_rect)
        
        # Score text
        score_text = self.game_over_score_font.render(f"{self.language_manager.translate('final_score')}: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(constants.SCREEN_WIDTH//2, constants.SCREEN_HEIGHT//2))
        self.screen.blit(score_text, score_rect)
        
        # Restart button
        restart_text = self.button_font.render(self.language_manager.translate('restart'), True, (255, 255, 255))
        self.restart_button = pygame.Rect(constants.SCREEN_WIDTH//2 - 60, constants.SCREEN_HEIGHT//2 + 50, 120, 50)
        pygame.draw.rect(self.screen, (0, 200, 0), self.restart_button)
        self.screen.blit(restart_text, (self.restart_button.centerx - restart_text.get_width()//2, self.restart_button.centery - restart_text.get_height()//2))
        
        # Quit button
        quit_text = self.button_font.render(self.language_manager.translate('quit'), True, (255, 255, 255))
        self.quit_button = pygame.Rect(constants.SCREEN_WIDTH//2 - 60, constants.SCREEN_HEIGHT//2 + 120, 120, 50)
        pygame.draw.rect(self.screen, (200, 0, 0), self.quit_button)
        self.screen.blit(quit_text, (self.quit_button.centerx - quit_text.get_width()//2, self.quit_button.centery - quit_text.get_height()//2))

