# coding: utf-8
# author: 罗旭维
# date: 2023-08-12
import random
from copy import deepcopy
from config import *

#检查新方块与现有方块是否发生碰撞
def check_collision(grid, shape, offset):
    for y, row in enumerate(shape):
        for x, val in enumerate(row):
            if val == 0:#方块当前位置是空的
                continue
            try:
                if grid[offset[1] + y][offset[0] + x] != 0:#同一个位置上，方块和盘面都非空就是发生碰撞
                    return True
            except IndexError:
                return True

    return False #遍历完了意味着没有发生碰撞

def get_rotated_piece(shape):
    return list(zip(*reversed(shape))) #旋转后通过zip提取横向量

def get_effective_height(grid, shape, offset):
    """
    计算方块可以往下掉的最底部的高度
    :param grid:盘面
    :param shape:方块
    :param offset:方块当前位置
    :return:
    """
    x,y = offset
    while not check_collision(grid, shape, (x, y)):
        y += 1

    return y - 1

def get_grid_with_piece(grid, piece, offset, flattened=False):
    new_grid = deepcopy(grid)
    if flattened:
        new_grid = [[int(bool(val)) for val in row] for row in new_grid]

    for y,row in enumerate(piece):
        for x,val in enumerate(row):
            new_grid[y + offset[1]][x + offset[0]] = val

    return new_grid

def print_grid(grid):
    print("Printing debug board")
    for i, row in enumerate(grid):
        print("{:02d}".format(i), row)



def get_grid_and_lines_completed(grid):
    """
    获取grid中完整的行数，注意这个函数会改变grid
    :param grid:
    :return:
    """
    completed = 0
    row = 0
    while row < len(grid):
        if 0 in grid[row]:
            row += 1
            continue

        del grid[row]
        completed += 1
        grid.insert(0, [0]*GRID_COL_COUNT)
    return grid, completed

def get_col_heights(grid):
    """
    获取所有列的高度
    从上往下一行行遍历，一旦碰到不为0的格子，就是当前列的最大高度。另外用一个列表保存还未找到最大高度的列号，一旦找到从列表中删除该列号
    :param grid:
    :return:
    """
    heights = [0] * GRID_COL_COUNT
    cols = list(range(GRID_COL_COUNT))
    for y, row in enumerate(grid):
        for x,val in enumerate(row):
            if 0 == val or x not in cols:
                continue
            heights[x] = GRID_ROW_COUNT - y
            cols.remove(x)

    return heights

def get_hole_count(grid):
    """
    找到所有的孔洞
    从上往下一行行遍历，找到每一列的最大高度，当遍历到为0的格子并且格子的高度小于该列的最大高度，就证明这个是一个孔
    :param grid:
    :return:
    """
    cols = [0]*GRID_COL_COUNT
    holes = 0

    for y, row in enumerate(grid):
        height = GRID_ROW_COUNT - y
        for x, val in enumerate(row):
            if val == 0 and height < cols[x]:
                holes += 1
                continue

            if val != 0 and cols[x] == 0:
                cols[x] = height
    return holes

def get_bumpiness(grid):
    """
    计算盘面平滑度
    先获取所有列的高度，然后累加相邻两列的高度差
    :param grid:
    :return:
    """
    heights = get_col_heights(grid)
    bumpiness = 0
    for i in range(1, GRID_COL_COUNT):
        bumpiness += abs(heights[i] - heights[i-1])
    return bumpiness

def random_weight():
    return random.uniform(-1, 1)

def get_finish_grid_with_piece(grid, piece, offsets, flattened=False):
    return get_grid_with_piece(grid, piece, (offsets[0], get_effective_height(grid, piece, offsets)), flattened)