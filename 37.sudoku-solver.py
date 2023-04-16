#
# @lc app=leetcode id=37 lang=python3
#
# [37] Sudoku Solver
#

# @lc code=start
from copy import deepcopy
from typing import List, Set


class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        b = [[set(range(1, 10)) for _ in range(10)] for _ in range(9)]

        for i in range(9):
            for j in range(9):
                v = board[i][j]
                if v != '.':
                    self.place(i, j, int(v), b)

        self.print(b)
        b = self.brute_force(b)

        for i in range(9):
            for j in range(9):
                assert len(b[i][j]) == 1
                board[i][j] = str(b[i][j].pop())

    def place(self, row: int, col: int, value: int, grid: List[List[Set[int]]]):
        place_queue = [(row, col, value)]
        while len(place_queue) > 0:
            reduce_queue = []
            row, col, value = place_queue.pop()
            if len(grid[row][col]) > 1:
                grid[row][col] = set([value])
            for x in range(9):
                if row != x:
                    reduce_queue.append((x, col))
                if col != x:
                    reduce_queue.append((row, x))
            sr = row // 3 * 3
            sc = col // 3 * 3
            for i in range(3):
                for j in range(3):
                    if sr + i != row or sc + j != col:
                        reduce_queue.append((sr + i, sc + j))
            for i, j in reduce_queue:
                if value in grid[i][j]:
                    grid[i][j].remove(value)
                    if len(grid[i][j]) == 1:
                       place_queue.append((i, j, next(iter(grid[i][j]))))
                    if len(grid[i][j]) == 0:
                        return False
            if len(place_queue) == 0:
                self.print(grid)
                for a in range(9):
                    dr = {}
                    dc = {}
                    for b in range(9):
                        if len(grid[a][b]) > 1:
                            for o in grid[a][b]:
                                if o in dr:
                                    dr[o][0] += 1
                                else:
                                    dr[o] = [1, b]
                        if len(grid[b][a]) > 1:
                            for o in grid[b][a]:
                                if o in dc:
                                    dc[o][0] += 1
                                else:
                                    dc[o] = [1, b]
                    for v, (occ_count, first_occ) in dr.items():
                        if occ_count == 1:
                            place_queue.append((a, first_occ, v))
                    for v, (occ_count, first_occ) in dc.items():
                        if occ_count == 1:
                            place_queue.append((first_occ, a, v))
        return True

    def brute_force(self, grid: List[List[Set[int]]]) -> bool:
        # print('Brute forcing:')
        # self.print(grid)
        solved = True
        for i in range(9):
            for j in range(9):
                if len(grid[i][j]) > 1:
                    solved = False
                    for o in grid[i][j]:
                        new_grid = self.fast_deepcopy(grid)
                        if self.place(i, j, o, new_grid):
                            g = self.brute_force(new_grid)
                            if g is not None:
                                return g
        return grid if solved else None

    def fast_deepcopy(self, grid: List[List[Set[int]]]) -> List[List[Set[int]]]:
        return [[set(o for o in s) if len(s) > 0 else s for s in grid[i]] for i in range(9)]

    def print(self, grid: List[List[Set[int]]]) -> None:
        print('╔═══════╤═══════╤═══════╦═══════╤═══════╤═══════╦═══════╤═══════╤═══════╗')
        for row in range(9):
            for i in range(1, 10, 3):
                r = '║'
                for col in range(9):
                    for j in range(i, i + 3):
                        r += ' '
                        r += str(j) if j in grid[row][col] else ' '
                    if col % 3 == 2:
                        r += ' ║'
                    else:
                        r += ' │'
                print(r)
            if row == 2 or row == 5:
                print('╠═══════╪═══════╪═══════╬═══════╪═══════╪═══════╬═══════╪═══════╪═══════╣')
            elif row == 8:
                print('╚═══════╧═══════╧═══════╩═══════╧═══════╧═══════╩═══════╧═══════╧═══════╝')
            else:
                print('╟───────┼───────┼───────╫───────┼───────┼───────╫───────┼───────┼───────╢')                

        print()

# @lc code=end

from test_utils import run_test

def test(grid):
    Solution().solveSudoku(grid)
    return grid

method = test
'''
run_test(method, [[
    ["5","3",".",".","7",".",".",".","."],
    ["6",".",".","1","9","5",".",".","."],
    [".","9","8",".",".",".",".","6","."],
    ["8",".",".",".","6",".",".",".","3"],
    ["4",".",".","8",".","3",".",".","1"],
    ["7",".",".",".","2",".",".",".","6"],
    [".","6",".",".",".",".","2","8","."],
    [".",".",".","4","1","9",".",".","5"],
    [".",".",".",".","8",".",".","7","9"]
    ]], [
    ["5","3","4","6","7","8","9","1","2"],
    ["6","7","2","1","9","5","3","4","8"],
    ["1","9","8","3","4","2","5","6","7"],
    ["8","5","9","7","6","1","4","2","3"],
    ["4","2","6","8","5","3","7","9","1"],
    ["7","1","3","9","2","4","8","5","6"],
    ["9","6","1","5","3","7","2","8","4"],
    ["2","8","7","4","1","9","6","3","5"],
    ["3","4","5","2","8","6","1","7","9"]
])
run_test(method, [[
    [".",".","9","7","4","8",".",".","."],
    ["7",".",".",".",".",".",".",".","."],
    [".","2",".","1",".","9",".",".","."],
    [".",".","7",".",".",".","2","4","."],
    [".","6","4",".","1",".","5","9","."],
    [".","9","8",".",".",".","3",".","."],
    [".",".",".","8",".","3",".","2","."],
    [".",".",".",".",".",".",".",".","6"],
    [".",".",".","2","7","5","9",".","."]
    ]], [
    ["5","1","9","7","4","8","6","3","2"],
    ["7","8","3","6","5","2","4","1","9"],
    ["4","2","6","1","3","9","8","7","5"],
    ["3","5","7","9","8","6","2","4","1"],
    ["2","6","4","3","1","7","5","9","8"],
    ["1","9","8","5","2","4","3","6","7"],
    ["9","7","5","8","6","3","1","2","4"],
    ["8","3","2","4","9","1","7","5","6"],
    ["6","4","1","2","7","5","9","8","3"]
])
run_test(method, [[
    [".",".",".","2",".",".",".","6","3"],
    ["3",".",".",".",".","5","4",".","1"],
    [".",".","1",".",".","3","9","8","."],
    [".",".",".",".",".",".",".","9","."],
    [".",".",".","5","3","8",".",".","."],
    [".","3",".",".",".",".",".",".","."],
    [".","2","6","3",".",".","5",".","."],
    ["5",".","3","7",".",".",".",".","8"],
    ["4","7",".",".",".","1",".",".","."]
    ]], [
    ["8","5","4","2","1","9","7","6","3"],
    ["3","9","7","8","6","5","4","2","1"],
    ["2","6","1","4","7","3","9","8","5"],
    ["7","8","5","1","2","6","3","9","4"],
    ["6","4","9","5","3","8","1","7","2"],
    ["1","3","2","9","4","7","8","5","6"],
    ["9","2","6","3","8","4","5","1","7"],
    ["5","1","3","7","9","2","6","4","8"],
    ["4","7","8","6","5","1","2","3","9"]
])
'''

run_test(method, [[
    [".",".",".",".",".","7",".",".","9"],[".","4",".",".","8","1","2",".","."],[".",".",".","9",".",".",".","1","."],[".",".","5","3",".",".",".","7","2"],["2","9","3",".",".",".",".","5","."],[".",".",".",".",".","5","3",".","."],["8",".",".",".","2","3",".",".","."],["7",".",".",".","5",".",".","4","."],["5","3","1",".","7",".",".",".","."]]
], [
    ["3","1","2","5","4","7","8","6","9"],["9","4","7","6","8","1","2","3","5"],["6","5","8","9","3","2","7","1","4"],["1","8","5","3","6","4","9","7","2"],["2","9","3","7","1","8","4","5","6"],["4","7","6","2","9","5","3","8","1"],["8","6","4","1","2","3","5","9","7"],["7","2","9","8","5","6","1","4","3"],["5","3","1","4","7","9","6","2","8"]
])