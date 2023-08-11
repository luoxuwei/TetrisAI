# coding: utf-8
# author: 罗旭维
# date: 2023-08-12
import random
import utils
from config import *

#封装俄罗斯方块的游戏逻辑，不包括UI
class Tetris:
    """
    每个游戏需要跟踪记录：
    - 游戏的状态：盘面，当前的方块等
    - 分数 score
    - 和基因组的健康数值 fitness
    """
    def __init__(self):
        self.dead = True
        self.grid = [] #游戏盘面
        self.piece_pool = [] #即将到来的方块
        # 用字符串表示不同形状的方块:
        # ["I", "L", "J", "S", "Z", "T", "O"]
        self.current = ""
        self.next = ""
        # 当前方块的位置
        self.piece_x = 0
        self.piece_y = 0
        #当前方块的形状矩阵
        self.piece_shape = []
        self.score = 0.0
        self.reset_game()

    def reset_game(self):
        """ 重置游戏 """
        self.dead = False
        self.grid = [[0] * GRID_COL_COUNT for _ in range(GRID_ROW_COUNT)]
        self.generate_piece()
        self.score = 0.0

    def generate_piece(self):
        """
        从方块池中生成一个新方块
        :return: 游戏是否结束
        """
        self.current = self.get_next_tile(True)
        self.piece_shape = PIECE_SHAPES[self.current][:]
        self.piece_x = int(GRID_COL_COUNT/2 - len(self.piece_shape[0])/2) #居中
        self.piece_y = 0
        #检查游戏是否结束：如果新方块与现有方块碰撞，则游戏结束
        return utils.check_collision(self.grid, self.piece_shape, (self.piece_x, self.piece_y))

    def get_next_tile(self, pop=False):
        """ 从方块池中取下一个方块 """
        if not self.piece_pool:
            self.generate_piece_pool()
        return self.piece_pool[0] if not pop else self.piece_pool.pop(0)

    def generate_piece_pool(self):
        """ 重置方块池 """
        self.piece_pool = list(PIECE_SHAPES.keys())
        random.shuffle(self.piece_pool)