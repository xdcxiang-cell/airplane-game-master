"""Centralised constants for game configuration."""

import pygame

# 屏幕相关常量
SCREEN_WIDTH = 480  # 屏幕宽度
SCREEN_HEIGHT = 650  # 屏幕高度
SCREEN_RECT = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)  # 屏幕矩形区域

# 移动和速度常量
HERO_SPEED = 8  # 英雄飞机移动速度
ENEMY_SPEED = 5  # 敌机默认移动速度（已被ENEMY_TYPES中的speed替代）
BULLET_SPEED = 18  # 英雄子弹速度
ENEMY_BULLET_SPEED = 12  # 敌机子弹速度
ENEMY_SHOOT_ODDS = (10, 20)  # 敌机射击概率（随机数在这个范围内时射击）
FPS = 60  # 游戏帧率

# 玩家相关常量
HERO_LIVES = 5  # 玩家初始生命值
HERO_SHIELD = True  # 玩家初始是否有护盾
SHIELD_RECOVERY_KILLS = 5  # 恢复护盾需要击杀的敌机数量
SCORE_PER_ENEMY = 10  # 默认每架敌机的积分（已被ENEMY_TYPES中的points替代）

# 敌机相关常量
ENEMY_TYPES = {  # 敌机类型及其属性（生命值、速度、积分）
    "type1": {"health": 1, "speed": 5, "points": 10},  # 普通敌机，生命值1，速度5，积分10
    "type2": {"health": 2, "speed": 4, "points": 20},  # 中等敌机，生命值2，速度4，积分20
    "type3": {"health": 3, "speed": 3, "points": 30}   # 强力敌机，生命值3，速度3，积分30
}

# 显示相关常量
HEART_SIZE = 20  # 爱心图标大小（用于显示生命值）
HEART_SPACING = 5  # 爱心图标间距
HEART_TOP_MARGIN = 10  # 爱心图标顶部边距
HEART_LEFT_MARGIN = 10  # 爱心图标左侧边距
SCORE_FONT_SIZE = 24  # 积分显示字体大小
SCORE_TOP_MARGIN = 10  # 积分显示顶部边距
SCORE_RIGHT_MARGIN = 20  # 积分显示右侧边距
SHIELD_FONT_SIZE = 24  # 护盾显示字体大小
SHIELD_TOP_MARGIN = 10  # 护盾显示顶部边距
SHIELD_LEFT_MARGIN = 100  # 护盾显示左侧边距

# 颜色常量
WHITE = (255, 255, 255)  # 白色
RED = (255, 0, 0)  # 红色（用于生命值爱心和血条背景）
GREEN = (0, 255, 0)  # 绿色（用于血条前景）
BLUE = (0, 0, 255)  # 蓝色（用于护盾显示）