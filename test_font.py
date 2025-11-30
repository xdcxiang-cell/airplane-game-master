import pygame
import sys

# 初始化pygame
pygame.init()

# 设置屏幕
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("中文显示测试")

# 测试不同字体
fonts_to_test = [
    ("/System/Library/Fonts/PingFang.ttc", 72),  # macOS系统字体
    ("msyh.ttc", 72),                          # Windows系统字体
    (None, 72)                                  # 默认字体
]

# 主循环
running = True
font_index = 0
while running:
    screen.fill((0, 0, 0))  # 黑色背景
    
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_SPACE:
                font_index = (font_index + 1) % len(fonts_to_test)
    
    # 获取当前字体
    font_path, font_size = fonts_to_test[font_index]
    
    # 渲染文本
    try:
        font = pygame.font.Font(font_path, font_size)
        text = font.render("测试中文显示: 游戏结束，积分: 12345", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
        
        # 显示当前字体信息
        info_font = pygame.font.Font(None, 24)
        info_text = info_font.render(f"当前字体: {font_path if font_path else '默认字体'}, 按SPACE切换字体，按Q退出", True, (255, 255, 255))
        screen.blit(info_text, (10, 10))
    except Exception as e:
        error_font = pygame.font.Font(None, 24)
        error_text = error_font.render(f"字体加载错误: {e}", True, (255, 0, 0))
        screen.blit(error_text, (10, 10))
    
    # 更新显示
    pygame.display.update()

# 退出pygame
pygame.quit()
sys.exit()