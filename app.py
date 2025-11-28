import pygame
import random
from typing import List

from game.assets import load_assets
from game.collision import handle_collisions
from game.constants import (
    FPS, SCREEN_HEIGHT, SCREEN_WIDTH,
    ENEMY_SPAWN_INTERVAL, ENEMY_MAX_ON_SCREEN,
    ENEMY_TYPES
)
from game.enemy import EnemyPlane
from game.hero import HeroPlane
from game.input_handler import key_control


def reset_game(screen, assets) -> tuple[HeroPlane, List[EnemyPlane], int]:
    """Reset the game state for a new game."""
    hero = HeroPlane(screen, assets)
    enemies: List[EnemyPlane] = []
    last_enemy_spawn_time = pygame.time.get_ticks()
    return hero, enemies, last_enemy_spawn_time


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption("飞行大战")
    assets = load_assets()

    clock = pygame.time.Clock()
    hero, enemies, last_enemy_spawn_time = reset_game(screen, assets)

    while True:
        # Calculate delta time
        dt = clock.tick(FPS) / 1000.0  # Convert milliseconds to seconds
        screen.blit(assets.background, (0, 0))
        
        # Spawn new enemies
        current_time = pygame.time.get_ticks()
        if (current_time - last_enemy_spawn_time >= ENEMY_SPAWN_INTERVAL and 
            len(enemies) < ENEMY_MAX_ON_SCREEN):
            
            # Choose a random enemy type
            enemy_types = list(ENEMY_TYPES.keys())
            enemy_type = random.choice(enemy_types)
            
            # Create new enemy
            new_enemy = EnemyPlane(screen, assets, enemy_type)
            enemies.append(new_enemy)
            
            # Update spawn time
            last_enemy_spawn_time = current_time
        
        # Update and display hero
        hero.display()
        key_control(hero, dt)
        
        # Handle game over screen interactions
        if hasattr(hero, 'game_over') and hero.game_over:
            # Check for button clicks
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = pygame.mouse.get_pressed()[0]
            
            if mouse_clicked:
                # Check restart button
                if hasattr(hero, 'restart_button') and hero.restart_button.collidepoint(mouse_pos):
                    # Reset game
                    hero, enemies, last_enemy_spawn_time = reset_game(screen, assets)
                # Check quit button
                elif hasattr(hero, 'quit_button') and hero.quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    return
        
        # Update and display enemies
        enemies_to_remove = []
        for enemy in enemies:
            if enemy.is_alive:
                enemy.display()
                enemy.move(dt)
                enemy.shoot()
            else:
                # Remove dead enemies after a delay (add explosion animation here)
                enemies_to_remove.append(enemy)
        
        # Remove dead enemies
        for enemy in enemies_to_remove:
            enemies.remove(enemy)
        
        # Handle collisions
        handle_collisions(hero, enemies)

        pygame.display.update()


if __name__ == "__main__":
    main()
