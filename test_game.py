import pygame
import random
import sys

from game.assets import load_assets
from game.collision import handle_collisions
from game.constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from game.enemy import EnemyPlane
from game.hero import HeroPlane
from game.input_handler import key_control

def test_game():
    """测试游戏运行，检查界面问题"""
    pygame.init()
    pygame.mixer.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption("飞行大战")
    assets = load_assets()
    
    # 测试字体显示
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    
    # 创建测试文本
    text1 = font.render("测试中文显示", True, (255, 255, 255))
    text2 = font.render("Score: 12345", True, (255, 255, 255))
    
    # 绘制测试界面
    screen.blit(assets.background, (0, 0))
    screen.blit(text1, (50, 50))
    screen.blit(text2, (50, 100))
    
    # 创建敌机测试血条显示
    enemy = EnemyPlane(screen, assets, "enemy1")
    enemy.display()
    
    pygame.display.update()
    
    # 等待用户关闭窗口
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    test_game()