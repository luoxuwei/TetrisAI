# coding: utf-8
# author: 罗旭维
# date: 2023-08-12

import pygame
import sys
from config import *

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 训练设置

#横竖多少个俄罗斯方块游戏在训练
ROW_COUNT = 4
COL_COUNT = 10
GAME_COUNT = ROW_COUNT * COL_COUNT #固定逻辑不要修改

#每个俄罗斯游戏显示的区域尺寸
GAME_WIDTH = 100
GAME_HEIGHT = GAME_WIDTH * 2
GAME_GRID_SIZE = GAME_WIDTH / GRID_COL_COUNT #固定逻辑不要修改

# 间隔空白区域
PADDING = 10
PADDING_STATS = 300

# 整个视图的大小
SCREEN_WIDTH = GAME_WIDTH * COL_COUNT + PADDING * (COL_COUNT + 1) + PADDING_STATS
SCREEN_HEIGHT = GAME_HEIGHT * ROW_COUNT + PADDING * (ROW_COUNT + 1)

def update(screen):
    pass

if __name__ == "__main__":
    #init pygam
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
    while True:
        #每个循环跑一帧游戏
        update(screen)
        for event in pygame.event.get():
            # 判断用户是否点了"X"关闭按钮,并执行if代码段
            if event.type == pygame.QUIT:
                # 卸载所有模块
                pygame.quit()
                # 终止程序，确保退出程序
                sys.exit()


