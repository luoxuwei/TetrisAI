# coding: utf-8
# author: 罗旭维
# date: 2023-08-13


import pygame
import utils

from config import *
from tetris import Tetris
from agent import GeneticAgent
SEP = ", "
screen = None

def init():
    global screen
    #init pygam
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))

def draw(tetris:list[Tetris], agents:list[GeneticAgent], game:Game):
    """
    绘制游戏GUI
    :param screen:
    :return:
    """
    screen.fill(COLORS.BACKGROUND_BLACK.value)
    cur_x,cur_y = PADDING,PADDING
    for y in range(ROW_COUNT):
        for x in range(COL_COUNT):
            draw_grid(screen, tetris[y*COL_COUNT + x], cur_x, cur_y)
            cur_x += GAME_WIDTH + PADDING

        cur_x = PADDING
        cur_y += GAME_HEIGHT + PADDING

    #统计数据展示
    cur_x, cur_y = GAME_WIDTH * COL_COUNT + PADDING * (COL_COUNT + 1), PADDING #统计数据展示区域的左上角坐标
    #标题
    draw_text("Tetris", (cur_x, cur_y), font_szie=48)
    cur_y += 60
    #数据
    best_indexs, best_score = get_high_score(tetris)
    draw_text(f"High Score: {best_score:.1f}", (cur_x, cur_y))
    cur_y += 20
    draw_text(f"Best Agent: {SEP.join(map(str, best_indexs))}", (cur_x, cur_y))
    cur_y += 20

    #绘制AI代理相关数据
    if game.gen_generation > -1:
        cur_y += 20
        draw_text(f"Generation #{game.gen_generation}", (cur_x, cur_y), font_szie=24) #第几代
        cur_y += 20
        draw_text(f"Time Limit: {game.time_elapsed}/{game.time_limit}", (cur_x, cur_y)) #剩余时间
        cur_y += 20

        survivor = len([a for a in tetris if not a.dead])
        draw_text(f"Survivors: {survivor}/{GAME_COUNT} ({survivor/GAME_COUNT * 100:.1f}%)", (cur_x, cur_y)) #存活的游戏
        cur_y += 20
        draw_text(f"Prev H.Score: {game.gen_previous_best_score:.1f}", (cur_x, cur_y))#上一代最高分
        cur_y += 20
        draw_text(f"All Time H.Score: {game.gen_top_score:.1f}", (cur_x, cur_y))#总体最高分
        cur_y += 40

        #绘制最佳代理的数据
        agent_index = -1
        if len(best_indexs) > 0:
            agent_index = best_indexs[0]

        if agent_index > -1:
            draw_text(f"Agent #{agent_index}:", (cur_x, cur_y))
            cur_y += 35
            draw_text(f">> Agg Height: {agents[agent_index].weight_height:.1f}", (cur_x, cur_y))
            cur_y += 20
            draw_text(f">> Hole Count: {agents[agent_index].weight_holes:.1f}", (cur_x, cur_y))
            cur_y += 20
            draw_text(f">> Bumpiness:  {agents[agent_index].weight_bumpiness:.1f}", (cur_x, cur_y))
            cur_y += 20
            draw_text(f">> Line Clear: {agents[agent_index].weight_line_completed:.1f}", (cur_x, cur_y))
            cur_y += 20








    pygame.display.update()


def draw_grid(screen, tetris:Tetris, x, y):

    #列背景
    for col in range(GRID_COL_COUNT):
        color = COLORS.BACKGROUND_DARK if col % 2 == 0 else COLORS.BACKGROUND_LIGHT
        pygame.draw.rect(screen, color.value, (x + col * GAME_GRID_SIZE, y, GAME_GRID_SIZE, GAME_HEIGHT))

    #画盘面
    draw_piece(screen, tetris.grid, global_offsets=(x, y))
    #画当前的方块
    draw_piece(screen, tetris.piece_shape, (tetris.piece_x, tetris.piece_y), (x,y))

    #游戏结束画面
    if tetris.dead:
        #画背景黑条，上下居中
        pygame.draw.rect(screen, COLORS.BACKGROUND_BLACK.value, (x, y + (GAME_HEIGHT/2 - GAME_HEIGHT*0.1/2), GAME_WIDTH, GAME_HEIGHT*0.1)) #设计黑条的高度为GAME_HEIGHT*0.1
        #画字，居中
        message = "GAME OVER"
        color = COLORS.RED
        text_image = pygame.font.SysFont(FONT_NAME, GAME_WIDTH//6).render(message, False, color.value)
        text_rect = text_image.get_rect()
        screen.blit(text_image, (x + GAME_WIDTH/2 - text_rect.width/2, y + GAME_HEIGHT/2 - text_rect.height/2))


def draw_piece(screen, matrix, offsets=(0, 0), global_offsets=(0, 0)):
    """
    盘面和当前的方块，都是一个矩阵，可以统一到一个函数画
    :param screen:pygame screen
    :param matrix:要画的矩阵
    :param offsets:游戏里当前方块的位置
    :param global_offsets:单个游戏的位置
    :return:
    """
    for y, row in enumerate(matrix):
        for x, val in enumerate(row):
            if val == 0:
                continue

            coord_x = global_offsets[0] + (offsets[0] + x) * GAME_GRID_SIZE
            coord_y = global_offsets[1] + (offsets[1] + y) * GAME_GRID_SIZE
            #画格子
            pygame.draw.rect(screen, COLORS["PIECE_" + PIECES[val-1]].value, (coord_x, coord_y, GAME_GRID_SIZE, GAME_GRID_SIZE))
            # 画边框
            pygame.draw.rect(screen, COLORS.BACKGROUND_BLACK.value, (coord_x, coord_y, GAME_GRID_SIZE,
                             GAME_GRID_SIZE), 1)
            #画格子左上角的三角形
            offset = GAME_GRID_SIZE/10
            pygame.draw.polygon(screen, COLORS.TRIANGLE_GRAY.value,
                                ((coord_x + offset, coord_y + offset),
                                 (coord_x + 3 * offset, coord_y + offset),
                                 (coord_x + offset, coord_y + 3*offset)),)



def draw_text(text, offsets, font_szie = 16, color=COLORS.WHITE):
    text_image = pygame.font.SysFont(FONT_NAME, font_szie).render(text, False, color.value)
    screen.blit(text_image, offsets)

def get_high_score(tetris:list[Tetris]):
    """
    获取分数最高的游戏，如果有并列第一的一起放入列表
    :param tetris:
    :return:
    """
    best_indexes, best_score = [], 0
    for a in range(GAME_COUNT):
        # Ignore dead games
        if tetris[a].dead:
            continue
        # Get score
        score = tetris[a].score
        if score > best_score:
            best_indexes = [a]
            best_score = score
        elif score == best_score:#并列第一的
            best_indexes.append(a)
    return best_indexes, best_score