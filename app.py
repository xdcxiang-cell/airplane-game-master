import pygame
import random

from game.assets import load_assets
from game.collision import handle_collisions
from game.constants import (
    FPS, SCREEN_HEIGHT, SCREEN_WIDTH, ENEMY_SPAWN_RATE,
    FONT_SIZE, FONT_COLOR, FONT_SHADOW_COLOR
)
from game.enemy import EnemyPlane
from game.hero import HeroPlane
from game.input_handler import key_control


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption("飞行大战")
    assets = load_assets()
    
    # Initialize font for displaying score and health
    pygame.font.init()
    font = pygame.font.Font(None, FONT_SIZE)

    clock = pygame.time.Clock()
    hero = HeroPlane(screen, assets)
    enemies: list[EnemyPlane] = []
    enemy_spawn_timer = 0

    while True:
        # Calculate delta time for frame rate independence
        dt = clock.tick(FPS) / 1000.0  # Convert ms to seconds
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not hero.hit:
                    hero.shoot()

        screen.blit(assets.background, (0, 0))

        # Spawn new enemies periodically
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= ENEMY_SPAWN_RATE:
            enemy_spawn_timer = 0
            # Randomly choose enemy type (small: 70%, medium: 20%, large: 10%)
            enemy_type = random.choices(
                ["small", "medium", "large"], 
                weights=[0.7, 0.2, 0.1]
            )[0]
            enemies.append(EnemyPlane(screen, assets, enemy_type))

        # Update and display hero
        hero.display(dt)
        
        # Update and display enemies
        for enemy in list(enemies):
            enemy.display(dt)
            enemy.move(dt)
            enemy.shoot()
            # Remove enemies that are off screen or destroyed
            if enemy.is_off_screen() or (enemy.destroyed and enemy.animation_frame >= len(enemy.assets.enemy_small_explosion if enemy.enemy_type == "small" else enemy.assets.enemy_medium_explosion if enemy.enemy_type == "medium" else enemy.assets.enemy_large_explosion)):
                enemies.remove(enemy)

        # Handle collisions
        handle_collisions(hero, enemies)
        
        # Handle user input
        key_control(hero, dt)
        
        # Display score and health
        # Draw shadow for better readability
        score_text_shadow = font.render(f"Score: {hero.score}", True, FONT_SHADOW_COLOR)
        health_text_shadow = font.render(f"HP: {hero.hp}", True, FONT_SHADOW_COLOR)
        screen.blit(score_text_shadow, (12, 12))
        screen.blit(health_text_shadow, (SCREEN_WIDTH - 72, 12))
        
        # Draw actual text
        score_text = font.render(f"Score: {hero.score}", True, FONT_COLOR)
        health_text = font.render(f"HP: {hero.hp}", True, FONT_COLOR)
        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (SCREEN_WIDTH - 70, 10))

        pygame.display.update()


if __name__ == "__main__":
    main()
