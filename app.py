import argparse
import pygame
import random

from game.assets import load_assets
from game.collision import handle_collisions
from game.constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from game.enemy import EnemyPlane, EnemyPlaneType1
from game.hero import HeroPlane
from game.input_handler import key_control


def main() -> None:
    parser = argparse.ArgumentParser(description='Airplane Game')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()
    DEBUG = args.debug
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption("飞行大战")
    assets = load_assets()

    clock = pygame.time.Clock()
    hero = HeroPlane(screen, assets)
    enemies = []

    # 生成初始波敌人
    for _ in range(3):
        # 随机选择敌人类型
        if random.random() < 0.5:
            enemy = EnemyPlane(screen, assets)
        else:
            enemy = EnemyPlaneType1(screen, assets)
        enemy.x = random.randint(0, SCREEN_WIDTH - enemy.image.get_width())
        enemies.append(enemy)

    while True:
        clock.tick(FPS)
        screen.blit(assets.background, (0, 0))

        hero.display()
        
        # 显示并移动所有敌人
        for enemy in list(enemies):
            enemy.display()
            enemy.move()
            enemy.shoot()
            
            # 如果敌人超出屏幕则移除
            if enemy.y > SCREEN_HEIGHT:
                enemies.remove(enemy)

        # 处理碰撞
        handle_collisions(hero, enemies)
        key_control(hero)

        # 如果所有敌人都被消灭，生成新的一波
        if not enemies:
            for _ in range(3):
                if random.random() < 0.5:
                    enemy = EnemyPlane(screen, assets)
                else:
                    enemy = EnemyPlaneType1(screen, assets)
                enemy.x = random.randint(0, SCREEN_WIDTH - enemy.image.get_width())
                enemies.append(enemy)

        # Debug information
        if DEBUG:
            font = pygame.font.SysFont("Microsoft YaHei", 24)
            debug_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
            screen.blit(debug_text, (SCREEN_WIDTH - 100, 10))
            debug_text = font.render(f"Enemies: {len(enemies)}", True, (255, 255, 255))
            screen.blit(debug_text, (SCREEN_WIDTH - 100, 40))

        pygame.display.update()


if __name__ == "__main__":
    main()

