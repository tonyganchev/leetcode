from enum import IntEnum
from numpy import Infinity
from test_utils import run_test
from typing import List, Tuple
from math import sqrt, ceil, floor
import re


def solve_internal(data: str, expansion_rate: int) -> int:
    mp = data.splitlines()
    galaxies = []
    for i, row in enumerate(mp):
        for j, cell in enumerate(row):
            if cell == '#':
                galaxies.append([i, j])
    row_remap = list(range(len(mp)))
    col_remap = list(range(len(mp[0])))
    for i, row in enumerate(mp):
        empty_row = True
        for j, cell in enumerate(row):
            if cell == '#':
                empty_row = False
                break
        if empty_row:
            for k in range(i, len(mp)):
                row_remap[k] += expansion_rate
    for j in range(len(mp[0])):
        empty_col = True
        for i in range(len(mp)):
            if mp[i][j] == '#':
                empty_col = False
                break
        if empty_col:
            for k in range(j, len(mp[0])):
                col_remap[k] += expansion_rate

    for g in galaxies:
        g[0] = row_remap[g[0]]
        g[1] = col_remap[g[1]]

    s = 0
    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            h = abs(galaxies[i][0] - galaxies[j][0])
            w = abs(galaxies[i][1] - galaxies[j][1])
            d = w + h
            # print(i, j, d)
            s += d
    return s

small_vector = '''...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....'''
large_vector = '''....................................#..............#.................................#......................................................
............#......#..........................................................#.....................................#.................#.....
.........................................................................................#...................#..............................
.....#......................................................#...............................................................................
..........................................................................#........................#.............................#..........
......................#.................#...............................................................................#...................
........#......................................................#...............................#............................................
...........................#.................#.......................................#...................#.........#.................#......
.#................#.......................................#..........#........#.............................................................
............................................................................................................................................
..................................#.........................................................................................................
.........................................................................................#.................................#................
.......#.............#................................#........#.....................................#......................................
..........................................#.................................................................................................
.............#...............................................................................................#..........#...................
....................................#.................................#............#....................#......................#............
............................................................................................#...............................................
........#...........................................#.......#.............................................................................#.
.....................#.......#..................................................#....................................................#......
..............#........................#.......#........................#................................................#..................
.......................................................#..........................................................#.........................
..#..............................................................#..........#.......................#.......................................
..................................................#......................................................#..................................
......................................................................................................................#.....................
.....#................................#...............................................#.....................................................
...................#.....#...............................#.......................#..............#..........................#................
.........#.................................#................................................................................................
..................................................................#.................................#......#.......................#........
............................#........................................................................................#..................#...
.................#...............................#............#............#................................................................
................................#................................................................#..........................................
............................................#.........................................#.......................................#.............
.........#.................................................................................#............................#............#......
..#....................................................#..........#.............#.........................#.................................
...........................#...................#............................................................................................
...................................#...................................#..........................................................#.........
................#..................................................................#..................#..........#..........................
.............................................................#...............................#..............................................
#.................................................................................................#.......................#.................
.........................#...............#..................................................................................................
...........................................................................................................#..................#......#......
.........................................................#.................................................................................#
..............................#.............#......#....................................................................#...................
.....#......................................................................#...............................................................
...............................................................................................................#.......................#....
............#.........#................#...............#............#...........#...........#........................#......................
............................................................................................................................................
................#.................................#............#..........................................................#........#........
...............................#...............................................................#...........................................#
.........................................#.............................#.............................#......................................
...................................................................................#.......................#................................
.........#................#...................#.........................................#...............................#...............#...
....................#................#......................................#.....................#.............#...........................
............................................................................................................................................
......................................................................#.....................................................................
......#..........................................................#........................................................................#.
.............#.........................#.......................................#............................#.....#......#..................
.........................#........#.........#......#.................................#.....#................................................
..#.....................................................#.........................................#.........................................
....................#...............................................#.......................................................................
........................................................................................................#.......................#.......#...
.............................#...................................................#.........................................#................
....................................................................................................#.......................................
.......#..........#..............................................#........#.................#..................#............................
....................................#..........#......#.....#.........................................................#.............#.......
............................................................................................................................................
..............................#................................................................#..........#.................................
..#..............................................................................................................................#..........
..............................................................................................................#.............................
.................................................#........................#...............................................#.................
...................#.....................................................................................................................#..
......#....................#......#.....#................#...................................#.............#................................
.............................................#.......................................#...............................#......................
.................................................................................................#..........................................
...#.................................................................#...........#..........................................................
....................#..............................................................................................................#........
..........#.....................#...........................................................#.............#...............................#.
............................................................................................................................................
..................................................#............................................................#...........#................
...........................................#........................#.........#.....................#.......................................
.#.........................#..............................#.................................................................................
.....................................................................................#.........................................#............
..............................................................................................#......................#...................#..
.....#...........#.....#.....................#..............................................................#...............................
..........#....................................................#.....#......................................................................
#...............................#.....#.....................................................................................................
........................................................#.........................#...................#........#..................#.........
.............................................................................................................................#.............#
.........................................................................#.................................#................................
.........#.......#................................#..............................................#.....................................#....
............................................................................................................................................
................................#............#........................#.........................................#...........................
............#...............................................#........................#................#...............#.....................
..#....................#..........................................#..........................................................#..............
...................................................#......................................................................................#.
................#....................................................................................................................#......
.......#..................................................#...................#.............#..............#................................
.................................................................................................................................#..........
...................#...........#............................................................................................................
.........................................#.....................#....................................#.........#.......#.....................
.#........................................................................#..............................#..................................
............#.....................#.....................................................................................................#...
.......#....................................................................................................................................
.................................................................#............#...................#........................#......#.........
........................................................................................#.......................#...........................
.........................................#.............................#....................................................................
..............#......#...............................................................................................................#......
................................................................................................#......................#....................
............................#............................#..........................#..................#...................................#
...........#...............................................................................#....................................#...........
............................................................................................................................................
.................#.......#............#.......................................................................#.............................
............................................................................................................................................
...#.........................#.................................#...............#............................................#.....#.........
......................................................#...................#..........#.........#.....#....................................#.
...................................#.........#......................................................................#.......................
............................................................................................................................................
..........#..............#...................................#..............................................................................
............................................................................................................................................
.....#...................................................#...............................#...................#..........#..................#
..............................#.......#........#............................................................................................
.................#...............................................................#.................................#........................
.....................................................................#........................................................#.............
............#..................................................................................#............................................
.......................#..................................#..............................................................#.............#....
...................................#........................................................................................................
...........................................................................#.......................................................#........
........#....................#.....................#...............#................................#..............#........................
...#.........#.............................#.........................................#...................#..................................
..............................................................................#..............#........................................#.....
..................................#.......................................................................................#.................
........................#...................................................................................................................
.......................................................#.............................................#............#.........................
............................#........#..............................#.......................................................................
...#........................................................#............#............#............................................#........
.................#..........................#...............................................................................................
..........................................................................................#................................................#
..........#.................................................................................................................................
.........................#............#........................................................#............................................
...............#...................................#......................#..............................#...........#......................'''
method = solve_internal
run_test(method, [small_vector, 1], 374)
run_test(method, [large_vector, 1], 9177603)
run_test(method, [small_vector, 9], 1030)
run_test(method, [small_vector, 99], 8410)
run_test(method, [small_vector, 999999], 82000210)
run_test(method, [large_vector, 999999], 632003913611)

