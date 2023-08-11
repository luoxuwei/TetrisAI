# coding: utf-8
# author: 罗旭维
# date: 2023-08-12

#检查新方块与现有方块是否发生碰撞
def check_collision(grid, shape, offset):
    for y, row in shape:
        for x, val in row:
            if val == 0:#方块当前位置是空的
                continue
            try:
                if grid[offset[1] + y][offset[0] + x] != 0:#同一个位置上，方块和盘面都非空就是发生碰撞
                    return True
            except IndexError:
                return True

    return False #遍历完了意味着没有发生碰撞

