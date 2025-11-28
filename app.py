import pygame

from game.assets import load_assets
from game.collision import handle_collisions
from game.constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH, HERO_MAX_HP, FONT_SIZE, UI_MARGIN, UI_COLOR, UI_BACKGROUND
from game.enemy import EnemyPlane
from game.hero import HeroPlane
from game.input_handler import key_control


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption("飞行大战")
    assets = load_assets()

    # Initialize font for UI
    pygame.font.init()
    font = pygame.font.SysFont("arial", FONT_SIZE)

    clock = pygame.time.Clock()
    hero = HeroPlane(screen, assets)
    enemies = [
        EnemyPlane(screen, assets, enemy_type=0),
        EnemyPlane(screen, assets, enemy_type=1),
        EnemyPlane(screen, assets, enemy_type=2),
    ]

    while True:
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds
        screen.blit(assets.background, (0, 0))

        hero.display()
        for enemy in enemies:
            enemy.display()
            enemy.move(dt)
            enemy.shoot()
        handle_collisions(hero, enemies)
        key_control(hero, dt)

        # Display UI
        # Health bar
        health_text = font.render(f"Health: {hero.hp}/{HERO_MAX_HP}", True, UI_COLOR)
        health_surf = pygame.Surface((health_text.get_width() + 4, health_text.get_height() + 4), pygame.SRCALPHA)
        health_surf.fill(UI_BACKGROUND)
        screen.blit(health_surf, (UI_MARGIN, UI_MARGIN))
        screen.blit(health_text, (UI_MARGIN + 2, UI_MARGIN + 2))

        # Score
        score_text = font.render(f"Score: {hero.score}", True, UI_COLOR)
        score_surf = pygame.Surface((score_text.get_width() + 4, score_text.get_height() + 4), pygame.SRCALPHA)
        score_surf.fill(UI_BACKGROUND)
        screen.blit(score_surf, (SCREEN_WIDTH - score_text.get_width() - UI_MARGIN - 4, UI_MARGIN))
        screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - UI_MARGIN - 2, UI_MARGIN + 2))

        # Enemy health bars
        for enemy in enemies:
            if not enemy.is_blowing_up:
                bar_width = enemy.image.get_width()
                bar_height = 5
                bar_x = enemy.x
                bar_y = enemy.y - bar_height - 5
                health_ratio = enemy.hp / enemy.max_hp

                # Background bar
                pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
                # Health bar
                pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))

        # Game over screen
        if hero.game_over:
            game_over_text = font.render("Game Over! Score: {}".format(hero.score), True, (255, 0, 0))
            restart_text = font.render("Press R to restart, Q to quit", True, UI_COLOR)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2))

            # Check for restart or quit
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_r]:
                hero = HeroPlane(screen, assets)
                enemies = [
                    EnemyPlane(screen, assets, enemy_type=0),
                    EnemyPlane(screen, assets, enemy_type=1),
                    EnemyPlane(screen, assets, enemy_type=2),
                ]
            elif pressed[pygame.K_q]:
                pygame.quit()
                raise SystemExit

        pygame.display.update()


if __name__ == "__main__":
    main()
