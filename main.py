# coding: utf-8
# author: 罗旭维
# date: 2023-08-12

import pygame
import sys
from config import *
from agent import *
import ui



def update(screen):
    ui.draw(screen)

if __name__ == "__main__":
    #init pygam
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))

    for _ in range(GAME_COUNT):
        AGENTS.append(GeneticAgent())
        TETRISTS.append(Tetris())

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


