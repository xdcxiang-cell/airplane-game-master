import pygame
import random
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from game.assets import load_assets
from game.collision import handle_collisions
from game.constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from game.enemy import EnemyPlane
from game.hero import HeroPlane
from game.input_handler import key_control


def main() -> None:
    """游戏主函数，初始化游戏并运行主循环"""
    try:
        logger.info("游戏初始化开始")
        pygame.init()
        logger.info("Pygame初始化完成")
        
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        pygame.display.set_caption("飞行大战")
        logger.info("游戏窗口创建完成")
        
        assets = load_assets()
        logger.info("游戏资源加载完成")

        clock = pygame.time.Clock()
        hero = HeroPlane(screen, assets)
        logger.info("英雄飞机初始化完成")
        
        # 敌机波次管理
        current_wave = 1  # 当前波次
        enemies: list[EnemyPlane] = []  # 敌机列表
        max_enemies_per_wave = 5  # 每波最大敌机数量
        enemy_spawn_interval = 2000  # 敌机生成间隔（毫秒）
        last_spawn_time = pygame.time.get_ticks()  # 上次生成敌机时间
        wave_started = False  # 当前波次是否已经开始
        logger.info(f"波次管理初始化完成: 当前波次={current_wave}, 最大敌机数量={max_enemies_per_wave}")
        
        def spawn_enemy() -> None:
            """生成一架敌机，根据当前波次选择敌机类型"""
            nonlocal wave_started
            # 根据波次选择敌机类型，波次越高，敌机类型越丰富
            if current_wave <= 3:
                enemy_types = ["type1"]  # 前3波只有type1敌机
            elif current_wave <= 6:
                enemy_types = ["type1", "type2"]  # 4-6波添加type2敌机
            else:
                enemy_types = ["type1", "type2", "type3"]  # 7波及以上添加type3敌机
            
            enemy_type = random.choice(enemy_types)
            enemy = EnemyPlane(screen, assets, enemy_type)
            enemies.append(enemy)
            logger.info(f"生成敌机: 类型={enemy_type}, 位置=({enemy.x}, {enemy.y}), 生命值={enemy.health}")
            # 如果是当前波次的第一架敌机，标记波次已经开始
            if not wave_started:
                wave_started = True
                logger.info(f"波次 {current_wave} 开始")

        def check_wave_completion() -> bool:
            """检查当前波次是否完成"""
            nonlocal current_wave, max_enemies_per_wave, enemy_spawn_interval, last_spawn_time, wave_started
            if len(enemies) == 0 and max_enemies_per_wave > 0 and wave_started:
                # 波次完成，准备下一波
                current_wave += 1
                max_enemies_per_wave = min(max_enemies_per_wave + 2, 10)  # 每波增加2架敌机，最多10架
                enemy_spawn_interval = max(enemy_spawn_interval - 100, 500)  # 每波减少100ms生成间隔，最少500ms
                last_spawn_time = pygame.time.get_ticks()
                # 生成新波次的第一架敌机
                spawn_enemy()
                return True
            return False

        running = True
        while running:
            clock.tick(FPS)
            screen.blit(assets.background, (0, 0))
            
            # 生成敌机
            current_time = pygame.time.get_ticks()
            if len(enemies) < max_enemies_per_wave and current_time - last_spawn_time > enemy_spawn_interval:
                spawn_enemy()
                last_spawn_time = current_time
            
            # 检查波次完成情况
            check_wave_completion()
            
            # 打印调试信息
            print(f"当前波次: {current_wave}, 敌机数量: {len(enemies)}, 最大敌机数量: {max_enemies_per_wave}")
            for enemy in enemies:
                print(f"敌机位置: ({enemy.x}, {enemy.y}), 生命值: {enemy.health}, 状态: {enemy.is_alive}")
            
            # 事件处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_r and hero.lives <= 0:
                        # 重新开始游戏
                        logger.info("重新开始游戏")
                        hero = HeroPlane(screen, assets)
                        enemies.clear()
                        current_wave = 1
                        max_enemies_per_wave = 5
                        enemy_spawn_interval = 2000
                        last_spawn_time = pygame.time.get_ticks()
            
            # 游戏逻辑处理
            key_control(hero)
            
            # 游戏结束判断
            if hero.lives <= 0:
                # 显示游戏结束文字
                font = pygame.font.SysFont(None, 72)
                game_over_text = font.render("游戏结束", True, (255, 0, 0))
                restart_text = font.render("按R重新开始", True, (255, 255, 255))
                quit_text = font.render("按Q退出游戏", True, (255, 255, 255))
                
                # 计算文字位置（居中）
                game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 100))
                restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
                quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 100))
                
                # 绘制文字
                screen.blit(game_over_text, game_over_rect)
                screen.blit(restart_text, restart_rect)
                screen.blit(quit_text, quit_rect)
                logger.info("游戏结束，显示重新开始和退出选项")
            else:
                # 游戏正常运行
                hero.display()
                
                # 绘制敌机
                for enemy in enemies[:]:
                    enemy.move()
                    enemy.shoot()
                    if not enemy.is_alive:
                        enemies.remove(enemy)
                
                # 碰撞检测
                for enemy in enemies:
                    handle_collisions(hero, enemy)
            
            pygame.display.update()
        
        pygame.quit()
        logger.info("游戏退出")
    except Exception as e:
        logger.error(f"游戏发生错误: {e}", exc_info=True)
    finally:
        pygame.quit()
        logger.info("游戏资源释放完成")


if __name__ == "__main__":
    main()