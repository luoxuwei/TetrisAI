# coding: utf-8
# author: 罗旭维
# date: 2023-08-13

from tetris import *
from config import *
from typing import *
from abc import ABC, abstractmethod
"""
封装遗传算法
"""

class BaseAgent(ABC):
    """
    智能体基类，定义框架
    """
    def __init__(self):
        self.actions:[ACTION] = []

    def get_action(self, tetris: Tetris):
        if len(self.actions) == 0:
            self.actions = self.calculate_actions(tetris.grid, tetris.piece_shape, PIECE_SHAPES[tetris.get_next_piece()], (tetris.piece_x, tetris.piece_y))

        return self.actions.pop(0)

    @abstractmethod
    def calculate_actions(self, board, current_tile, next_tile, offsets) -> List[ACTION]:
        """
        获取最佳操作
        :param board:当前游戏盘面
        :param current_tile:当前方块
        :param next_tile:下一个方块
        :param offsets:当前方块位置
        :return:
        """
        pass


class RandomAgent(BaseAgent):
    def calculate_actions(self, board, current_tile, next_tile, offsets) -> List[ACTION]:
        return [ACTION(random.randint(0, 8)) for _ in range(10)]