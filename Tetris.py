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
        self.current = self.get_next_piece(True)
        self.piece_shape = PIECE_SHAPES[self.current][:]
        self.piece_x = int(GRID_COL_COUNT/2 - len(self.piece_shape[0])/2) #居中
        self.piece_y = 0
        #检查游戏是否结束：如果新方块与现有方块碰撞，则游戏结束
        return utils.check_collision(self.grid, self.piece_shape, (self.piece_x, self.piece_y))

    def get_next_piece(self, pop=False):
        """ 从方块池中取下一个方块 """
        if not self.piece_pool:
            self.generate_piece_pool()
        return self.piece_pool[0] if not pop else self.piece_pool.pop(0)

    def generate_piece_pool(self):
        """ 重置方块池 """
        self.piece_pool = list(PIECE_SHAPES.keys())
        random.shuffle(self.piece_pool)

    def on_piece_collision(self):
        """
        方块落定了，做盘面的整理，如果有完整的行就清理并加上积分，最后产生新的方块
        :return:
        """
        #将当前方块加入到盘面self.grid里
        for y,row in enumerate(self.piece_shape):
            for x,val in enumerate(row):
                if val == 0:
                    continue
                self.grid[y + self.piece_y - 1][min(x + self.piece_x, 9)] = val #发生碰撞后触发的这个函数，所以这里计算时要把方块往上挪一格，所以有self.piece_y - 1

        index = 0
        row_completed = 0
        while index < len(self.grid):
            if 0 in self.grid[index]:
                index += 1
                continue
            del self.grid[index]#删除完整的行
            self.grid.insert(0, [0] * GRID_COL_COUNT)#在首部插入空行
            row_completed += 1

        #有完整的行要奖励积分
        self.score += MULTI_SCORE_ALGORITHM(row_completed)
        #产生新的方块
        self.dead = self.generate_piece()


    ###############################
    # 下面部分是游戏中所有可执行的操作 #
    ###############################
    def drop_piece(self, instant=False):
        """
        方块往下坠落，instant为True表示直接掉到最底部，为False表示下落一格
        按照积分规则，存活的越久分应该越高，每掉落一格表示又多存活了一个时间，所以每掉落一格要奖励一定的分值
        :param instant:
        :return:
        """
        if instant:#掉落到最底部
            y = utils.get_effective_height(self.grid, self.piece_shape, (self.piece_x, self.piece_y))
            self.score += PER_STEP_SCORE_GAIN * (y - self.piece_y)
            self.piece_y = y + 1 #这里加1是让方块发生碰撞，配合最后的on_piece_collision函数
        else:
            self.piece_y += 1
            self.score += PER_STEP_SCORE_GAIN

        #如果是下落一格，并且没有发生碰撞就直接返回。因为后面是处理方块落定后的逻辑，如果是instant就一定是落定了。
        if not instant and not utils.check_collision(self.grid, self.piece_shape, (self.piece_x, self.piece_y)):
            return

        self.on_piece_collision()


    def move_piece(self, delta):
        """
        横向移动方块
        :param delta:数值是列表[-2, -1, 1, 2]中的一个，负数往左移动，正数往右移动
        """
        assert delta in [-2, -1, 1, 2], "Invalid move distance"
        new_x = self.piece_x + delta
        new_x =max(0, min(new_x, (GRID_COL_COUNT - len(self.piece_shape[0])))) #大于0，小于GRID_COL_COUNT - len(self.piece_shape[0])
        if utils.check_collision(self.grid, self.piece_shape, (new_x, self.piece_y)):
            return
        self.piece_x = new_x

    def rotate_piece(self):
        """
        旋转方块
        :return:
        """
        new_piece = utils.get_rotated_piece(self.piece_shape)
        new_x = self.piece_x
        if self.piece_x + len(new_piece[0]) > GRID_COL_COUNT:#如果旋转后超出范围，就调整位置到最右的位置
            new_x = GRID_COL_COUNT - len(new_piece[0])

        if utils.check_collision(self.grid, new_piece, (new_x, self.piece_y)):
            return

        self.piece_shape = new_piece
        self.piece_x = new_x

    def swap_piece(self):
        """
        当前方块与方块池中下一个进入的方块交换
        :return:
        """
        new_piece = self.get_next_piece(False)
        new_piece_shap = PIECE_SHAPES[new_piece]
        new_x = self.piece_x
        new_y = self.piece_y

        #规范新方块的位置
        if new_x + len(new_piece_shap[0]) > GRID_COL_COUNT:
            new_x = GRID_COL_COUNT - len(new_piece_shap[0])
        if new_y + len(new_piece_shap) > GRID_ROW_COUNT:
            new_y = GRID_ROW_COUNT - len(new_piece_shap)

        #如果新方块与现有盘面冲突就不执行交换
        if utils.check_collision(self.grid, new_piece, (new_x, new_y)):
            return

        self.piece_pool[0] = self.current
        self.piece_x = new_x
        self.piece_y = new_y
        self.current = new_piece
        self.piece_shape = new_piece_shap


    def step(self, action:ACTION):
        """
        走一步
        :param action: 执行的操作
        :return:
        """
        if self.dead:
            return

        #横向移动
        if action in [ACTION.L, ACTION.R, ACTION.L2, ACTION.R2]:
            self.move_piece((-1 if action in [ACTION.L, ACTION.L2] else 1) * (1 if action in [ACTION.L, ACTION.R] else 2))

        #旋转
        elif action is ACTION.ROTATE:
            self.rotate_piece()
        #交换
        elif action is ACTION.SWAP:
            self.swap_piece()
        #下坠
        elif action in [ACTION.FAST_FALL, ACTION.INSTANT_FALL]:
            self.drop_piece(instant=(action is ACTION.INSTANT_FALL))

        self.drop_piece()


if __name__ == '__main__':
    tetris = Tetris()

    while True:
        if not tetris.dead:
            utils.print_grid(utils.get_grid_with_piece(tetris.grid, tetris.piece_shape, (tetris.piece_x, tetris.piece_y)))

        # Get user input (q = quit, r = reset)
        # 0-8 = actions
        message = input("Next action (0-8): ")
        if message == "q":
            break
        elif message == "r":
            tetris.reset_game()
            continue

        # Step
        tetris.step(ACTION(int(message)))