import pygame
import random
import sys

from game.assets import load_assets
from game.constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from game.enemy import EnemyPlane
from game.hero import HeroPlane

def test_features():
    """测试游戏功能：游戏结束、敌机血条、积分显示"""
    pygame.init()
    pygame.mixer.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption("飞行大战 - 功能测试")
    assets = load_assets()
    
    # 初始化字体
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    game_over_font = pygame.font.Font(None, 72)
    
    # 创建测试英雄和敌机
    hero = HeroPlane(screen, assets)
    enemy = EnemyPlane(screen, assets, "enemy3")  # 使用生命值高的敌机测试血条
    
    # 设置测试状态
    hero.lives = 1  # 只剩一条命，方便测试游戏结束
    hero.hit = False  # 初始未被击中
    
    clock = pygame.time.Clock()
    
    print("=== 游戏功能测试 ===")
    print("1. 按 SPACE 测试敌机血条显示")
    print("2. 按 H 测试玩家被击中（游戏结束）")
    print("3. 按 Q 退出测试")
    
    running = True
    while running:
        clock.tick(FPS)
        
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # 测试敌机血条：让敌机受到伤害
                    print(f"敌机当前生命值: {enemy.health}")
                    enemy.take_damage(1)
                    print(f"敌机受到伤害后生命值: {enemy.health}")
                elif event.key == pygame.K_h:
                    # 测试游戏结束：玩家被击中
                    hero.take_damage()
                    print("玩家被击中，生命值: {}".format(hero.lives))
        
        # 绘制背景
        screen.blit(assets.background, (0, 0))
        
        # 显示英雄和敌机
        if not hero.hit:
            hero.display()
            enemy.display()
            enemy.move()
            
            # 显示测试信息
            test_text = font.render("按 SPACE 测试敌机血条 | 按 H 测试游戏结束 | 按 Q 退出", True, (255, 255, 255))
            screen.blit(test_text, (10, 10))
            
            # 显示积分
            score_text = font.render(f"积分: {hero.score}", True, (255, 255, 255))
            screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))
            
            # 显示敌机生命值
            enemy_health_text = font.render(f"敌机生命值: {enemy.health}/{enemy.max_health}", True, (255, 255, 255))
            screen.blit(enemy_health_text, (10, 50))
        
        else:
            # 显示游戏结束界面
            game_over_text = game_over_font.render("游戏结束", True, (255, 0, 0))
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - game_over_text.get_height()//2 - 50))
            
            score_text = font.render(f"最终积分: {hero.score}", True, (255, 255, 255))
            screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2 - score_text.get_height()//2 + 20))
            
            instruction_text = font.render("按 Q 退出测试", True, (255, 255, 255))
            screen.blit(instruction_text, (SCREEN_WIDTH//2 - instruction_text.get_width()//2, SCREEN_HEIGHT//2 - instruction_text.get_height()//2 + 100))
        
        pygame.display.update()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    test_features()