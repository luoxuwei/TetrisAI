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
    def calculate_actions(self, grid, current_piece, next_piece, offsets) -> List[ACTION]:
        """
        获取最佳操作
        :param grid:当前游戏盘面
        :param current_piece:当前方块
        :param next_piece:下一个方块
        :param offsets:当前方块位置
        :return:
        """

        pass


class RandomAgent(BaseAgent):
    def calculate_actions(self, grid, current_piece, next_piece, offsets) -> List[ACTION]:
        return [ACTION(random.randint(0, 8)) for _ in range(10)]


class GeneticAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.weight_height = random.random() #盘面累积的高度，盘面累积的方块越高越接近死亡
        self.weight_holes = random.random() #盘面里的孔洞，孔洞越多盘面越糟糕
        self.weight_bumpiness = random.random() #盘面里累积的方块的平滑度，凹凸不平落差大的盘面很糟糕
        self.weight_line_completed = random.random() #清除的完整的行数，清除的越多越优秀

    def calculate_actions(self, grid, current_piece, next_piece, offsets) -> List[ACTION]:
        """
        获取最佳操作
        就是遍历所有可能的组合，计算每个组合的得分，返回分数最大的
        :param grid:当前游戏盘面
        :param current_piece:当前方块
        :param next_piece:下一个方块
        :param offsets:当前方块位置
        :return:
        """
        best_fitness = -9999
        best_piece_index = -1
        best_rotation = -1
        best_x = -1
        #因为可以和下一个方块交换，分两种情况
        # 遍历所有旋转和水平移动的组合，垂直的方向的移动不参与组合，确定旋转和水平位置后，计算fitness是看方块坠落到最底部时的情况，所以垂直方向是默认走到最底部。
        pieces = [current_piece, next_piece]
        for piece_index in range(len(pieces)):
            piece = pieces[piece_index]
            # 遍历旋转次数，0-3，第4次就回到最初的状态了
            for rotation_times in range(0, 4):
                #遍历横向所有位置（0~GRID_COL_COUNT - len(piece[0])）
                for x in (0, GRID_COL_COUNT - len(piece[0])):
                    #获取方块落到最底部时的盘面
                    new_grid = utils.get_finish_grid_with_piece(grid, piece, (x, offsets[1]), True)
                    fitness = self.get_fitness(new_grid)
                    if fitness > best_fitness:
                        best_fitness = fitness
                        best_piece_index = piece_index
                        best_rotation = rotation_times
                        best_x = x
                piece = utils.get_rotated_piece(piece)

        #将最佳操作组合转换成命令列表
        actions = []
        #交换
        if pieces[best_piece_index] != current_piece:
            actions.append(ACTION.SWAP)
        #旋转
        for _ in range(best_rotation):
            actions.append(ACTION.ROTATE)
        #横向移动
        pre_x = offsets[0]
        while pre_x != best_x:
            direction = 1 if pre_x < best_x else -1
            magnitude = 1 if abs(pre_x - best_x) == 1 else 2
            pre_x += direction * magnitude
            act = [ACTION.R, ACTION.R2] if direction > 0 else [ACTION.L, ACTION.L2]
            actions.append(act[magnitude - 1])

        actions.append(ACTION.INSTANT_FALL)

        return actions

    def get_fitness(self,grid):
        """
        计算棋盘的适应度分数，就是基因组的优秀程度
        :param grid: 盘面，会改变grid，所以应该传进来一个副本，
        :return:
        """

        score = 0
        grid, completed_lines = utils.get_grid_and_lines_completed(grid)
        #计算盘面的总高度并乘以权重
        score += self.weight_height * sum(utils.get_col_heights(grid))
        #计算盘面的孔洞数并乘以权重
        score += self.weight_holes * utils.get_hole_count(grid)
        #计算盘面的平滑度并乘以权重
        score += self.weight_bumpiness * utils.get_bumpiness(grid)
        #计算清理的完整的行数并乘以权重
        score += self.weight_line_completed * completed_lines
        return score

    def cross_cover(self, other):
        """
        两个agent配对，产生下一代
        就是四个权重，随机从父母一方继承
        :param other:
        :return:
        """
        child = GeneticAgent()
        #从父母那里随机选择参数权重
        child.weight_height = self.weight_height if random.getrandbits(1) else other.weight_height
        child.weight_holes = self.weight_holes if random.getrandbits(1) else other.weight_holes
        child.weight_bumpiness = self.weight_bumpiness if random.getrandbits(1) else other.weight_bumpiness
        child.weight_line_completed = self.weight_line_completed if random.getrandbits(1) else other.weight_line_completed

        #随机突变
        if random.random() < MUTATION_RATE:
            child.weight_height = utils.random_weight()
        if random.random() < MUTATION_RATE:
            child.weight_holes = utils.random_weight()
        if random.random() < MUTATION_RATE:
            child.weight_bumpiness = utils.random_weight()
        if random.random() < MUTATION_RATE:
            child.weight_line_completed = utils.random_weight()
        return child