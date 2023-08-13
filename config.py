# coding: utf-8
# author: 罗旭维
# date: 2023-08-12

from enum import Enum

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 训练设置
GRID_ROW_COUNT = 20
GRID_COL_COUNT = 10

#横竖多少个俄罗斯方块游戏在训练
ROW_COUNT = 4
COL_COUNT = 10
GAME_COUNT = ROW_COUNT * COL_COUNT #固定逻辑不要修改


#每个俄罗斯游戏显示的区域尺寸
GAME_WIDTH = 100
GAME_HEIGHT = GAME_WIDTH * 2
GAME_GRID_SIZE = GAME_WIDTH / GRID_COL_COUNT #固定逻辑不要修改

# 间隔空白区域
PADDING = 10
PADDING_STATS = 300

# 整个视图的大小
SCREEN_WIDTH = GAME_WIDTH * COL_COUNT + PADDING * (COL_COUNT + 1) + PADDING_STATS
SCREEN_HEIGHT = GAME_HEIGHT * ROW_COUNT + PADDING * (ROW_COUNT + 1)



# Mutation Rate
MUTATION_RATE = 0.1  # 10% mutation chance

######################
# Piece Configuration #
######################
PIECES = ["I", "L", "J", "S", "Z", "T", "O"]
PIECE_SHAPES = {
    "I": [[1, 1, 1, 1]],
    "L": [[0, 0, 2],
          [2, 2, 2]],
    "J": [[3, 0, 0],
          [3, 3, 3]],
    "S": [[0, 4, 4],
          [4, 4, 0]],
    "Z": [[5, 5, 0],
          [0, 5, 5]],
    "T": [[6, 6, 6],
          [0, 6, 0]],
    "O": [[7, 7],
          [7, 7]]
}

class ACTION(Enum):
    NOTHING = 0
    L = 1
    R = 2
    L2 = 3
    R2 = 4
    ROTATE = 5
    SWAP = 6
    FAST_FALL = 7
    INSTANT_FALL = 8


########################
# Score Configurations #
########################
MULTI_SCORE_ALGORITHM = lambda lines_cleared: 5 ** lines_cleared
PER_STEP_SCORE_GAIN = 0.001

def get_color_tuple(color_hex:str):
    if color_hex is None:
        color_hex = "11c5bf"
    color_hex = color_hex.replace("#", "")
    return tuple(int(color_hex[i:i+2], 16) for i in [0, 2, 4])

class COLORS(Enum):
    # Display
    BACKGROUND_BLACK = get_color_tuple("000000")
    BACKGROUND_DARK = get_color_tuple("021c2d")
    BACKGROUND_LIGHT = get_color_tuple("00263f")
    TRIANGLE_GRAY = get_color_tuple("efe6ff")
    WHITE = get_color_tuple("ffffff")
    RED = get_color_tuple("ff0000")
    # Tetris pieces
    PIECE_I = get_color_tuple("ffb900")
    PIECE_L = get_color_tuple("2753f1")
    PIECE_J = get_color_tuple("f7ff00")
    PIECE_S = get_color_tuple("ff6728")
    PIECE_Z = get_color_tuple("11c5bf")
    PIECE_T = get_color_tuple("ae81ff")
    PIECE_O = get_color_tuple("e94659")
    # Highlights
    HIGHLIGHT_GREEN = get_color_tuple("22ee22")
    HIGHLIGHT_RED = get_color_tuple("ee2222")

FONT_NAME = "Consolas"

