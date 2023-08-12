# coding: utf-8
# author: 罗旭维
# date: 2023-08-12

from copy import deepcopy

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