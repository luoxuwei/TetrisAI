# coding: utf-8
# author: 罗旭维
# date: 2023-08-12


GRID_ROW_COUNT = 20
GRID_COL_COUNT = 10

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

########################
# Score Configurations #
########################
MULTI_SCORE_ALGORITHM = lambda lines_cleared: 5 ** lines_cleared
PER_STEP_SCORE_GAIN = 0.001