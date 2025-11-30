"""主游戏入口文件，处理游戏初始化、循环和主要逻辑。"""
import pygame
import random

from game.assets import load_assets
from game.collision import handle_collisions
from game.constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from game.enemy import EnemyPlane
from game.hero import HeroPlane
from game.input_handler import key_control


def main() -> None:
    """主函数，初始化游戏并启动主循环。"""
    # 初始化Pygame
    pygame.init()
    # 初始化音效系统
    pygame.mixer.init()
    
    # 设置游戏窗口
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption("飞行大战")
    # 加载游戏资源
    assets = load_assets()
    
    # 加载音效文件
    shoot_effect = pygame.mixer.Sound(assets.shoot_sound)
    explosion_effect = pygame.mixer.Sound(assets.explosion_sound)
    
    # 播放背景音乐（无限循环）
    pygame.mixer.music.load(assets.main_music)
    pygame.mixer.music.set_volume(0.5)  # 设置音量为50%
    pygame.mixer.music.play(-1)

    # 初始化游戏时钟（控制帧率）
    clock = pygame.time.Clock()
    # 创建玩家飞机
    hero = HeroPlane(screen, assets)
    # 敌机列表
    enemies: list[EnemyPlane] = []
    # 波次计数器
    wave = 1
    # 每波最大敌机数量
    max_enemies_per_wave = 5
    # 敌机生成计时器
    enemy_spawn_timer = 0
    # 敌机生成间隔（毫秒）
    enemy_spawn_interval = 1500

    # 加载生命值和护盾图标
    heart_icon = pygame.image.load("./feiji/prop_type_1.png")
    heart_icon = pygame.transform.scale(heart_icon, (30, 30))
    shield_icon = pygame.image.load("./feiji/prop_type_0.png")
    shield_icon = pygame.transform.scale(shield_icon, (30, 30))

    # 初始化字体系统
    pygame.font.init()
    # 创建字体对象（使用支持中文的字体，优先使用系统字体）
    try:
        # macOS系统使用PingFang SC字体
        font = pygame.font.Font("/System/Library/Fonts/PingFang.ttc", 24)
    except FileNotFoundError:
        try:
            # Windows系统使用微软雅黑
            font = pygame.font.Font("msyh.ttc", 24)
        except FileNotFoundError:
            # 回退到默认字体
            font = pygame.font.Font(None, 24)

    # 游戏状态
    game_state = "playing"  # playing, game_over, main_menu
    
    # 游戏主循环
    while True:
        # 控制游戏帧率
        clock.tick(FPS)
        
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and game_state == "game_over":
                if event.key == pygame.K_r:
                    # 重新开始游戏
                    hero = HeroPlane(screen, assets)
                    enemies: list[EnemyPlane] = []
                    wave = 1
                    max_enemies_per_wave = 5
                    enemy_spawn_timer = 0
                    enemy_spawn_interval = 1500
                    game_state = "playing"
                elif event.key == pygame.K_q:
                    # 退出游戏
                    pygame.quit()
                    return
        
        # 绘制背景
        screen.blit(assets.background, (0, 0))
        
        if game_state == "playing":
            # 生成敌机
            enemy_spawn_timer += clock.get_time()
            if len(enemies) < max_enemies_per_wave and enemy_spawn_timer > enemy_spawn_interval:
                # 随机选择敌机类型（enemy1出现概率最高，enemy3最低）
                enemy_type = random.choice(["enemy1", "enemy1", "enemy1", "enemy2", "enemy2", "enemy3"])
                enemies.append(EnemyPlane(screen, assets, enemy_type))
                enemy_spawn_timer = 0

            # 显示玩家飞机
            hero.display()
            
            # 检查玩家是否被摧毁
            if hero.hit:
                game_state = "game_over"
                continue

            # 显示和移动所有敌机
            for enemy in list(enemies):
                enemy.display()
                enemy.move()
                enemy.shoot()
                # 检查敌机是否被摧毁
                if enemy.is_destroyed():
                    enemies.remove(enemy)
                    
                    # 检查是否需要刷新波次
                    if len(enemies) == 0:
                        wave += 1
                        # 增加每波最大敌机数量（最多15架）
                        max_enemies_per_wave = min(max_enemies_per_wave + 2, 15)
                        # 缩短敌机生成间隔（最少500毫秒）
                        enemy_spawn_interval = max(enemy_spawn_interval - 100, 500)

            # 处理碰撞检测
            handle_collisions(hero, enemies, explosion_effect)

            # 显示生命值
            for i in range(hero.lives):
                screen.blit(heart_icon, (10 + i * 35, 10))
            
            # 显示护盾
            if hero.shield:
                screen.blit(shield_icon, (10 + hero.lives * 35, 10))
            
            # 显示积分
            score_text = font.render(f"积分: {hero.score}", True, (255, 255, 255))
            screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))

            # 显示波次
            wave_text = font.render(f"波次: {wave}", True, (255, 255, 255))
            screen.blit(wave_text, (10, SCREEN_HEIGHT - wave_text.get_height() - 10))

            # 处理玩家输入
            key_control(hero, shoot_effect)
        
        elif game_state == "game_over":
            # 显示游戏结束界面
            try:
                game_over_font = pygame.font.Font("/System/Library/Fonts/PingFang.ttc", 72)
                score_font = pygame.font.Font("/System/Library/Fonts/PingFang.ttc", 48)
                instruction_font = pygame.font.Font("/System/Library/Fonts/PingFang.ttc", 36)
            except FileNotFoundError:
                try:
                    game_over_font = pygame.font.Font("msyh.ttc", 72)
                    score_font = pygame.font.Font("msyh.ttc", 48)
                    instruction_font = pygame.font.Font("msyh.ttc", 36)
                except FileNotFoundError:
                    game_over_font = pygame.font.Font(None, 72)
                    score_font = pygame.font.Font(None, 48)
                    instruction_font = pygame.font.Font(None, 36)
            
            game_over_text = game_over_font.render("游戏结束", True, (255, 0, 0))
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - game_over_text.get_height()//2 - 50))
            
            score_text = score_font.render(f"最终积分: {hero.score}", True, (255, 255, 255))
            screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2 - score_text.get_height()//2 + 20))
            restart_text = instruction_font.render("按 R 重新开始", True, (255, 255, 255))
            quit_text = instruction_font.render("按 Q 退出游戏", True, (255, 255, 255))
            screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 - restart_text.get_height()//2 + 100))
            screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, SCREEN_HEIGHT//2 - quit_text.get_height()//2 + 150))

        # 更新游戏显示
        pygame.display.update()


if __name__ == "__main__":
    main()
