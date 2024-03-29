from enum import IntEnum
from numpy import Infinity
from test_utils import run_test
from typing import List, Tuple, Dict, Set
from math import sqrt, ceil, floor, prod, lcm
import re
import numpy as np
from functools import cache


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iadd__(self, tx):
        assert isinstance(tx, Tx)
        self.x += tx.dx
        self.y += tx.dy
        return self

    def __add__(self, tx):
        assert isinstance(tx, Tx)
        return Point(self.x + tx.dx, self.y + tx.dy)


class Tx:
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy


class TestSuite:
    def __init__(self):
        self.tests = []

    def add_new_test(self, pt):
        self.tests.append(pt)

    @property
    def tests_remaining(self):
        return len(self.tests)

    @property
    def current_test(self):
        return self.tests[0]

    def finish_test(self):
        self.tests.pop(0)


class Stack:
    def __init__(self):
        self.queue = []

    def add_new_test_suite(self):
        self.queue.append(TestSuite())

    @property
    def suites_remaining(self):
        return len(self.queue) > 0

    @property
    def current_suite(self):
        return self.queue[-1]

    @property
    def path_length(self):
        l = 0
        for i, suite in enumerate(self.queue[:-1]):
            e = suite.current_test.edges[self.queue[i + 1].current_test]
            l += e.weight
        return l

    def finish_suite(self):
        self.queue.pop()


visited = {
    '.': 'x',
    '>': 'r',
    '<': 'l',
    '^': 'u',
    'v': 'd'
}

unvisited = {value: key for key, value in visited.items()}

left = Tx(-1, 0)
right = Tx(1, 0)
up = Tx(0, -1)
down = Tx(0, 1)

dirs = {
    '#': [],
    '.': [left, right, up, down],
    '>': [right],
    '<': [left],
    'v': [down],
    '^': [up]
}


def print_grid(grid: List[List[str]]) -> None:
    print()
    print('\n'.join(''.join(row) for row in grid))


def solve(data: str, no_slopes=False) -> int:
    stack = Stack()
    grid = [['.' if no_slopes and c != '.' and c != '#' else c for c in row]
            for row in data.splitlines()]
    for sx, c in enumerate(grid[0]):
        if c == '.':
            stack.add_new_test_suite()
            stack.current_suite.add_new_test(Point(sx, 0))
            break
    best_so_far = 0

    while stack.suites_remaining:

        while stack.current_suite.tests_remaining:
            pt = stack.current_suite.current_test

            # print('testing', pt.x, pt.y)

            next_directions = dirs[grid[pt.y][pt.x]]
            grid[pt.y][pt.x] = visited[grid[pt.y][pt.x]]

            test_exhausted = True
            if pt.y == len(grid) - 1:
                if stack.path_length > best_so_far:
                    print_grid(grid)
                    print('Reached the end in ', stack.path_length)
                    best_so_far = stack.path_length
            else:
                nd = []
                for d in next_directions:
                    np = pt + d
                    if np.y >= 0 and np.y < len(grid) and grid[np.y][np.x] in visited.keys():
                        nd.append(Point(np.x, np.y))
                if len(nd) > 0:
                    stack.add_new_test_suite()
                    for n in nd:
                        stack.current_suite.add_new_test(n)
                    test_exhausted = False
            if test_exhausted:
                grid[pt.y][pt.x] = unvisited[grid[pt.y][pt.x]]
                stack.current_suite.finish_test()

        stack.finish_suite()
        if stack.suites_remaining:
            pt = stack.current_suite.current_test
            grid[pt.y][pt.x] = unvisited[grid[pt.y][pt.x]]
            stack.current_suite.finish_test()

    return best_so_far - 1


class Node:
    def __init__(self, x, y):
        self.edges = {}
        self.x = x
        self.y = y

    def __str__(self):
        return f'{self.x}:{self.y}'

    def __repr__(self):
        return str(self)


class Edge:
    def __init__(self, weight, src, dst):
        self.weight = weight
        self.src = src
        self.dst = dst

    def __str__(self):
        return f'{self.src}-{self.weight}->{self.y}'

    def __repr__(self):
        return str(self)


def solve2(data: str) -> int:
    stack = Stack()
    grid = [['.' if c != '.' and c != '#' else c for c in row]
            for row in data.splitlines()]

    nodes = {}

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '.':
                nodes.setdefault(y, {})
                nodes[y][x] = Node(x, y)
    for y, node_row in nodes.items():
        for x, node in node_row.items():
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nx = x + dx
                ny = y + dy
                if ny >= 0 and ny < len(grid) and grid[ny][nx] == '.':
                    node.edges[nodes[ny][nx]] = Edge(1, node, nodes[ny][nx])

    nodes_reduced = True
    while nodes_reduced:
        nodes_reduced = False
        for y, node_row in nodes.items():
            for x, node in node_row.items():
                if len(node.edges) == 2:
                    ea, eb = node.edges.values()
                    na = ea.dst
                    nea = na.edges[node]
                    nb = eb.dst
                    neb = nb.edges[node]
                    nea.weight = neb.weight = nea.weight + neb.weight
                    nea.dst = nb
                    na.edges[nb] = nea
                    neb.dst = na
                    nb.edges[na] = neb
                    
                    del na.edges[node]
                    del nb.edges[node]
                    del nodes[y][x]
                    if len(nodes[y]) == 0:
                        del nodes[y]
                    
                    nodes_reduced = True
                    
                    break
            if nodes_reduced:
                break

    sx = next(iter(nodes[0].keys()))
    stack.add_new_test_suite()
    stack.current_suite.add_new_test(nodes[0][sx])
    best_so_far = 0

    while stack.suites_remaining:

        while stack.current_suite.tests_remaining:
            node = stack.current_suite.current_test

            grid[node.y][node.x] = visited[grid[node.y][node.x]]

            test_exhausted = True
            if node.y == len(grid) - 1:
                pl = stack.path_length
                if pl > best_so_far:
                    # print_grid(grid)
                    print('Reached the end in ', pl)
                    best_so_far = pl
            else:
                nd = []
                for d in node.edges:
                    if grid[d.y][d.x] in visited.keys():
                        nd.append(d)
                if len(nd) > 0:
                    stack.add_new_test_suite()
                    for n in nd:
                        stack.current_suite.add_new_test(n)
                    test_exhausted = False
            if test_exhausted:
                grid[node.y][node.x] = unvisited[grid[node.y][node.x]]
                stack.current_suite.finish_test()

        stack.finish_suite()
        if stack.suites_remaining:
            node = stack.current_suite.current_test
            grid[node.y][node.x] = unvisited[grid[node.y][node.x]]
            stack.current_suite.finish_test()

    return best_so_far


small_vector = ''
small_vector_2 = ''
official_vector = ''


def run_tests():
#     run_test(solve2, [r'''#.#
# #.#
# #.#'''], 2)
#     run_test(solve2, [r'''#.##
# #..#
# ##.#'''], 3)
#     run_test(solve2, [r'''#.#####
# #.....#
# #.#.#.#
# #.....#
# ####.##'''], 13)
    # run_test(solve, [small_vector], 94)
    # run_test(solve, [official_vector], 2094)
    # run_test(solve2, [small_vector], 154)
    run_test(solve2, [official_vector], 2094)


small_vector = r'''#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#'''

small_vector_2 = r'''0,0,1~0,5,1
0,6,1~0,9,1
0,0,2~0,0,2
0,3,2~0,8,2'''

official_vector = r'''#.###########################################################################################################################################
#...#...#...#...#...#.....#####.........#...#.............#...#...#...#...#...#...........#.....#.......#...#.....#.......#...###...#...#####
###.#.#.#.#.#.#.#.#.#.###.#####.#######.#.#.#.###########.#.#.#.#.#.#.#.#.#.#.#.#########.#.###.#.#####.#.#.#.###.#.#####.#.#.###.#.#.#.#####
#...#.#.#.#...#.#.#.#...#.......#.......#.#.#...........#.#.#.#.#...#...#.#.#.#.........#.#.#...#.....#.#.#.#...#...#.....#.#...#.#...#.....#
#.###.#.#.#####.#.#.###.#########.#######.#.###########.#.#.#.#.#########.#.#.#########.#.#.#.#######.#.#.#.###.#####.#####.###.#.#########.#
#...#.#...#.....#.#...#.#.........#...###.#.#...###...#.#.#.#.#.........#...#.#...#####.#...#.#...#...#.#.#...#.....#...#...#...#...#.......#
###.#.#####.#####.###.#.#.#########.#.###.#.#.#.###.#.#.#.#.#.#########.#####.#.#.#####.#####.#.#.#.###.#.###.#####.###.#.###.#####.#.#######
###...###...#...#...#.#.#...#.......#...#.#.#.#.#...#...#.#.#.#.....#...#.....#.#...#...#.....#.#.#.#...#.#...#...#.#...#.#...#.....#.......#
#########v###.#.###.#.#.###.#.#########.#.#.#.#.#.#######.#.#.#.###.#.###.#####.###.#.###.#####.#.#.#.###.#.###.#.#.#.###.#.###.###########.#
#.......#.>...#...#.#.#.#...#.#...#.....#.#.#.#.#.......#.#.#.#...#.#...#.#...#.#...#.#...#...#.#.#.#...#.#...#.#...#...#.#...#.#...........#
#.#####.#v#######.#.#.#.#.###.#.#.#.#####.#.#.#.#######.#.#.#.###.#.###.#.#.#.#.#.###.#.###.#.#.#.#.###.#.###.#.#######.#.###.#.#.###########
#...#...#.#.......#.#.#.#...#.#.#...#####.#.#.#.#...#...#...#...#.#...#.#.#.#.#.#.>.>.#...#.#.#.#.#.#...#...#.#.....#...#.#...#.#.###...#...#
###.#.###.#.#######.#.#.###.#.#.#########.#.#.#.#.#.#.#########.#.###.#.#.#.#.#.###v#####.#.#.#.#.#.#.#####.#.#####.#.###.#.###.#.###.#.#.#.#
#...#.....#.....#...#.#.#...#.#.###...#...#.#.#...#.#.........#...###...#.#.#...###.....#.#.#.#.#.#.#.>.>...#.#...#.#.#...#.....#.....#...#.#
#.#############.#.###.#.#.###.#.###.#.#.###.#.#####.#########.###########.#.###########.#.#.#.#.#.#.###v#####.#.#.#.#.#.###################.#
#.....#.......#.#.#...#.#.....#...#.#.#...#.#...#...#####...#.......#.....#.......###...#.#.#.#.#.#...#...#...#.#.#.#.#...#.................#
#####.#.#####.#.#.#.###.#########.#.#.###.#.###.#.#######.#.#######.#.###########.###.###.#.#.#.#.###.###.#.###.#.#.#.###.#.#################
#...#...#...#.#.#.#.###...#.......#.#.#...#.....#.#...>.>.#.#.......#...#...#.....#...###...#...#.#...#...#.#...#.#.#...#.#...#...#.........#
#.#.#####.#.#.#.#.#.#####.#.#######.#.#.#########.#.###v###.#.#########.#.#.#.#####.#############.#.###.###.#.###.#.###.#.###.#.#.#.#######.#
#.#.#...#.#...#.#.#...#...#...>.>.#.#.#.#.........#.###...#.#.........#.#.#.#.#.....#...###...###.#...#...#...###.#.#...#.#...#.#.#.#.......#
#.#.#.#.#.#####.#.###.#.#######v#.#.#.#.#.#########.#####.#.#########.#.#.#.#.#.#####.#.###.#.###.###.###.#######.#.#.###.#.###.#.#.#.#######
#.#...#...#...#...###.#.#####...#.#.#.#.#...#.....#.#.....#...........#.#.#.#.#.......#...#.#...#...#.###.......#.#.#.#...#.....#...#.......#
#.#########.#.#######.#.#####.###.#.#.#.###.#.###.#.#.#################.#.#.#.###########.#.###.###.#.#########.#.#.#.#.###################.#
#.#...#.....#.......#...###...###...#.#.###...###...#...#...#.........#.#.#.#.#...........#.#...###...###.......#...#...###.................#
#.#.#.#.###########.#######.#########.#.###############.#.#.#.#######.#.#.#.#.#.###########.#.###########.#################.#################
#.#.#.#.#...........###...#.........#...#...#...###...#.#.#.#.#.......#.#.#...#.......#.....#.###.......#.........#...#...#.#...............#
#.#.#.#.#.#############.#.#########.#####.#.#.#.###.#.#.#.#.#.#.#######.#.###########.#.#####.###.#####.#########.#.#.#.#.#.#.#############.#
#.#.#.#.#...........#...#...........#...#.#.#.#.....#...#.#...#.......#...#...#.....#...#...#...#.....#.#.........#.#...#.#...#.............#
#.#.#.#.###########.#.###############.#.#.#.#.###########.###########.#####.#.#.###.#####.#.###.#####.#.#.#########.#####.#####.#############
#.#.#...###.........#.....#.......###.#.#.#.#.............#...#.......#.....#.#...#.#.....#.....#...#.#.#.#...#...#.....#.#...#.....#.......#
#.#.#######v#############.#.#####.###.#.#.#.###############.#.#.#######.#####.###.#.#.###########.#.#.#.#v#.#.#.#.#####.#.#.#.#####.#.#####.#
#...#.....#.>...###.....#...#...#...#.#.#.#.#.....#.........#...#...###.....#...#.#.#.........#...#...#.>.>.#...#.#.....#.#.#.#...#.#.#.....#
#####.###.#v###.###.###.#####.#.###.#.#.#.#.#.###.#.#############.#.#######.###.#.#.#########.#.#########v#######.#.#####.#.#.#.#.#.#.#.#####
#...#...#.#.###...#.#...#...#.#.....#.#.#.#.#...#.#.........#.....#...#...#...#.#.#.###.......#.......#...###.....#.....#...#.#.#.#...#.....#
#.#.###.#.#.#####.#.#.###.#.#.#######.#.#.#.###.#.#########v#.#######.#.#.###.#.#.#.###.#############.#.#####.#########.#####.#.#.#########.#
#.#.#...#...#.....#.#.###.#.#.#...#...#.#.#...#.#.#...#...>.>.#.......#.#.#...#.#.#...#.........#.....#.....#.###...#...#...#.#.#...........#
#.#.#.#######.#####.#.###.#.#v#.#.#.###.#.###.#.#.#.#.#.###v###.#######.#.#.###.#.###.#########.#.#########.#.###.#.#.###.#.#.#.#############
#.#.#.....###.....#.#...#.#.>.>.#.#...#.#.#...#.#...#.#.###.#...###...#.#.#...#.#.#...###.......#.#...#.....#...#.#...#...#...#.............#
#.#.#####.#######.#.###.#.###v###.###.#.#.#.###.#####.#.###.#.#####.#.#.#.###.#.#.#.#####v#######.#.#.#.#######.#.#####.###################.#
#.#.....#.......#.#...#...###...#...#.#.#.#.#...#.....#.#...#.....#.#.#.#...#.#.#.#...#.>.>.#...#.#.#.#.......#.#.#.....#...#...#...........#
#.#####.#######.#.###.#########.###.#.#.#.#.#.###.#####.#.#######.#.#.#.###.#.#.#.###.#.#v#.#.#.#.#.#.#######.#.#.#.#####.#.#.#.#.###########
#.#...#.......#.#.#...###.......###...#.#.#.#...#.....#.#...###...#.#.#...#...#.#.#...#.#.#...#...#.#.#...#...#.#.#.....#.#.#.#.#...#.......#
#.#.#.#######.#.#.#.#####.#############.#.#.###.#####.#.###.###.###.#.###.#####.#.#.###.#.#########.#.#.#.#.###.#.#####.#.#.#.#.###v#.#####.#
#...#.......#.#.#.#.#.....#.........###...#...#.....#...###...#.....#.#...#.....#.#.#...#...###.....#...#...#...#.#.....#.#.#.#.#.>.#.#.....#
###########.#.#.#.#.#.#####.#######.#########.#####.#########.#######.#.###.#####.#.#.#####.###.#############.###.#.#####.#.#.#.#.#v#.#.#####
#...........#.#.#...#.......#.......#.......#.#...#.#.....#...#.......#.###.....#.#...#...#.#...#.....#.....#.#...#.......#.#.#.#.#...#.....#
#.###########.#.#############.#######.#####.#.#.#.#.#.###.#.###.#######.#######.#.#####.#.#.#.###.###.#.###.#.#.###########.#.#.#.#########.#
#.#.........#...#.............#...###.#.....#...#...#...#...###...#...#.......#.#.#.....#...#.....#...#.#...#...#...........#.#.#.#.........#
#.#.#######.#####.#############.#.###.#.###############.#########.#.#.#######.#.#.#.###############.###.#.#######.###########.#.#.#.#########
#...#...#...#...#...#.....#.....#...#.#...#...#.....#...#.......#...#.#.......#...#.........#.....#.....#.......#.....#...#...#...#.........#
#####.#.#.###.#.###.#.###.#.#######.#.###.#.#.#.###.#.###.#####.#####.#.###################.#.###.#############.#####.#.#.#.###############.#
#.....#...#...#...#.#...#...#.......#.#...#.#.#...#.#.....#.....#...#.#...#...#.............#...#...........#...#...#...#...#...............#
#.#########.#####.#.###.#####.#######.#.###.#.###.#.#######.#####.#.#.###.#.#.#.###############.###########.#.###.#.#########.###############
#...........#.....#.....#...#...#.....#...#.#.#...#.#.....#.....#.#.#.....#.#.#...............#...........#...###.#.###...#...#.............#
#############.###########.#.###.#.#######.#.#.#.###.#.###.#####.#.#.#######.#.###############.###########.#######.#.###.#.#.###.###########.#
#.............#...###...#.#...#.#.#.......#.#.#...#.#.#...#.....#.#.###...#.#...#...#...#...#...#.........#.......#...#.#.#.....###.........#
#.#############.#.###.#.#.###.#.#.#.#######.#.###.#.#.#.###v#####.#.###.#.#.###.#.#.#.#.#.#.###.#.#########.#########.#.#.#########.#########
#...............#.###.#.#...#.#...#.#...#...#.....#...#...>.>...#.#.#...#.#.#...#.#.#.#.#.#.....#.....#...#.....#.....#.#.....#.....#.......#
#################.###.#.###.#.#####v#.#.#.#################v###.#.#.#.###.#.#.###.#.#.#.#.###########.#.#.#####.#.#####.#####.#.#####.#####.#
#...#...#.........#...#.#...#...#.>.>.#...###.............#.#...#.#.#...#.#.#.###.#.#.#...###.........#.#.....#.#.#...#.....#.#.......#.....#
#.#.#.#.#.#########.###.#.#####.#.#v#########.###########.#.#.###.#.###.#.#.#.###.#.#.#######.#########.#####.#.#.#.#.#####.#.#########.#####
#.#...#...#.......#...#...#...#...#.#...#...#.....#.....#.#.#...#.#.#...#.#.#.....#...###...#...........#.....#.#.#.#...###.#.#.....###.....#
#.#########.#####.###.#####.#.#####.#.#.#.#.#####.#.###.#.#.###.#.#.#.###.#v#############.#.#############.#####.#.#.###.###.#.#.###.#######.#
#.#...#...#.....#...#.#.....#.......#.#...#...###.#.#...#.#.###.#.#...###.>.>...###.....#.#.#...#.........#...#.#.#...#.###.#.#...#.#...#...#
#.#.#.#.#v#####.###.#.#.#############.#######.###.#.#.###.#.###.#.#########v###.###.###.#.#.#.#.#.#########.#.#.#.###.#.###.#.###.#.#.#.#v###
#.#.#...#.>.#...#...#.#...#...#...#...###...#...#...#...#...#...#.........#...#...#...#.#.#.#.#.#...#...#...#...#.#...#.#...#...#.#.#.#.>.###
#.#.#####v#.#.###.###.###.#.#.#.#.#.#####.#.###.#######.#####.###########.###.###.###.#.#.#.#.#.###v#.#.#.#######.#.###.#.#####.#.#.#.###v###
#...###...#...###...#.#...#.#.#.#...#.....#...#.#.......#...#...#.........###...#.....#.#.#.#.#...>.>.#.#...#.....#...#.#...###.#.#...###...#
#######.###########.#.#.###.#.#.#####.#######.#.#.#######.#.###.#.#############.#######.#.#.#.#####v###.###.#.#######.#.###.###.#.#########.#
#.......#...#...###...#...#.#.#.#.....#...###...#.......#.#.....#.#.....###...#.......#...#...#.....###...#.#...#...#.#.#...#...#.#.........#
#.#######.#.#.#.#########.#.#.#.#.#####.#.#############.#.#######.#.###.###.#.#######.#########.#########.#.###.#.#.#.#.#.###.###.#.#########
#.........#...#.....#...#...#.#.#...#...#...#.....#.....#.....#...#.#...#...#.#.......###.......#.......#...###...#.#.#.#...#.#...#...#.....#
###################.#.#.#####.#.###.#.#####.#.###.#.#########.#.###.#.###.###.#.#########.#######.#####.###########.#.#.###.#.#.#####.#.###.#
###...#.............#.#...###...###.#.#.....#.#...#...#...###...###.#.#...#...#...###...#.....#...#.....#.........#.#.#.....#...#####...#...#
###.#.#.#############.###.#########.#.#.#####.#.#####v#.#.#########.#.#.###.#####.###.#.#####.#.###.#####.#######.#.#.###################.###
#...#...#...........#.#...#...#...#...#...#...#.#...>.>.#...###...#.#.#...#.#...#.....#.#...#.#.#...#...#.#.......#.#.#...#####...#...#...###
#.#######.#########.#.#.###.#.#.#.#######.#.###.#.###v#####.###.#.#.#.###.#.#.#.#######v#.#.#.#.#.###.#.#.#.#######.#.#.#.#####.#.#.#.#.#####
#...#...#.#.........#.#...#.#.#.#.#...###.#.###.#.###.#...#...#.#.#.#...#.#.#.#.....#.>.>.#.#...#.....#...#.......#...#.#...#...#.#.#.#.....#
###.#.#.#.#.#########.###.#.#.#.#.#.#.###v#.###.#.###.#.#.###.#.#.#.###.#.#.#.#####.#.#v###.#####################.#####.###.#.###.#.#.#####.#
###...#...#.........#...#.#.#.#.#.#.#...>.>.#...#...#...#.###.#.#.#...#.#.#...#...#...#.#...#.....................#...#...#.#...#.#.#.###...#
###################.###.#.#.#.#.#.#.#####v###.#####.#####.###.#.#.###.#.#.#####.#.#####.#.###.#####################.#.###.#.###.#.#.#.###v###
#.........#...#.....#...#...#.#.#.#.###...###.#...#...#...#...#.#.#...#.#.#.....#.###...#...#.......#...............#.###.#.#...#...#...>.###
#.#######.#.#.#.#####.#######.#.#.#.###.#####.#.#.###.#.###.###.#.#.###.#.#.#####.###.#####.#######.#.###############.###.#.#.###########v###
#.......#.#.#...#...#.......#...#...#...#####...#.....#...#...#.#.#...#...#.....#.#...#...#...#...#...###...#...#.....#...#.#.#...#...#...###
#######.#.#.#####.#.#######.#########.###################.###.#.#.###.#########.#.#.###.#.###.#.#.#######.#.#.#.#.#####.###.#.#.#.#.#.#.#####
#.......#...#...#.#.#...#...#.........#.....#.............#...#.#.#...###...#...#.#.....#.###...#.#.....#.#...#...###...###...#.#...#...#...#
#.###########.#v#.#.#.#.#.###.#########.###.#.#############.###.#.#.#####.#.#.###.#######.#######.#.###.#.###########.#########.#########.#.#
#.......#...#.#.>.#.#.#.#...#...........#...#.............#...#.#.#...#...#.#...#.........#.......#.#...#.......###...#...#...#...........#.#
#######.#.#.#.#v###.#.#.###.#############.###############.###.#.#.###.#.###.###.###########.#######.#.#########v###.###.#.#.#.#############.#
#.......#.#...#...#.#.#.#...#.............#...#...........###...#...#.#...#...#.........###...#...#.#.#.......>.>...#...#.#.#.###...#.......#
#.#######.#######.#.#.#.#.###.#############.#.#.###################.#.###.###.#########.#####.#.#.#.#.#.#######v#####.###.#.#.###.#.#.#######
#.........#...#...#...#.#...#.#...#.......#.#.#...................#...#...#...#...#.....#...#...#.#.#...#...#...#...#...#...#.....#...#...###
###########.#.#.#######.###.#.#.#.#.#####.#.#.###################.#####.###.###.#.#.#####.#.#####.#.#####.#.#.###.#.###.###############.#.###
#...........#...#...###.....#.#.#...#...#.#.#.#.....#.............#...#...#.#...#.#.......#.###...#.#...#.#.#.....#...#...#...........#.#...#
#.###############.#.#########.#.#####.#.#.#.#.#.###.#.#############.#.###.#.#.###.#########.###.###.#.#.#.#.#########.###.#.#########.#.###.#
#.....#.....###...#.........#...#.....#...#.#.#...#.#.............#.#.....#...#...#...#...#...#.#...#.#.#.#.#...#...#.###...#.........#.#...#
#####.#.###.###.###########.#####.#########.#.###.#.#############.#.###########.###.#.#.#.###.#.#.###.#.#.#.#.#.#.#.#.#######.#########.#.###
#.....#.#...#...#...........#...#.....###...#...#.#.#...#.........#...#.......#.#...#...#...#.#...#...#.#.#.#.#.#.#...#...###.......#...#...#
#.#####.#v###.###.###########.#.#####.###.#####.#.#.#.#.#.###########.#.#####.#.#.#########.#.#####.###.#.#.#.#.#.#####.#.#########.#.#####.#
#.......#.>.#...#.#.........#.#.#...#...#...#...#.#.#.#.#.#...###...#...#.....#...#...#...#...#.....###...#...#...#...#.#.#...#.....#.#.....#
#########v#.###.#.#.#######.#.#.#.#.###.###.#.###.#.#.#.#v#.#.###.#.#####.#########.#.#.#.#####.###################.#.#.#.#.#.#.#####.#.#####
#.....#...#...#.#.#...#.....#.#.#.#.#...#...#.#...#.#.#.>.>.#...#.#.#...#...#...#...#.#.#...###.......#...#.....#...#.#.#.#.#.#.......#.....#
#.###.#.#####.#.#.###.#.#####.#.#.#.#v###.###.#.###.#.###v#####.#.#.#.#.###.#.#.#.###.#.###.#########.#.#.#.###.#.###.#.#.#.#.#############.#
#...#.#.....#...#...#.#...#...#.#.#.>.>...###.#...#.#.#...#.....#.#...#.....#.#.#...#...#...#.........#.#.#.#...#.#...#.#.#.#.###...........#
###.#.#####.#######.#.###.#.###.#.###v#######.###.#.#.#.###.#####.###########.#.###.#####.###.#########.#.#.#.###.#.###.#.#.#.###v###########
#...#.......###...#...###.#...#.#.###...#...#.#...#...#...#.#...#...#...#...#.#.###...#...###.......###.#.#.#...#.#...#.#.#.#.#.>.#.........#
#.#############.#.#######.###.#.#.#####.#.#.#.#.#########.#.#.#.###.#.#.#.#.#.#.#####.#.###########v###.#.#.###.#.###.#.#.#.#.#.#v#.#######.#
#.....#.....#...#.....#...#...#.#.#.....#.#.#...#.....###.#.#.#...#...#...#.#.#.#...#.#.#...#...#.>.>...#.#.#...#...#.#.#.#.#.#.#.#.#.......#
#####.#.###.#.#######.#.###.###.#.#.#####.#.#####.###.###.#.#.###.#########v#.#.#.#.#.#.#.#.#.#.#.#v#####.#.#.#####.#.#.#.#.#.#.#.#.#.#######
#.....#.#...#.#.......#...#...#...#.......#.#...#...#.#...#...#...#...#...>.>.#...#...#.#.#...#.#.#.....#...#...#...#...#.#.#...#...#.......#
#.#####.#.###.#.#########.###.#############.#.#.###.#.#.#######.###.#.#.###v###########.#.#####.#.#####.#######.#.#######.#.###############.#
#...#...#.....#.......#...#...#.............#.#.#...#.#...#...#...#.#.#.###.........#...#.....#...#...#.......#.#...#...#.#...###...#.......#
###.#.###############.#.###.###.#############.#.#.###.###.#.#.###.#.#.#.###########.#.#######.#####.#.#######.#.###.#.#.#.###.###.#.#.#######
###...#...###.........#.....###.#...........#.#.#...#...#...#...#...#...#...........#...#...#.#.....#.........#.#...#.#.#.....#...#...#.....#
#######.#.###.#################.#.#########.#.#.###.###.#######.#########.#############.#.#.#.#.###############.#.###.#.#######.#######.###.#
#.......#...#...........#...###...#.......#...#...#...#.........#.....###.............#.#.#.#.#.......#...#...#...###.#.#.....#...#.....#...#
#.#########.###########.#.#.#######.#####.#######.###.###########.###.###############.#.#.#.#.#######.#.#.#.#.#######.#.#.###.###.#.#####.###
#.......#...#...........#.#...#.....#...#.........###.......#.....#...#...............#...#...#.....#.#.#...#.....###.#.#...#.....#.#.....###
#######.#.###.###########.###.#.#####.#.###################.#.#####.###.#######################.###.#.#.#########.###.#.###.#######.#.#######
#.......#...#.....#...###.#...#.......#.........###.........#...#...###...........#...#...#...#...#.#...#.........#...#...#.........#.......#
#.#########.#####.#.#.###.#.###################.###.###########.#.###############.#.#.#.#.#.#.###.#.#####.#########.#####.#################.#
#.#...#...#.......#.#.#...#...###...#...........#...#.......###.#.###.............#.#...#...#.#...#.......###.....#.....#.#.....#.......#...#
#.#.#.#.#.#########.#.#.#####.###.#.#.###########.###.#####v###.#.###.#############.#########.#.#############.###.#####.#.#.###.#.#####.#.###
#...#...#...........#...#.....#...#.#.......#...#.....###.>.>.#.#...#...#.......#...#.........#...............#...#...#.#.#.#...#.....#.#...#
#########################.#####.###.#######.#.#.#########.###.#.###.###.#.#####.#.###.#########################.###.#.#.#.#.#.#######v#.###.#
#...................#...#...###...#.#.......#.#.###.......###.#.###...#...#.....#.#...###...#...#...#...........#...#.#.#...#.....#.>.#...#.#
#.#################.#.#.###.#####.#.#.#######.#.###.#########.#.#####.#####.#####.#.#####.#.#.#.#.#.#.###########.###.#.#########.#.#v###.#.#
#...#...#...#.....#...#.#...#.....#.#.......#.#...#.....###...#.....#...###.......#.....#.#.#.#.#.#.#.....#...#...#...#...###...#.#.#...#...#
###.#.#.#.#.#.###.#####.#.###.#####.#######.#.###.#####.###.#######.###.###############.#.#.#.#.#.#.#####v#.#.#.###.#####.###.#.#.#.###.#####
###...#...#...###...###...###.#...#.........#...#.#...#...#...#.....###...###...........#.#.#.#.#.#...#.>.>.#.#...#...#...#...#...#...#...###
###################.#########.#.#.#############.#.#.#.###.###.#.#########.###.###########.#.#.#.#.###.#.#####.###.###.#.###.#########.###.###
#####...............#...#...#...#...#...###...#.#...#.#...###.#...#.....#...#...........#.#.#.#.#...#.#.#...#...#.#...#.#...#.....#...###...#
#####.###############.#.#.#.#######.#.#.###.#.#.#####.#.#####.###.#.###.###.###########.#.#.#.#.###.#.#.#.#.###.#.#.###.#.###.###.#.#######.#
#.....#...#...#.....#.#...#.#...#...#.#...#.#.#.....#...#...#.#...#...#.#...#...#.......#.#...#.#...#.#...#...#...#.#...#.....###...#...###.#
#.#####.#.#.#.#.###.#.#####.#.#.#.###.###.#.#.#####.#####.#.#.#.#####.#.#.###.#.#.#######.#####.#.###.#######.#####.#.###############.#.###.#
#...#...#...#...#...#.#.....#.#.#.....#...#.#.#...#.......#.#.#.#.....#...###.#.#.....###.....#...###.#...#...#.....#.........#.......#.....#
###.#.###########.###.#.#####.#.#######v###.#.#.#.#########.#.#.#.###########.#.#####v#######.#######.#.#.#.###.#############.#.#############
#...#.#...........#...#.#...#.#.#...#.>.>.#.#.#.#.#...#...#.#.#.#...#.....#...#.#...>.>.#...#.....#...#.#.#.#...#...#...#...#.#.......#.....#
#.###.#.###########.###.#.#.#.#.#.#.#.###.#.#.#.#.#.#.#.#.#.#.#.###.#.###.#.###.#.#####.#.#.#####.#.###.#.#.#.###.#.#.#.#.#.#.#######.#.###.#
#.....#.............###...#...#...#...###...#...#...#...#...#...###...###...###...#####...#.......#.....#...#.....#...#...#...#######...###.#
###########################################################################################################################################.#'''

run_tests()
