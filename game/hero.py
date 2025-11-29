"""Hero plane implementation.

This module defines the HeroPlane class which represents the player's aircraft in the game.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from . import constants
from .bullet import Bullet

if TYPE_CHECKING:
    from .assets import GameAssets


class HeroPlane:
    def __init__(self, screen: pygame.Surface, assets: "GameAssets") -> None:
        """Initialize the hero plane.
        
        Args:
            screen: The pygame surface to draw on.
            assets: The game assets containing images and sounds.
        """
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
        self.lives = 5  # 玩家初始生命值
        self.score = 0  # 玩家得分
        self.font = pygame.font.SysFont("Microsoft YaHei", 36, bold=True)

    @property
    def rect(self) -> pygame.Rect:
        """Get the rectangular bounding box of the hero plane.
        
        Returns:
            A pygame.Rect object representing the hero's position and size.
        """
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def bomb(self) -> None:
        """Handle the hero plane being hit by an enemy bullet.
        
        This method triggers the explosion animation and decreases the player's lives.
        """
        if not self.hit:
            self.hit = True
            self.lives -= 1
            # Play explosion sound
            if self.assets.explode_sound:
                self.assets.explode_sound.play()

    def display(self) -> None:
        """Display the hero plane and its current state on the screen.
        
        This method also displays the player's remaining lives and current score.
        """
        # Display lives and score
        lives_text = self.font.render(f"生命值: {self.lives}", True, (255, 255, 255))
        score_text = self.font.render(f"得分: {self.score}", True, (255, 255, 255))
        self.screen.blit(lives_text, (10, 10))
        self.screen.blit(score_text, (10, 50))

        if self.hit:
            # Display explosion animation
            self.screen.blit(self.bomb_frames[self.bomb_frame_index], (self.x, self.y))
            self.frame_counter += 1
            if self.frame_counter == 7:
                self.frame_counter = 0
                self.bomb_frame_index += 1
            if self.bomb_frame_index >= len(self.bomb_frames):
                # Reset hero position and state after explosion
                self.hit = False
                self.frame_counter = 0
                self.bomb_frame_index = 0
                self.x = constants.SCREEN_WIDTH // 2 - self.image.get_width() // 2
                self.y = constants.SCREEN_HEIGHT - self.image.get_height() - 20
                
                # If no lives left, game over
                if self.lives <= 0:
                    self.game_over()
        else:
            # Display hero plane
            self.screen.blit(self.image, (self.x, self.y))
            
        # Display and move bullets
        for bullet in list(self.bullets):
            bullet.display()
            bullet.move()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

    def game_over(self) -> None:
        """Handle the game over state.
        
        This method displays the game over screen with the final score and
        provides options to restart or quit the game.
        """
        # Play game over sound
        if self.assets.game_over_sound:
            self.assets.game_over_sound.play()
        font = pygame.font.SysFont("Microsoft YaHei", 72, bold=True)
        game_over_text = font.render("游戏结束", True, (255, 0, 0))
        score_text = self.font.render(f"最终得分: {self.score}", True, (255, 255, 255))
        restart_text = self.font.render("按 R 重新开始, Q 退出游戏", True, (255, 255, 255))
        
        # Center the text on the screen
        game_over_rect = game_over_text.get_rect(center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2 - 50))
        score_rect = score_text.get_rect(center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2 + 20))
        restart_rect = restart_text.get_rect(center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2 + 80))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)
        pygame.display.update()
        
        # Wait for user input
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Restart game
                        self.__init__(self.screen, self.assets)
                        return
                    if event.key == pygame.K_q:
                        pygame.quit()
                        raise SystemExit

    def move_left(self) -> None:
        """Move the hero plane to the left."""
        if self.x > constants.SCREEN_RECT.left:
            self.x = max(self.x - constants.HERO_SPEED, constants.SCREEN_RECT.left)

    def move_right(self) -> None:
        """Move the hero plane to the right."""
        max_x = constants.SCREEN_RECT.right - self.image.get_width()
        if self.x < max_x:
            self.x = min(self.x + constants.HERO_SPEED, max_x)

    def shoot(self) -> None:
        """Shoot a bullet from the hero plane."""
        if self.hit:
            return
        self.bullets.append(Bullet(self.x, self.y, self.screen, self.assets.bullet))
        # Play shoot sound
        if self.assets.shoot_sound:
            self.assets.shoot_sound.play()