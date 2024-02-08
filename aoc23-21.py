from enum import IntEnum
from numpy import Infinity
from test_utils import run_test
from typing import List, Tuple, Dict
from math import sqrt, ceil, floor, prod, lcm
import re
import numpy as np
from functools import cache


def find_start(grid):
    for si, row in enumerate(grid):
        for sj, cell in enumerate(row):
            if cell == 'S':
                return si, sj
    assert False, 'missing S element'


def solve(data: str, steps) -> int:
    grid = tuple(list(s) for s in data.splitlines())
    si, sj = find_start(grid)
    tile_count = 1
    queue = {si: set([sj])}
    while len(queue) > 0 and steps >= 0:
        tile_count = 0
        new_queue = {}
        overlaps = 0
        for si, v in queue.items():
            for sj in v:
                if grid[si][sj] == '.':
                    grid[si][sj] = 'O'
                    tile_count += 1
                else:
                    overlaps += 1
        # print(overlaps)
        # print('\n'.join(''.join(row) for row in grid))
        for si, v in queue.items():
            for sj in v:
                grid[si][sj] = '.'
                for di, dj in ((-1, 0), (0, -1), (0, 1), (1, 0)):
                    i, j = si + di, sj + dj
                    if i >= 0 and i < len(grid) and j >= 0 and j < len(grid[0]) and grid[i][j] == '.':
                        new_queue.setdefault(i, set())
                        new_queue[i].add(j)
        queue = new_queue
        # print(tile_count)
        steps -= 1
    return tile_count


free_slots = set(['.', 'O', 'S'])
f = 1000000000

reverse = '\033[;7m'
reset = '\033[0;0m'
start = '\033[0;43m'


def chunk_coord(coord, length):
    offset = (coord + length * f) % length
    return (coord - offset) // length


# run_test(chunk_coord, [0, 10], 0)
# run_test(chunk_coord, [-1, 10], -1)
# run_test(chunk_coord, [-13, 10], -2)
# run_test(chunk_coord, [33, 10], 3)

repeats = 2
optimize_with_full_chunks = False

def dump_grid(grid, display_grid, top, left):
    smi = (top - (len(grid) * f + top) % len(grid)) // len(grid)
    smj = (left - (len(grid[0]) * f + left) % len(grid[0])) // len(grid[0])
    for i, line in enumerate(display_grid):
        for j, c in enumerate(line):
            mi = i // len(grid) + smi
            mj = j // len(grid[0]) + smj
            if mi == 0 and mj == 0:
                print(start, end='')
            elif (mi + mj) % 2 == 0:
                print(reverse, end='')
            print(c, end='')
            print(reset, end='')
        print()
    print()

def print_grid(grid, queue, step_count, full_grids, full_grid, stable_grid_lookup):
    top = 0
    left = 0
    bottom = len(grid[0])
    right = len(grid)
    for si, v in queue.items():
        for sj, c in v.items():
            top = min(top, si)
            left = min(left, sj)
            bottom = max(bottom, si + 1)
            right = max(right, sj + 1)
    oi = (len(grid) * f + top) % len(grid) - top
    oj = (len(grid[0]) * f + left) % len(grid[0]) - left

    h = ceil((oi + bottom) / len(grid)) * len(grid)
    w = ceil((oj + right) / len(grid[0])) * len(grid[0])

    display_grid = [[grid[i % len(grid)][j % len(grid[0])]
                     for j in range(w)] for i in range(h)]

    for si, v in queue.items():
        for sj, c in v.items():
            display_grid[si + oi][sj + oj] = 'O'

    full_grid_count = 0
    for mi, row in full_grids.items():
        for mj, (reps_even, reps_odd) in row.items():
            if reps_even >= repeats and reps_odd >= repeats:
                full_grid_count += 1
                for y in range(len(grid)):
                    for x in range(len(grid[0])):
                        display_grid[oi + mi * len(grid) + y][oj + mj * len(grid[0]) + x] = 'X'
    
    stable_grid_count = len(stable_grid_lookup)
    for mi, row in stable_grid_lookup.items():
        for mj in row:
            # stable_grid_count += 1
            for y in range(len(grid)):
                for x in range(len(grid[0])):
                    display_grid[oi + mi * len(grid) + y][oj + mj * len(grid[0]) + x] = '*'

    dump_grid(grid, display_grid, top, left)

    print('full grids', full_grid_count)
    print('stable grids', stable_grid_count)
    print()

    smi = (top - (len(grid) * f + top) % len(grid)) // len(grid)
    smj = (left - (len(grid[0]) * f + left) % len(grid[0])) // len(grid[0])

    aggregates = [[0 for _ in range(w // len(grid[0]))]
                  for _ in range(h // len(grid[0]))]
    for i, line in enumerate(display_grid):
        for j, c in enumerate(line):
            mi = i // len(grid)
            mj = j // len(grid[0])
            if display_grid[i][j] == 'O':
                aggregates[mi][mj] += 1
    for mi, line in enumerate(aggregates):
        for mj, a in enumerate(line):
            if mi + smi == 0 and mj + smj == 0:
                print(start, end='')
            elif (mi + mj + smi + smj) % 2 == 0:
                print(reverse, end='')
            print(f'{a:2} ', end='')
            print(reset, end='')
        print()
    print()

def compute_full_girds(g, si, sj):
    grid = [[c for c in row] for row in g]
    step = 0
    h = len(grid)
    w = len(grid[0])
    queue = [(si, sj)]
    while len(queue) > 0:
        new_queue = []
        for si, sj in queue:
            if si >= 0 and sj >= 0 and si < h and sj < h:
                grid[si][sj] = str(step % 2)
            for di, dj in ((-1, 0), (0, -1), (0, 1), (1, 0)):
                i = si + di
                j = sj + dj
                if i < -h or i >= 2 * h or j < -w or j >= 2 * w:
                    continue
                gi = (len(grid) * f + i) % len(grid)
                gj = (len(grid[0]) * f + j) % len(grid[0])
                if grid[gi][gj] == '.':
                    new_queue.append((i, j))
        queue = new_queue
        step += 1
    full_grid_data = [0, 0]
    for r in grid:
        for c in r:
            if c != '#' and c != '.':
                full_grid_data[int(c)] += 1
    return full_grid_data

report_rate = 1

def solve2(data: str, steps) -> int:
    grid = tuple(list(s) for s in data.splitlines())
    si, sj = find_start(grid)
    grid[si][sj] = '.'

    full_grid = compute_full_girds(grid, si, sj)

    full_grids = {}

    stable_grids = [0, 0]
    stable_grid_lookup = {}

    queue = {si: {sj: 1}}
    step_count = 0
    while len(queue) > 0 and step_count <= steps:
        # print()
        new_queue = {}
        new_queue_len = 0

        if step_count % report_rate == 0:
            print_grid(grid, queue, step_count, full_grids, full_grid, stable_grid_lookup)

        full_grid_count = 0
        stable_grid_count = 0
        grids = {}
        for si, v in queue.items():
            for sj, c in v.items():
                mi = chunk_coord(si, len(grid))
                mj = chunk_coord(sj, len(grid[0]))
                grids.setdefault(mi, {})
                grids[mi].setdefault(mj, 0)
                grids[mi][mj] += 1
        # print('Finding full grids...')
        if optimize_with_full_chunks:
            for mi, v in grids.items():
                for mj, c in v.items():
                    if c == full_grid[(mi + mj + step_count) % 2]:
                        full_grids.setdefault(mi, {})
                        full_grids[mi].setdefault(mj, [0, 0])
                        full_grids[mi][mj][step_count % 2] += 1

            for mi, v in full_grids.items():
                for mj, v in v.items():
                    if v[0] >= repeats and v[1] >= repeats:
                        full_grid_count += full_grid[(mi +
                                                      mj + step_count) % 2]
            
            if step_count % report_rate == 0:
                print('full_grid_count', full_grid_count)
            
            stable_grid_count += stable_grids[0] * full_grid[step_count % 2]
            stable_grid_count += stable_grids[1] * full_grid[(step_count + 1) % 2]

            if step_count % report_rate == 0:
                print('stable_grid_count', stable_grid_count)

        individual_tile_count = 0

        for si, v in queue.items():
            for sj, c in v.items():
                mi = chunk_coord(si, len(grid))
                mj = chunk_coord(sj, len(grid[0]))

                if False and si >= 0 and sj >= 0 and si < len(grid) and sj < len(grid[0]):
                    grid[si][sj] = str(step_count % 2)

                if optimize_with_full_chunks:
                    if mi in full_grids and mj in full_grids[mi] and full_grids[mi][mj][0] >= repeats and full_grids[mi][mj][1] >= repeats:
                        continue
                    if mi in stable_grid_lookup and mj in stable_grid_lookup[mi]:
                        continue

                individual_tile_count += c
                for di, dj in ((-1, 0), (0, -1), (0, 1), (1, 0)):
                    i = si + di
                    j = sj + dj
                    gi = (len(grid) * f + i) % len(grid)
                    gj = (len(grid[0]) * f + j) % len(grid[0])

                    if grid[gi][gj] == '.':
                        new_queue.setdefault(i, {})
                        new_queue[i].setdefault(j, 0)
                        new_queue[i][j] = 1
                        new_queue_len += 1

        if True and optimize_with_full_chunks:
            full_grids_to_purge = []
            for mi, v in full_grids.items():
                for mj, v in v.items():
                    if v[0] >= repeats and v[1] >= repeats:
                        full_grids_to_purge.append((mi, mj))
                        stable_grids[(mi + mj) % 2] += 1
                        stable_grid_lookup.setdefault(mi, set())
                        assert mj not in stable_grid_lookup[mi]
                        stable_grid_lookup[mi].add(mj)
            for mi, mj in full_grids_to_purge:
                del full_grids[mi][mj]
                if len(full_grids[mi]) == 0:
                    del full_grids[mi]
            if False and len(stable_grid_lookup) > 30:
                # assert False
                ys_to_kill = (len(stable_grid_lookup) - 5) // 2
                for y in range(-ys_to_kill, ys_to_kill + 1):
                    xs_to_kill = (len(stable_grid_lookup[y]) - 5) // 2
                    for x in range(-xs_to_kill, xs_to_kill + 1):
                        if x in stable_grid_lookup[y]:
                            stable_grid_lookup[y].remove(x)

        if step_count % report_rate == 0:
            print('individual_tile_count', individual_tile_count)
            print('stable grids', stable_grids[0] + stable_grids[1])
            print('new queue', new_queue_len)

        tile_count = full_grid_count + stable_grid_count + individual_tile_count
        queue = new_queue
        # print(tile_count, step_count, '/', steps)
        if step_count % report_rate == 0:
            print(step_count, '/', steps)
        step_count += 1
    return tile_count


small_vector = ''
small_vector_2 = ''
official_vector = ''


def run_tests():
    v = '''...
.S.
...'''
    # for i in range(20):
    #     run_test(solve2, [v, i], (i + 1) ** 2)
    v = '''S#.
.##
...'''
    # run_test(solve2, [v, 0], 1)
    # run_test(solve2, [v, 1], 3)
    # run_test(solve2, [v, 2], 5)
    # run_test(solve2, [v, 3], 9)
    # run_test(solve2, [v, 4], 14)
    # run_test(solve2, [v, 5], 22)
    # run_test(solve2, [v, 6], 31)
    # run_test(solve2, [v, 7], 40)
    # run_test(solve2, [v, 8], 51)
    # run_test(solve2, [v, 9], 65)
    # run_test(solve2, [v, 10], 78)
    # run_test(solve2, [v, 11], 92)
    # run_test(solve2, [v, 12], 111)
    # run_test(solve2, [v, 13], 128)
    # run_test(solve2, [v, 14], 145)
    # run_test(solve2, [v, 15], 169)
    # run_test(solve2, [v, 16], 190)
    # run_test(solve2, [v, 17], 210)
    # run_test(solve2, [v, 18], 239)
    # run_test(solve2, [v, 19], 264)
    run_test(solve2, [v, 100], 287)

    v = '''...#.
S###.
.#.#.
.###.
.....'''

    # run_test(solve2, [v, 0], 1)
    # run_test(solve2, [v, 1], 3)
    # run_test(solve2, [v, 2], 6)
    # run_test(solve2, [v, 4], 13)
    # run_test(solve2, [v, 5], 18)
    # run_test(solve2, [v, 6], 23)
    # run_test(solve2, [v, 7], 31)
    # run_test(solve2, [v, 8], 42)
    # run_test(solve2, [v, 9], 56)
    # run_test(solve, [small_vector, 6], 16)
    # run_test(solve, [official_vector, 64], 3858)

    # run_test(solve2, [small_vector, 1], 2)
    # run_test(solve2, [small_vector, 2], 4)
    # run_test(solve2, [small_vector, 3], 6)
    # run_test(solve2, [small_vector, 4], 9)
    # run_test(solve2, [small_vector, 5], 13)
    # run_test(solve2, [small_vector, 6], 16)
    # run_test(solve2, [small_vector, 7], 22)
    # run_test(solve2, [small_vector, 8], 32)
    # run_test(solve2, [small_vector, 9], 32)
    # run_test(solve2, [small_vector, 10], 50)
    # run_test(solve2, [small_vector, 11], 50)
    # run_test(solve2, [small_vector, 12], 50)
    # run_test(solve2, [small_vector, 13], 50)
    # run_test(solve2, [small_vector, 50], 1594)
    # run_test(solve2, [small_vector, 100], 6536)
    # run_test(solve2, [small_vector, 500], 167004)
    # run_test(solve2, [small_vector, 1000], 668697)
    # run_test(solve2, [small_vector, 5000], 16733044)
    # run_test(solve2, [official_vector, 500], 3858)
    # run_test(solve2, [official_vector, 26501365], 3858)


small_vector = r'''...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........'''

small_vector_2 = r'''broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output'''

official_vector = r'''...................................................................................................................................
..#....#..............#.................#......#...................................##...............#.......#....#..#...#..........
.............#.#.........#....#...#...............#........#.............................##..#...#......#.............#.........#..
...................................#.#......#....#......##....................##...#.#.#....#......#....#.........#.........#.#.#..
........#..........................................................................................#.....##......#......#.......#..
..#...........#......#.............#.........................................#.....#...............#..#.....#.............#....#...
..#................#..................................#...................................##...............#........#.........#....
...................#....#........#..#....#...........#..........................................#.#................#...........#...
.#......#............#.....##.#...#.............................................#..#......#......#..#..............................
........................#...#..#.......#..#..................#.................#............#..#........#......#...#.....#.#.......
..............#...#................#..#............#........#...................#.....................#....#.......................
........#.#........#...#.#...#...#..#..#..#.#.............#..#................................#..........................#.........
..............#..#..#........#.......#..##...#...........#.....#..................#.....#.................#........#.....#...#.....
..#...........##...........#.......................................#.#..................#..#.................................#.....
.......................#.#...........#.....#...........#.......#.......#.#............##..#..#......................#..............
..#.........#.......#........#.#.#.#.#...#................#.......#...#................#...#...................#............#......
.#.....#........#..............#....#..............................#.#....#..............#....#.................#....#..#..........
................#..#..#.......................................#.#..........#.#.......................#.#.......#...#.............#.
.#...#......#....#.........................#...................##.....#......................#.........#........#.#.#....#...#.....
..#.....................##..........#........................#.................................#..#..........###................##.
.................#....#........#...#..#......................................#..................#.#....#.#.....#...##.##...##..#...
........#....##..#.................................................#..#......................#............#.......#.#......##..#...
.................#....................#...............#...#...#...#....#......#..............##..........#........#...........#....
.......##......#..................##..#........##.....#.#..#................#................#......#......#.#...............#.....
..............#...............................#.........#..............................................#.....#......#......#.#.#...
.#......#...........................#.........#..#...........#.....#..#.#..#............................................#..#.......
.#.....#...##..............#.#..#.................#...##..#.......#...................#........#.......#..................###......
.#...#.....................#.........................#....#.........#.......#...........................#.......#....##.#..#.......
....#.....................#......................#........................#.................................#....#.....#...##..##..
...#...#.........#............#..............##...#...............#......................#.........#...............#...........#...
........................#........................#.......#....#.............#....#......##................#.......#..#.......###...
.......#.........#.#....................#...................#.....##.........#.......................#....#....#......###..........
...................#...#.....#..................##......#................##...#......................#.#........#..................
...#.....#.....#.#...#..#...........#.....##.........#......#....................#...........................#.....................
..#........#....#.......#........................#............##.............#.....#....................#...#........#.............
............#..........#.................#.###..........................##.....#..#....#...#..#..............#.##..................
.#............#......#............#..................................###.................#.#.......................................
.#.#..#.......#.#..#............................#...................................................................#....#.....#...
................##.#................................................#..........................................#...#...............
.#.....#.##........#..........................#.#..............#......#...........#.......#.......#..........#.#...##........#.....
................#..#................#..................#..##........#..................#......................#..............#...#.
........#.....#....#............#........#...#............#.#.#.....#...........#.#....#...........................................
.#........#.......#..........................................##....#.#.............#.............#....#............#.............#.
.#....#........#......................#...........#....#.............................................#...............#......#......
................#............#.......#.............#............#.............#.....##...............#..................#...#......
.#..#....#..#.#.........#...#...........#.......................#..............#....#............#....#..#.................#.......
....#..........................#.....#......#..................##..............#.........##..#............................#........
....#.....................................#..#..............#..#........................................#..........................
.....#...............#...........#..#.........#........#.....#...................................#...................#.............
.........#...................#....#........#........................................#.........#..#.#....................#.....#....
....................#...................................#....#...................#.......#............#......#.....................
......................#.................#..#...###.....#..#.......#..#...#..........#....#...#..#....#......................#......
..................#.##.................#....#...#...........##....................#....#.............#.......#..................#..
.......#........#.....#..#.....................#.....................#...........#..........#.......#.............#..........#.....
.##................###.........##........###.........#.#....#..............#..#..............#..............................#......
....#..............##..........#.............#....#................................#.............#............#.#...........#......
...................#.#.......#.....#...#...............#..........#......#.#........#....#.......#.................................
........................#............................#.#...........#..........#................#......#...#.#.................#....
...#..........................................#...#.................................#...................#...#........#...........#.
..............#................#...#.......#....................#...#..............#........#....##.#.......#......................
................#..#.#.......#.#........#.........#...#......#....................................#..............#..#............#.
........#..#........#.##..##..................#...#.......................#.#..........................#................##.........
..............................#.....#...#................#.............#.............#...#..........................#..............
.......#.....#.........#............##...............#..........................#......#.#..#.......#....#..#.......#..#...........
...........................#................#........#..............#....#............#..................................#..#......
.................................................................S.................................................................
.....#........#..##..........#..#...#..........#.#...........#.#....#..........##........#..........#..#.......#..#................
.......#......#......#...#...........#.##......#...#......#..........................#.......#.....................................
...........................#.............#......#..........#.#.....#..................##..........#...................#............
........#.............##......#...#......................##...#........#..........................#............#...................
......................#...#....#..#.##...#..#....#............##........................#..............#..#........#..##...........
...............................................#......#...........................#...#............#.....#........#................
............#..........#.....#.....#........#...........#................#......#...####......#.........#.......................#..
.............#........#..#.#..........#.##...#.#..#....#..........................#...#..#...###...................#............#..
..............#..#...........#.............#.#...#......................#..........................................................
..............#..........#..#.......#.........................#.#......#...#..................#..#......#..........................
................#.........#...........#............#........#.#.#....................................#.............................
........................#...#..#..#....#...................#...........#..................##.....#..............#................#.
.#......##...........#...#.............##........#..........#..........#...#...#.#......#.#....#...##........##....................
.......................##...#......#......#....#.............#.....#..............#.....................#.....#.........#...#..#.#.
.................................#..#....#....##...................#......#...#..............................##....................
...#......##..........#.............#.#....#................#...#............#.........#..#................###...........#..#......
.#..........#.........#....##.#....#......##.#....#.#...........#...##........#............#....#.#...#.#.....................#....
..#........#.................#.#...........................#...............#........#.....#.#...............#........#.#...........
..#...........#..........#....#..#............................#........#............................#..#..................##.......
...........##..............................#..##.......................##...#....................#.................................
...........................#......##...#.....#..............#...#....#................#...#.....##...............#......#..........
.......#..#...#................#...#...........#........#.#.#..................#..............#...#.....................##.........
.................#.#.....................#.#.............#..............................#......#.......#.......#......##.....#.....
............#.......#..............#........#..#......#..#................................#...#.....#.#..........#......#......#...
...................#...............................................#..............#........#.#..................##..............##.
...#..............................#.........#................#................#.#...#.......#.....#.........#......................
.#.#.#...............#...................##......#......................#............#........................#.......#........#...
......#.....#....#......#..........#...#...##.............#.#..............................#.#..#...........#......##..............
....................#...#........#..#..#....#................................#.......#..#..##..................#.........#.........
.......#...#.........#..............#................#...#.........#......................................#..........#...#.#.....#.
..##..#.....................................#.....#........#....#.....#....................................#..........#.........##.
.#.........................................##....#.........................#..#.........#.............#.......###..................
...........#...##..................................##..#....#.......#....#..#.......#......................#......#.#.#...#........
...........#...#.......................#....#..##..................#............#.#...##....#.......................###............
..........#......##........................#........#.......#......#................................#..............................
...................##....#..#................#........................#...#....#....#....#........#..........#.....#....#..........
.......................#.....#...................#...#...#..#.............#.#..................................#..#...#..........#.
.................#.....................................................#.#.........................#........................#......
................#..........#.........................#.##.##...........#.................................#.........#..#............
....##....##......##.....#....................#......#..........#..........................................#...#..........##.......
...#..........#..........#..........#............##...#...#.#...................#...#.............#.......#....................#...
.....#........#.........#............................#..#.#............#.....#...............#..........#...#..................#...
...............#...#.#...#.......#........................#........................................#......#..............#.........
.....#.#............#.....#.....................................#....#...##.................................#....#..#..#.....#.#...
....#...#..#.....#...................#..#...................#.....#...#......#.....................#.....#....#.#.....##..##.......
.........................#........................#....#..#.#......#.....#.................................#.........#...#.........
.....#.............#......................#.........#......................................#........................#..#.#.#.....#.
.........#.#.......................#.#..#...........#.##......#.............#......................................#.....#....###..
.............#...................#...#.................#.#......#....#.....#.#..........#.....#....#...#.#......#...#...##....#..#.
......##......#.................#..#....................#....#..#.......#...................##......#.......#....#...#...#.#.......
..#....#........##.......##.#...#...........................#.......................#.....#...#.......##..................#........
.....#...........#.#...............#.#......#..#..........#..#....................................##......#..........#...#..#...#..
.#....................##...#.............................##.....#.................#........###...........#...#..................#..
.....#..#....#...#....#........#..#..#.....#....................................#......#....#.##.........#.....................#...
.......#............#................#......#.#....................#...#.................#.............#.......##.#................
..#.....#..............#........................#............#........#..........#..............#..##.....#.#........##......#..#..
..........#.............#................#...................#..............................#......#...............................
....#....................#.#....#................#.##.......................#......................#.....................#....#....
..#...#................##..#.........#.............#..#.........#............................#.......#........#...#.......#....##..
....#..#.................#....#................................................#...........#.......#...........#..............#....
...#...#................#...........#........#..#...#....................#........#.....##...........#.#...........##.....#.....##.
...........#.....#..#........#.....#..........#.#......#.#........................................#...#.....................#......
............................#........##..........#......................................................#........#....#.#...#.#....
..#..#.........#.#..........#.........#.........#............................#..#....#......##..#......#..............#............
...................................................................................................................................'''

run_tests()