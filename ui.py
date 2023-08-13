# coding: utf-8
# author: 罗旭维
# date: 2023-08-13


import pygame
import utils

from config import *
from tetris import Tetris

def draw(screen):
    """
    绘制游戏GUI
    :param screen:
    :return:
    """
    screen.fill(COLORS.BACKGROUND_BLACK.value)
    cur_x,cur_y = PADDING,PADDING
    for y in range(ROW_COUNT):
        for x in range(COL_COUNT):
            draw_grid(screen, TETRISTS[y*COL_COUNT + x], cur_x, cur_y)
            cur_x += GAME_WIDTH + PADDING

        cur_x = PADDING
        cur_y += GAME_HEIGHT + PADDING
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
        text_image = pygame.font.SysFont(FONT_NAME, GAME_HEIGHT//6).render(message, False, color.value)
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


