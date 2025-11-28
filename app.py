import pygame

from game.assets import load_assets
from game.collision import handle_collisions
from game.constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from game.enemy import EnemyPlane
from game.hero import HeroPlane
from game.input_handler import key_control


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption("飞行大战")
    assets = load_assets()

    clock = pygame.time.Clock()
    hero = HeroPlane(screen, assets)
    enemy = EnemyPlane(screen, assets)

    while True:
        clock.tick(FPS)
        screen.blit(assets.background, (0, 0))

        hero.display()
        enemy.display()
        enemy.move()
        enemy.shoot()
        handle_collisions(hero, enemy)
        key_control(hero)

        pygame.display.update()


if __name__ == "__main__":
    main()
