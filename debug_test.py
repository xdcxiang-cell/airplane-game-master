import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game.enemy import EnemyPlane
import pygame

# 初始化pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))

# 创建一个模拟的GameAssets类
class MockGameAssets:
    def __init__(self):
        self.enemy1 = pygame.Surface((50, 50))
        self.enemy1_blowup = [pygame.Surface((50, 50))]

# 创建敌机实例
assets = MockGameAssets()
enemy = EnemyPlane(screen, assets, "enemy1")
print(f"Initial: enemy.hit={enemy.hit}, enemy.health={enemy.health}")

# 第一次调用take_damage
result = enemy.take_damage()
print(f"After first take_damage: enemy.hit={enemy.hit}, enemy.health={enemy.health}, result={result}")

# 重置health并再次调用take_damage
enemy.health = 1
result = enemy.take_damage()
print(f"After reset and take_damage: enemy.hit={enemy.hit}, enemy.health={enemy.health}, result={result}")

# 尝试重置hit和health
enemy.hit = False
enemy.health = 1
result = enemy.take_damage()
print(f"After reset hit and health: enemy.hit={enemy.hit}, enemy.health={enemy.health}, result={result}")