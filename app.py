import pygame
import sys
import random
sys.path.append('game')
import constants

from game.assets import load_assets
from game.collision import handle_collisions
from game.constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH, ENEMY_MAX_COUNT, ENEMY_SPAWN_RATE
from game.enemy import EnemyPlane
from game.hero import HeroPlane
from game.input_handler import key_control
from game.language import LanguageManager


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption("飞行大战")
    assets = load_assets()
    
    # Set up font for displaying health and score
    pygame.font.init()
    font = pygame.font.SysFont("SimHei", 24)
    large_font = pygame.font.SysFont("SimHei", 48)
    instruction_font = pygame.font.SysFont("SimHei", 20)

    # Initialize language manager
    lang_manager = LanguageManager()

    clock = pygame.time.Clock()
    hero = HeroPlane(screen, assets)
    enemies: list[EnemyPlane] = []
    frame_count = 0
    game_over = False

    while True:
        dt = clock.tick(FPS) / 1000  # Delta time in seconds
        screen.blit(assets.background, (0, 0))

        # Spawn new enemies periodically
        frame_count += 1
        if frame_count % ENEMY_SPAWN_RATE == 0 and len(enemies) < ENEMY_MAX_COUNT:
            enemy_type = random.randint(0, 2)
            new_enemy = EnemyPlane(screen, assets, enemy_type)
            new_enemy.reset_position()  # Randomize position
            enemies.append(new_enemy)

        # Update and display all enemies
        for enemy in list(enemies):
            enemy.display()
            enemy.move()
            enemy.shoot()
            
            # Draw health bar if enemy is not exploding
            if not enemy.exploding:
                max_health = constants.ENEMY_HEALTH[enemy.enemy_type]
                health_percent = enemy.health / max_health
                bar_width = enemy.image.get_width()
                bar_height = 5
                
                # Draw background bar
                pygame.draw.rect(screen, (255, 0, 0), 
                               (enemy.x, enemy.y - bar_height - 2, 
                                bar_width, bar_height))
                
                # Draw health bar
                pygame.draw.rect(screen, (0, 255, 0), 
                               (enemy.x, enemy.y - bar_height - 2, 
                                bar_width * health_percent, bar_height))
            
            # Remove enemies that have finished exploding
            if enemy.exploding and enemy.explosion_frame_index >= len(enemy.explosion_frames):
                enemies.remove(enemy)

        # Check if game over
        if hero.health <= 0:
            game_over = True

        if not game_over:
            # Update and display hero
            hero.display()
            handle_collisions(hero, enemies)
            key_control(hero)

            # Display health and score using language manager
            health_text = font.render(lang_manager.get_text('health', hero.health), True, (255, 255, 255))
            score_text = font.render(lang_manager.get_text('score', hero.score), True, (255, 255, 255))
            screen.blit(health_text, (10, 10))
            screen.blit(score_text, (SCREEN_WIDTH - 100, 10))

            # Display instructions
            instruction_text = instruction_font.render(lang_manager.get_text('instructions'), True, (255, 255, 255))
            screen.blit(instruction_text, (10, SCREEN_HEIGHT - 30))
        else:
            # Display game over screen
            game_over_text = large_font.render(lang_manager.get_text('game_over'), True, (255, 0, 0))
            final_score_text = font.render(lang_manager.get_text('final_score', hero.score), True, (255, 255, 255))
            play_again_text = font.render(lang_manager.get_text('play_again'), True, (255, 255, 255))
            quit_text = font.render(lang_manager.get_text('quit'), True, (255, 255, 255))
            
            # Center the text
            screen.blit(game_over_text, (SCREEN_WIDTH/2 - game_over_text.get_width()/2, SCREEN_HEIGHT/2 - 100))
            screen.blit(final_score_text, (SCREEN_WIDTH/2 - final_score_text.get_width()/2, SCREEN_HEIGHT/2 - 40))
            screen.blit(play_again_text, (SCREEN_WIDTH/2 - play_again_text.get_width()/2, SCREEN_HEIGHT/2 + 20))
            screen.blit(quit_text, (SCREEN_WIDTH/2 - quit_text.get_width()/2, SCREEN_HEIGHT/2 + 60))

            # Handle game over input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                # Reset game
                hero = HeroPlane(screen, assets)
                enemies.clear()
                frame_count = 0
                game_over = False
            elif keys[pygame.K_q]:
                # Quit game
                pygame.quit()
                sys.exit()

        pygame.display.update()
        
        # Handle language toggle
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    lang_manager.toggle_language()
                    # Update window caption
                    pygame.display.set_caption(lang_manager.get_text('title'))


if __name__ == "__main__":
    main()
