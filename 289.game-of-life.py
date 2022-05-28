#
# @lc app=leetcode id=289 lang=python3
#
# [289] Game of Life
#

# @lc code=start
from typing import List


class Solution:
    def gameOfLife(self, board: List[List[int]]) -> None:
        test_vectors = [
            [-1, -1], [-1, 0], [-1, 1],
            [ 0, -1],          [ 0, 1],
            [ 1, -1], [ 1, 0], [ 1, 1],
        ]

        h = len(board)
        w = len(board[0])

        for y in range(h):
            for x in range(w):
                nc = 0
                for dx, dy in test_vectors:
                    ny = y + dy
                    nx = x + dx
                    if ny >= 0 and ny < h and nx >= 0 and nx < w:
                        if board[ny][nx] & 1 == 1:
                            nc += 1
                if nc <= 1 or nc > 3:
                    board[y][x] &= 1
                elif nc == 2:
                    board[y][x] |= board[y][x] << 1
                elif nc == 3:
                    board[y][x] |= 2
        print(board)
        for y in range(h):
            for x in range(w):
                board[y][x] >>= 1

# @lc code=end

from test_utils import run_test

def test(x):
    Solution().gameOfLife(x)
    return x

method = test
run_test(method, args=[[[0,1,0],[0,0,1],[1,1,1],[0,0,0]]],
                 expected=[[0,0,0],[1,0,1],[0,1,1],[0,1,0]])
run_test(method, args=[[[1,1],[1,0]]],
                 expected=[[1,1],[1,1]])
