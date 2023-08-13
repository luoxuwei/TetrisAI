# coding: utf-8
# author: 罗旭维
# date: 2023-08-12

import pygame
import sys
from config import *
from agent import *
import ui

########################
# Genetics Information #
########################
gen_generation = 1  #族群迭代的次数
gen_previous_best_score = 0.0
gen_top_score = 0.0

# 设置一个最大的游戏时间，不然游戏不结束，就不会停
time_elapsed = 0 #当前游戏时间
time_limit = 1000 #最大游戏时间

AGENTS = []
TETRISTS = []

def update():
    global gen_generation, gen_previous_best_score, gen_top_score
    global time_elapsed, time_limit
    global AGENTS, TETRISTS
    time_elapsed += 1

    #如果所有的游戏都结束，或到最大游戏时间，就结束这一代基因群组的训练，并进化下一代
    if all([tetris.dead for tetris in TETRISTS]) or (time_elapsed % time_limit == 0):
        time_elapsed = 0
        pair = zip(AGENTS, TETRISTS)
        parents = sorted(pair, key=lambda e : e[1].score, reverse=True)#以score的值，从大到小排列
        gen_generation += 1
        gen_previous_best_score = parents[0][1].score
        if gen_top_score < gen_previous_best_score:
            gen_top_score = gen_previous_best_score

        parents = [e[0] for e in parents] #拿到agent列表
        parents = parents[0:GAME_COUNT//2] #淘汰落后的一半基因组
        AGENTS = [parents[0]] #保留最好的一组，其他的都是新一代
        #随机繁衍其余的代理
        while len(AGENTS) < GAME_COUNT:
            parent1,parent2 = random.sample(parents, 2)
            AGENTS.append(parent1.cross_cover(parent2))

        for tetris in TETRISTS:
            tetris.reset_game()

    for i in range(len(AGENTS)):
        if TETRISTS[i].dead:
            continue
        TETRISTS[i].step(AGENTS[i].get_action(TETRISTS[i]))

    ui.draw(TETRISTS, AGENTS, Game(gen_generation, time_elapsed, time_limit, gen_previous_best_score, gen_top_score))



if __name__ == "__main__":

    ui.init()
    for _ in range(GAME_COUNT):
        AGENTS.append(GeneticAgent())
        TETRISTS.append(Tetris())

    while True:
        #每个循环跑一帧游戏
        update()
        for event in pygame.event.get():
            # 判断用户是否点了"X"关闭按钮,并执行if代码段
            if event.type == pygame.QUIT:
                # 卸载所有模块
                pygame.quit()
                # 终止程序，确保退出程序
                sys.exit()


