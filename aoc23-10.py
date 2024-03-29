from enum import IntEnum
from numpy import Infinity
from test_utils import run_test
from typing import List, Tuple
from math import sqrt, ceil, floor
import re


up = 0
left = 1
right = 2
down = 3


swaps = {
    'L': '└',
    'J': '┘',
    'F': '┌',
    '7': '┐',
    '-': '─',
    '|': '│',
    'S': 'X',
    '.': '.',
    '\n': '\n'
}


def find_start(mp: List[str]) -> Tuple[int, int]:
    for i, row in enumerate(mp):
        for j, cell in enumerate(row):
            if cell == 'X':
                return i, j


def pad(m: str) -> str:
    w = m.find('\n')
    empty_line = '.' * (w + 1)
    padded_map = '\n'.join([empty_line, m, empty_line]).replace('\n', '.\n.')
    s = ''
    for c in padded_map:
        s += swaps[c]
    return s


def dirtod(dir: int) -> Tuple[int, int]:
    if dir == up:
        return -1, 0
    elif dir == left:
        return 0, -1
    elif dir == right:
        return 0, 1
    elif dir == down:
        return 1, 0
    assert False, dir


def opposite(dir: int) -> int:
    if dir == up:
        return down
    elif dir == left:
        return right
    elif dir == right:
        return left
    elif dir == down:
        return up
    assert False, dir


possible_connections = {
    'X': {
        up: True,
        left: True,
        right: True,
        down: True
    },
    '┌': {
        up: False,
        left: False,
        right: True,
        down: True
    },
    '└': {
        up: True,
        left: False,
        right: True,
        down: False
    },
    '┘': {
        up: True,
        left: True,
        right: False,
        down: False
    },
    '┐': {
        up: False,
        left: True,
        right: False,
        down: True
    },
    '│': {
        up: True,
        left: False,
        right: False,
        down: True
    },
    '─': {
        up: False,
        left: True,
        right: True,
        down: False
    },
    '.': {
        up: False,
        left: False,
        right: False,
        down: False
    }
}


def left_side(dir):
    if dir == up:
        return left
    if dir == left:
        return down
    if dir == right:
        return up
    if dir == down:
        return right


def right_side(dir):
    if dir == up:
        return right
    if dir == left:
        return up
    if dir == right:
        return down
    if dir == down:
        return left


def solve(data: str) -> int:
    padded_map = pad(data)
    mp = padded_map.splitlines()
    track = [['.' for _ in mp[0]] for _ in mp]
    si, sj = find_start(mp)
    pi, pj = si, sj
    i, j = si, sj
    loop_len = 0
    while True:
        for d, p in possible_connections[mp[i][j]].items():
            if p:
                di, dj = dirtod(d)
                ni, nj = i + di, j + dj
                if pi != ni or pj != nj:
                    n = mp[ni][nj]
                    if possible_connections[n][opposite(d)]:
                        # this is the next node
                        pi, pj = i, j
                        i, j = ni, nj
                        loop_len += 1
                        track[i][j] = n
                        if i == si and j == sj:
                            print('\n'.join([''.join(s) for s in track]))
                            return ceil(loop_len / 2.0)
                        break


def solve2(data: List[str]):
    padded_map = pad(data)
    mp = padded_map.splitlines()
    track = [['.' for _ in mp[0]] for _ in mp]
    si, sj = find_start(mp)

    start_connections = {up: False, left: False, right: False, down: False}
    for d in [up, left, right, down]:
        di, dj = dirtod(d)
        ni, nj = si + di, sj + dj
        neighbour = mp[ni][nj]
        if neighbour != '.':
            rd = opposite(d)
            if possible_connections[neighbour][rd]:
                start_connections[d] = True
    if start_connections[up]:
        if start_connections[down]:
            c = '│'
        elif start_connections[left]:
            c = '┘'
        elif start_connections[right]:
            c = '└'
    elif start_connections[down]:
        if start_connections[left]:
            c = '┐'
        elif start_connections[right]:
            c = '┌'
    else:
        c = '─'
    mp[si] = mp[si][:sj] + c + mp[si][sj + 1:]

    pi, pj = si, sj
    i, j = si, sj
    inside_count = 0
    while True:
        for d, p in possible_connections[mp[i][j]].items():
            if p:
                di, dj = dirtod(d)
                ni, nj = i + di, j + dj
                if pi != ni or pj != nj:
                    n = mp[ni][nj]
                    if possible_connections[n][opposite(d)]:
                        # this is the next node
                        pi, pj = i, j
                        i, j = ni, nj
                        track[i][j] = n
                        if i == si and j == sj:

                            for i, row in enumerate(track):
                                outside = True
                                for j, cell in enumerate(row):
                                    if cell == '.':
                                        if outside:
                                            row[j] = 'o'
                                        else:
                                            row[j] = 'i'
                                            inside_count += 1
                                    elif cell in set(['┐', '│', '┌']):
                                        outside = not outside

                            print('\n'.join([''.join(s) for s in track]))
                            return inside_count
                        break


run_test(solve, ['''.....
.S-7.
.|.|.
.L-J.
.....'''], 4)

run_test(solve, ['''..F7.
.FJ|.
SJ.L7
|F--J
LJ...'''], 8)

run_test(solve, ['''...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........'''], 23)

run_test(solve2, ['''...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........'''], 4)

run_test(solve, ['''.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...'''], 70)

run_test(solve, ['''FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L'''], 80)

small_vector = '''7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ'''
large_vector = '''FL7L-F7FJF-7FFF7FF|-F-F|JF--|.|-J-7.F--FJF|-7.F.-FF7.-F7-L-|FF-F-|-7.-F7-FF-|7J-J.F-J7.FF7..L7F|7F-7JF-L7F.|--FL7F---|.FFF-L7FL--L777L-.FF7F
7FFJ.FLJF-.FJ||F-FJJJJ||F|-F7FLJ.7-F7J||-FFF7.L7-FJL7.F|||-J7JJ.LL77F|LF7LJJ||L7--|-7F-F|F-7JLJ.LJL--F-|LLJ|7J|L|-|7|FF|7|J.LJFFJ7.|-J.F.|L|
L-77.L77JF-JF7.||||.F7FFF7-|-7L.L--|.FF.|F-JL77.|L-7|F7|-|7F|-.-7L-F7--JJ|.||L7L-.|JF|.|JL-77F-|J-L|JL--FLJLJ7JF|7||7.FJL|7--L|---7|.|FF-J-|
LF7--FFJFLJLFL|J|.77---J-F-|F7-7.|7.L|J--L--7L7F7F7|LJL7-77-L.--J7LL-7.|LF-J--.F-J7-F--L7|-F7LFJ--77-7.77LJJ.7FL.J-JFJJ|F|J|LF|7||F|7FFJL|LJ
L|J7.-JJ-.|F|FJJJL||FL77LJ.|FJ7|FL7F.L7JJFLFJFJ|LJLJF--J-F7...FF||.FJL.-7L|.FL7JJLL-JJ.|||F||.L7|JFJ.|FJ7|--7JJ-|7LLF-FJ-F.--FJF|-LJFLJ-J.FJ
FJF-L-|.LF-F||J-7.-7|FF7-77J-7|LLJ|JJLJ--7-L7|JL-7F-JF-7.||7F-JJF7.J7.||L.--JJ.---77L7--777||7FLJFJJ-|7||F-L|-J7LJ-FJL|J.|.F77.L|F|JFJ|7.FF7
|-FJ.-F7.F..L|LF|7---LL77|L7FJJ.L.|LF-JFF|-FJ|F--JL-7|FJFJ|-7JLL||F7FL.JLLJ..F.L--LF7L.LF-7|L77J.FL7.FFLF--FF.L|7|.J|FJFL|-|7-7|F|7-J..777|F
F77.F|L77LFF-|LJ-L7|-LJ|F|.--7|.L--F-|7-L7.L7|L--7F-J|L-JFJFJJ-|JFF-7---FJ..-77||7.F7||-L7LJFJ77F7JLFF7L|7|||L7||7-J-|7-.|.L|.LJ.|LJJ.FLL-L7
|.|--F-J-7L7-FF|---7-|.J7JF.LFL-J.||LF-J.F--J|LF-JL7FJF7FJ77|F7--FL7|-L7-77F7F---7-||F7F7L-7|JLF77-L|||F-7-|JLJJLL7FF...JL-J.77|FJ.|.77|L-|J
-F7FLJ|LF7.|.L-LJ.LJ..F|..F.L-|.F-J77|F-7L--7L7L--7LJFJ|L7F777J|.F-JL7LJ---L7L--7|FJ||||L7FJL7.|L7-F7|||FJ7L|J.L|LJ7JF77L.|FLJ7-7FF7|77|.F-7
J.-77LF7||F77FJ-7.|L7F-7-.F7.|F7JJ-F7J7LF7F7L7L7F7|F7L7L-J||F7-JFL7F7|--7L|LF---J||FJ||L7|L7FJF|FJF|LJLJL-7L7|F7|FLL7LLJ77LJ7|.FJ-J||L7J.JF-
|.LL-.LLL-|L-7|---L-7.LL.FL7.FJ||.F-7|F7||||JL7|||||L-JFF-J|||.F7FJ|LJ7F7-JLL7F-7|||FJL7|L7|L--JL-7L-7F---JF|7LF-LJFL-J-LLJF---FJ.F|LJJ.JJLJ
L||L|7.L7LL77LJ.F|J7|7||7|7J|.|--FL7L-JLJ|||F7|||LJ|F7F7L7FJ||FJ|L7L7F7|L7J-FLJFJLJLJF-J|FJ|F--7F-JF-JL--7L--L7JFJ.L|L|FL7.JJ-||J-7-|JFJ.FF|
|JF7LL-.|7-|77.-F|LF--FJ-JF7F77FFLJL----7LJLJLJ|L7FJ||||FJL7|LJFJ-|FJ|||FJ|--LFJF---7|F7|L7|L7-LJF7|F--7FJ.JJ7F7|.J-J7-7-F-|..FJF-.J.LJJ-F7.
F7.|-|.FF7L|.L7||..|.|.JFF|LJ|F7J-F-7F7JL-----7L-JL-J||||F-JL-7L7FJ|FJ|||F77.LL-JF--JLJLJFJL7L-7-||LJF7||F7|.F||77|.|L7L-L.F-F-LLJ7.FF-|.L--
L7FF-FF-LJ.7-FJJ|JFL-L7FJLL-7|||F7L7LJL-7F77F7L--7F--J||||F7F7L7||FJ|FJ|||||F7F77L---7F--JF7|F-JFJ|F7|||LJL77F||F7J--.|F|LF|.L-.|FF--J7LF-||
.J-J.|JLF|F|7F|.JLJ|.F-7|FF-J||LJ|JL-7F7LJ|FJ|F--JL7|FJ||||||L7|LJ|FJ|FJ||L7|LJL-7F7FJL7JFJLJL-7|FJ|||||F--JF7||||JFL-J-J.-7-|F-|-|7L-F.J--J
FJL-7|FF-FFL--7-LFJ7-J.---|F7LJF-JF-7LJL-7|L7LJF7F7L7L7|||||L7|L7FJL7||FJ|FJL---7LJ|L-7L7L---7FJ||FJ||||L-7FJ||||L7F7LF|.|-LL|-||-LFF-JF.F|7
|7LF77-J-L-.|L||.L7|-|F|-LLJL-7L77L7|F-7L|||L-7|||L7L-J||||L-JL-JL-7|||L7|L-7LF7L-7L--JFJF7|FJL7|||FJ|||F-JL7||||FJ|L--777J.F---J7L|J7-7-FJ7
LFFL|J|..F.FJ|F-7.LJFF|7.LF7F7|FJF7|||FJFJL--7LJLJ.|F--J|||F--7F7F7||LJFJ|F-JFJ|F7|F--7L7|L-JF-J|||L7||||.F7|||LJL-JF--J7.|FJ.FL7L-7-77||J.J
|F7-JFJ-FLFJ.FJL-7J--LJ|FF|LJLJL7|LJ||L7L---7|.F7-FJL7F7|||L7FJ|LJLJL-7|-||F7L7|||LJF7L7|L--7|F7||L7||||L7|||||F---7|F7F-777.77L|J7L-J-FF--J
LJ|7.FJ.|.F7F|.77|J.F|J|--|F---7LJF-J|FJ7F7FJ|FJ|FJF7LJ||||FJL7|F7|F7FJL7|LJ|FJ||L--JL-JL7F7|||||L-JLJLJFJ||||||LF7LJ|LJFJL7-7JL|LFJF|LFJ7|7
F-|JF|JFLJJ-77.L|J|F|-F7FFLJF7LL-7L7J|L7FJ|L7|L7|L-J|F7||LJL77LJ||FJ|L7FJ|F-JL7|L-------7LJLJLJLJF------JF|LJLJL-J|F7|F7L-7JF|7.7JF-FJ||F-JL
F-J7L.F|J7.|L-7F-J-7JFJ|F7F-J|F-7L7L7|FJL7L-JL7||F--J|LJL7F7L-7F|||FJFJL7|L7F7||F-7F-7F7L---7F---JF7F-7F-7|F--7F--J||||L--J|FJF-7-J-|JLJJ-7J
L7L-7.J7--.|--77F7FL-L7|||L-7LJFJ|L7LJ|JJL---7|||L--7L7F7||L--JFJ|||JL-7LJFJ|LJ|L7|L7|||F-7-|L---7||L7||FJ||F7LJFF7||||F--7FJ-|FJ|J.|.L|J.|7
L-JF--FFJ.F|7FLLJJ|JLF|LJ|F7L-7|F-7L-7L7F7F7FJ||L7-FJFJ|LJL--7F|FJ|L7|FJF-J.L-7L7|L-JLJ||FJFJF---J||FJLJL7|LJL7F7|||||||F-J--||L-7LL77.F--FJ
-JJ|J.|J7-F-JJL||-JF-7L7FJ|L7FJ||FJF7|FJ||||L7LJFJFJFJFJF---7|FJL7|FJFJFJF7FF7L7|L--7F7LJL7L7L-7F-J|L7F7FJ|F--J|||||LJLJ|F7J.FJF-JF||7LL-LJ|
....-.|F|.LJ.FFFF7.|--FJL7|FJL7LJL7||||FJ|||7L-7L7L7|F|FJF-7LJL-7|||FJFJFJL7||FJ|F-7LJL--7|FJF-JL-7L7LJ||FJL-7FJ||||F7F-J||.FJFJJ-7L-J||.|L-
-F77LFJFJ-7|F|LFJ|-F7.L-7|||F7L--7LJ|||L7LJL7F7L7L7|L7|L7L7L77F7||||L7L7L7FJ|||FJ|FJF7F7FJLJFJ7F7|L7|F7||L7F-J|FJ|LJ|LJF7|L7|FJ7FF77J|FFF.|.
|LL-F|.FJ-7L|J-L7|J||F--J||||L7F7L-7||||L-7FJ|L-JFJ|FJ|FJ.|FJFJ||LJL-JFJFJL-J||L7|L7|LJ|L-7FJ.FJL7FJ||||L7||F-JL-JF7L7-|||FJ||L|||L7LJ-7J77-
JJL7FL.L..|.7FF7||FJ|L7F7|||L7||L7FJ||L7F-JL7L--7|FJL-JL-7||FJFJL-7F--JFL-7F-J|FJL7|L-7L7-|L-7L-7|L7||||FJ|||F--7FJL-JFJ|||FJL--7JJLFL-JL-..
..FLJL|L|J|-JFJLJ|L7|JLJ|||||||L7|L7|L7|L--7L-7FJ||F7F---J|||FJF77|L7F7F7FJL7-|L7FJ|F7L7L-JF-JF-JL7||||||FJLJL-7LJF7F7L7||LJF---JF-JL||.F|L.
F-L|7.-7|LJLFL--7L-JL7F7|LJ|FJ|FJ|FJL7||-F-JF-JL7|||LJF7F-J||L7||FJFJ||||L-7L7|FJ|FJ||FL--7|F7|F7FJ||||||L7F---JF-JLJL7|||F-J7LJJL77FLF.LLL|
.|-|-7L--L.FFF--JF--7|||L-7|L7|L7|L-7LJL7L-7L7F7|LJ|F7||L-7||FJ|||FJL||||F-JFJ|L7|L7||F7F7|LJ|||||FJ||||L-JL--7|L7F---J|LJL--7-JL|-FF..7L|L|
-LFJ.7|L-..FFL---JF-J|||F-JL7|L7||F7L7F-JF7|FJ||L7FJ||||F7||||-||||F7||||L7FJJL7||FJ||||||L7FJLJ||L7||||F-----JF7||F7F-JF7F-7|77FFF-77-L-7-7
L||LJJ7.L-7JJF----JF7LJ||F7FJL7||LJL-JL7FJ||L7|L7||FJLJ||||||L7|||||LJ||L7|L7F7||||FJ|||||FJL-7FJL7|||LJL-----7|||||||F-JLJ.LJF7F7|FJ7JFL|F|
.LJ|7|F-JJ||-L-----JL7FJLJ|||FJ|L----7-||FJL7|L7|||L-7FJ|LJ|L7|||||L7||L7|L7||LJ||||F||LJ||F7FJ|F7||||F------7||||||LJL-7F7F77|||||L77||FFLJ
F7-|J-7|J.F7.L-F-----J|F7FJL-JFJ|F7F7L7|||F7||FJLJL7FJL7|F7|FJ|||||FJFJFJ|FJ||-FJ|||FJL-7|LJ||FJ|LJ||||F---7LLJ|||||F---J||||FJLJ|L7|F7|LFJ.
FJF|JJLL--JF7LFJF7F7F7LJLJF7F7L--JLJL7|||LJLJLJF---JL7J|LJ|LJFJ|||LJFJFJFJL7|L7|FJ||L7F7||F7||L7|F7|LJLJF--JF-7|LJLJL-7F7|||||F--JFJLJ|-JL7F
.F-J|F.L-LFJL7L-JLJLJL---7|||L7F-7F-7LJ|L-----7L7F7F7|FJF7L-7L-J|L-7L7|FJF7||FJ||FJ|FJ|||||LJ|FJLJLJFF-7L7F7L7LJF-7F--J|LJLJLJL7F7|F--JF7-F7
F|LFF.7.7|L-7|LF--7F7F7F-J|LJFJ|FJ|FJF7L----7FJFJ|LJ||L7||F-JF--JF7L7|||FJ|||L7LJ|FJL-J|||L7FJ|F----7L7|FLJL7|F-J|LJF7FL7F-----J|LJL7F77F7--
-J-JJ7|7LJJL|L7L-7LJLJLJF7L7FJFJL-JL-JL----7LJJ|FJF-J|-|||L-7L-7FJ|FJ||||FJ|L7|F-JL---7|||FJL7|L7F-7L-JL---7LJL-----JL7FJL------JF--J|L-J|7|
|J..LJF|FJLFJFJF7L---7F-J|FJL7|F-----7F-7F7L--7||FJF7|FJ||F-J7FJ|FJL7||LJ|FJFJ|L7F7F7FJLJ|L7FJL7||FJF7F--7.L---7F7F7F-J|F-----7F-JF7FJF--JF7
|-FF.FLJJ|-L7L-JL-7F7LJF-J|F7LJ|F7F7.LJLLJ|F--J||L-JLJL7|LJ-F-JFJL7FJ|L-7LJFJFJJ||||LJF-7|FJL7FJLJL7|LJF-JF-7F7LJ||LJF7||-F--7LJF7||L7L--7||
-7FJ-J.|L77.L----7||L--JF-J||F7LJLJL----7FJL--7|L7F--7F|L--7L-7|F-JL7|F7L7.L7L-7LJ|L-7L7LJL-7|L7F-7LJ7FJF7L7||L-7LJF-JLJL-JF7L7||||L-JF-7LJ|
FLJJL7--F--------J|L----JF-JLJ|-F-----7FJL7F7FJL-JL-7L-JF--JF-J||F7FJ||L-JF7|F-JF-JF-JFJF7F-J|FJL7L--7L-JL-JLJF-JF7L7F----7|L7L-JLJF7FJFJF-J
FL-...|.L7F7F7F7F7|F-----JF7F7L7L--7F7||F7LJ|L--7F--JF-7L-7FJF7|||||FJ|7F7|LJL77L-7L7FJFJ|L-7||F7|F-7|F7F-----JF-JL-JL---7LJFJF7F7FJLJFJFJ||
|-FFF-7-LLJLJLJLJ||L------J||L7L7F7LJ||LJ|F7L7F7||F7FJFJF7|L7|||||||L7|FJLJF-7L--7|FJL7|JL7FJ||||LJFJ|||L------JF--7F7F-7L-7|FJLJ|L--7L7L7F|
J-|-J|.LJ7|LL|F--JL-------7LJ-L7LJL--JL--J|L7LJLJ||||FJFJ||FJ|||||||FJ|L7F7L7|F--J||F7||F-J|FJ|||F7L7|||FF--7F-7L-7LJLJLL7FJ||F--JF-7L7L-J-7
|-J|FFL---J-F-JF---------7|F--7L7F-7F7|F--JFJF-7-LJLJ|FJLLJ|FJ||||LJL7|L||L7||L--7LJ|LJ|L7FJ|FJ|LJL-JLJL-JF7LJL|F7L-----7|L7||L7F7L7L7L-7JL-
.LJF7LL-J7||L-7|-F-------J|L-7|JLJFLJL-JF-7L-JFJF7F--JL---7||FJ||||F7||FJ|FJ|L7F-JF-JF7L7||FJ|.L7F7F------JL--7LJL---7F-J|FJLJ-LJ|FJ7L-7|7LL
|7JFL77.||-J.L||FJF------7|F-J|F-------7L7|F--JFJLJF-7F7F-JLJL7||L7||||L7||FJFJ|F-JF7||FJLJL-JF-J|LJF---7F-7F7L-7F--7LJF-JL7F7FF7|L--7.LJJ7|
|J-LL.7--||J-FLJL-JF----7||L-7|L----7F7|FJ|L7F7L7F7|7|||L--7F-J||FJ||LJFJ||L7L-JL--J|||L7F7F-7L-7|F-JF-7LJ.LJL-7LJF7|F7L-7FJ||FJLJF7FJF|LFL-
LFF7J-LJFJJ-F7F77F7L---7LJL--JL-7F7FJ||LJFL7LJL7LJ|L7||L7F-JL-7||L-JL7FJFJL7L7F-----J||FJ|LJFJF7LJL-7|FJF77F--7L7FJLJ|L-7LJFJ|L7F7|LJ7FJ.7J7
||LJJ7J7||L-|LJL-J|F7F7L---7F7F7LJLJ||L--7-L7F-J.FJFJ|L7|L7JF7||L7F7FJ|FJ|FJFJ|F7F-7FJ|L7|F7L-JL7F--J|L-JL-JF-J||L---JF-JF7|FJ7LJ|L-7-|JF|FJ
F|-JFFFFJ7|.L----7||LJL--7LLJLJL-7F--JF--JF7LJF-7|FJFJFJ|FJFJLJ|F||LJFJ|F7L7L7||LJJLJ|L-JLJL-7F7LJF7FJ7F--7FJ.F7|F7F-7|JFJ|||F--7|F7L7--J.|J
LLJFJ--L-J-FJF7F-JLJF7F-7L7F-----J|F--JFF-JL--JFJLJJL-J.|L7L7F-JFJL-7L7LJ|F|FJ||.F7-F77F7F7F7LJ|F7|LJF7L-7|L--J|LJ||FJL7|FJ|LJF-J||L7|JJ|-J|
LL7LJ|L-7|||FJLJF---JLJ-L7LJF7F7F7|L---7|F--7F-JF-7F7F-7|FJ-LJF-JF7FJFJF7|FJ||||FJL-JL-JLJ|||F7LJLJF7|L--JL---7L-7|||F7LJL-JF7L-7LJL||-F|L-7
FL7JL7---7F-JF--JF77F7F--JF7|LJLJLJF7F7LJL7LLJF7L7||||FJLJF7F7L-7|||FL7|LJL7L7||L7F7F7F7F7LJLJL7F--JLJF-----7|L--JLJLJL7F7F-JL--JJ|JLJ-FL-L7
77LF-FF-L-L--JF--JL-JLJF7FJLJF7F7F-JLJL---JF7FJ|FJLJLJL-77|||L--J||L-7|L-7FJFJLJFJ|||LJ|||F-7F7LJF----JF7F-7L--------7F|||L------7JJFLF7|JLF
|L-77.J.L7JF-7L-----7F-JLJF7FJLJLJF--7F-7F7|||FJL--7F-7FJFJ|L--7FJ|F7|L--JL7|J|.|FJ||F-J||L7LJ|F7|F----JLJJL-----7F--JFJ||F-----7|.FFFFJ|J-F
LJL|77-FFF7L7|F7F7F7|L7F--JLJF--7FJF-J|FJ|LJLJ|LF-7|L7LJL|FJLF-J|FJ||L7J7F-J|F-7LJ-LJL--JL-JF7|||||F--7F--------7|L--7L7||L----7LJ.LL.JFJ-FJ
L|--.|F-FJL-JLJLJ|||L7|L-7F7FJF-JL7L--JL-JF7F7L7L7||FJF-7||.FJF7|L7|L-J|FL-7||FJF----7F-----J|LJLJLJF7||F-------JL-7FJJLJL7F7F-JL|-FFJ.|J.F7
-|J-7|J-L-7F7F7F7LJL7LJF7LJLJ.L---JF-7F---JLJL7|FJLJL7L7||L7|FJ|L7||JFFF..FJLJ|JL---7|L-----7L-7F7F7||LJL---------7|L---7J|||L-7F7|FFJ7J.-FL
|L77L|.7FLLJ||||L7F-JF7|L---7FF7JF-JFLJF7F---7LJ|F--7|FJLJFJLJ.L7|||J|7LF-L7F7|J.LLFJ|F7F7F7L-7LJLJLJL----7F------J|F7F7L7|||F7LJ|7L-JL-7|||
JJ||.LF|7.F7LJLJFJL-7||L7F7FJFJL-JF7F7FJLJF--JF7|L-7LJ|F7FJF7F-7||LJ-JLF--LLJLJ77-FL7||LJ|||F7|F----7F---7|L------7LJLJ|FJ||LJ|F7|J7L7-L.FFL
LFJFF---F-J|J.F7L--7|||-LJ||FJF---JLJLJF-7|JF-JLJF-JF-J|LJFJLJFJ||J|L--7.|7|.FLJ--|F|LJF7LJLJ|LJF--7LJF--JL--7F7F7L--7LLJFJL7JLJLJ77LJ7L-F|.
L77LL7||L-7L7FJL---JLJL---JLJFJF--7F7F-JFJL-JF7F-JF7|F-JF7|F--JLLJF-77.L.7-.L7LLJ-F7L--JL-7F7|F7L-7L-7L-----7LJLJL7F7L--7L--JF777|.J77F-FFF7
FJF7LL--L-L7LJF7F-----7F7F7F7|JL-7LJ|L-7|F7F7||L--JLJL7-|LJL---7LJ7L|77.F|JFLJ7-FFJ|F7-F--J||LJL-7L7FJ-F7F-7L-7F-7||L--7|F7F7|L--7JF7JL7FLJF
|-7J7FLF77LL7FJLJF----J|LJ||||F--JF7L--JLJ||||L7F--7F7L7|F----7L7FJJLL7-FF.7.|7FLL7LJL7L---JL---7L-JL-7|LJ-L-7LJFJ|L7F7LJ|||||F--J||JJJLFJ7|
7F|FLJ7FF7F-J||F-JF-7F7L7LLJLJL--7|L-----7|||L7|L-7LJL7LJL---7L7L77F77|7F-FJ7|F|.LL--7L-7|F-----JF7F-7LJF7LF7L--J-L-J||F7||||||J||-FJ7.F|-J.
--JFJFLF|LJF7|FJF7L7LJL-JF7F7F7F7||F--7F7|LJL-J|F-J-F-JF-7F-7L7L7|-L77|LF.|--JLJFJJF-JF7L7L---7F-J|L7L7FJL-JL7F---7F-JLJLJLJLJL7F7F77-|-|J.|
L|--.|.FJF-JLJL-JL-JJF7-FJLJLJLJ|LJL-7LJLJF7F-7|L--7|F7|-|L7L-JLLJ-JF--J|F-7JFLF7JFL--JL7L-7F7LJF7L-J-LJF----J|F-7|L7F---7F7F-7LJLJL7.LF7.F|
.7FJ.J.L-J|-F-----77FJL7L----7F7L-7F7L--7L|||FJL--7|||||FJFJJ.F77L|JJ.|FLJFLF7.JJF------JF7LJL-7||.F7FF7L-----JL7LJFJL--7LJLJ|L7F-7FJ7F7JFJ.
F-JFJJF|-L|.L--7F7|FJF7L-7|F-J||F7LJL--7L7|||L7F77LJ||||L-J.F-JL7L|-.7JLL-JJ.J7||L--7F7F7|L7F-7LJL-JL-JL-------7L--JF7F7|F7LF7|LJ7LJF-J|-|J7
|7L|F|-|.LLFF-7LJ||L-J|F7L7|F7|LJL----7L-J||L7LJL--7||||F7F7L-7FJF7J-|7.L---..F7LJLFJ|LJ||FJ|FJF--7F----------7L--7FJLJ|||L7|L7F7F7FJF-J7LF|
7J-FJ7.J7LLFL7L--JL---J|L7LJ|||F------JJF-JL-JF7F--JLJLJ|LJL7-|||||F-|-F7F7-77FLJLLL7|F7||L7|L7|F-J|F--------7L7F7|L--7LJ|FJL7LJLJ||FJJFJ7|7
L-F7JJ7.7-FFJL7F-7F7F7FJ|L7FJLJL-7F--7FFJF7F--J||F7F7-F7|F--JFJL-J|7J|F777JF-77JJFLLLJ||LJ-LJ7LJL--JL----7F-7L-J||L---JF7||F7|F---J|L77|J|L|
||||L-J|LF-|-LLJ7LJLJ|L--7LJF7F7FLJF7L7L7|LJF7.LJ|LJL-JLJL7F7|F7F7L-7-LF7FF7|F77FJ.||FJL-----7FF--7LF----J|FJF--J|F7F--JLJLJLJL----JFJFL.JJ|
J-|F-L-F7L-|FF7F7F---JF--JF7||||F7FJL7L-JL--JL--7|F7F----7|||||LJ|F-JFL|L7||FJL7LJFF7L-----7FJFJF7L7L-----JL-JF-7||LJF--7F7F7F--7F-7|F7--.F.
.LLJLLFJ-J-FFJLJLJF-7FJLF-J|||||||L-7L--7F7F7F-7LJ|LJF--7LJ|LJL-7LJF77JL7||||F-J7JFJL-7F---JL7L-JL7|FF7LF----7L7|LJF7L-7|||||L-7LJ7LJ-|7..F7
|.|7F-JJ.J--L7F7F-JFJ|F-JF7LJLJLJ|F-JF7LLJLJ||JL--JF7L7FJF7|F---J.FJ|F77|LJ|||JF7JL--7|L7F7F7L----JL-JL7L---7L7||F7|L7FJLJ|||F7|F--77|L--7L.
L-JL|7777FF||LJLJF7L7||F7|L-----7|L--J|F---7|L-----JL-JL7|LJL-7F7FL7||L7|F7|||FJL7F--JL7LJLJL7F7F-7F7F7L----JJLJLJ|L7|L-7FJ||||||F-J7JF-F-77
FJFLJL|7-L-F-----JL7LJLJ||F-----JL----J|F--JL--7F--7F7F7LJF-7FJ||F-J||FJLJ|||LJF7|L--7FJF---7LJLJFJ||||F-7F7.F---7|FJL--JL-JLJLJ||F7J.FL--77
J7|7|JLJ7JLL------7L7F77LJL----7F------JL----7F||F7LJLJL7FJ|LJFJ|L-7|||F7FJ||F-JLJ7F7|L7L--7|-F--JFJLJLJFLJL7|F--J|L---7F7F7F7|FJLJL-7JJ-F||
FF|-L.|7L7|L7|FF7L|FJ||F7F-7F-7||F---7F----7FJFJLJL----7|L-7F7|FJF7||||||L7||L7F7F7||L7L7F7|L-JF-7|F--7F7F7FJ||F7||F---J|||LJL-JF7F7FJJ.-F77
F7F-L7L-7JF--LFJL-JL-J|||L7|L7|LJL--7|L---7|L7|F7F7F7F-JL--J|LJ|FJ||LJ|||FJ|L7||LJ||L7L7LJ|L--7|FJ|L-7||LJLJJ|||L7LJF-7FJLJF7F7FJ||LJJF|.L|7
J7L77F|L|.JJF|L------7|||FJ|FJL-----JL---7|L-J||||||LJF7|F-7|F-JL7|L7FJ|LJFJ.|LJF-JL7|7L-7L7F7LJL-JF-JLJF7|F-JLJFJF7|FJL7F-JLJLJLLJJ..FJL.L7
L|.LLJF-JF|7FF--7F7F7||||L7|L7F7F-------7|L--7||||LJF7|L7|FJ||F-7|L-JL7L-7|F7L-7|-F-J|F7FJFJ|L7F--7L--7FJL-JF7F7L7|LJL7FJL-----7|LF-7-|7|.7|
7||7LLLJ-FJF7L-7LJLJLJLJL-JL7LJLJF------JL---JLJLJF7|||FJ|||||L7|L---7L77|LJL7FJL-JF7||LJFJFL7||F-JF--J|F---J|||FJ|F--J|F--7F-7|F7|FJ7|FF|LJ
L-L7.|.7.FFJ|F7L-----7F--7F7L7LF7L---------7F-7-F7|||||L7|L7||FJ|F7F7L7L-JF--JL-7F-JLJL-7|F7FJ|||F7L---JL7FF7LJLJF|L---J|LFJL7LJ|LJL7FF7L7-7
|.FF-7-FFFL7LJL----7LLJF-J|L7L-JL7F----7F--J|FJFJ||||||FJL7||||FJ||||JL--7L7F7F-JL7F7F7F|LJ|L7LJ|||F7F7F7L-JL-----JF7F-7L7L-7L--JF-7L-JL7J-J
77|L7L.||LFJF--7F-7L-7FJF7L7L7F7FJL---7|L---JL7L7|||||||F7|||||L7|||L-7F7|FJ||L7F7|||||FJF7L7|F7LJLJLJ|||F-7F7F7F-7||L7L7L-7L----JFJF--7|J-7
--L-JF|LJ.L7|J7LJFJF7LJFJ|FJ-LJ|L-----JL------JFJ|||||||||||||L7LJ||F-J|||L7|L7LJ|||||||FJL-JLJL-----7|||L7|||||L7LJL-J7L--JF----7L7L7.LJJF7
|-J-J-F-J7JLJFF7-L-J|F-JFLJF7F-JF7F--------7F-7L7||LJ||LJLJ|||7L-7|||F7|LJFJ|FJFFJLJ||LJ|F77F---7F7LFJLJ|FJLJ||L7L---------7|F---JJL-J77L7F7
F7.FL7J.FF-LLFJ|F7F-JL7F---J|L--JLJF-----7FJ|FJFJ||F7||F---J|L-77||||||L-7S7||F7|F-7||F-J|L7L--7|||FJF-7LJF7-LJFJF7F7F--7F7LJL--7-FL-|.7F|JL
L|7F7|.F|LF7FL7|||L-7FJL-7F7L-7F--7L7F--7LJFJ|LL7|LJ|||L---7L-7|FJLJ|||F-JFJ|LJ|LJ-|LJ|F7L7|F-7||||L-J||F7||F7.L-JLJ|L-7|||F7F-7L7L|---L7|.|
F-J|J.FFF-J|F-J||L--JL--7LJL-7|L-7L-J|F-JF7L7L7FJL-7|LJF---JF7||L-7FJ||L-7|J|F7L7F7|F7LJL-J|L7||LJL--7FJ|LJLJL7F7F7JL--JLJLJ|L7L-JL--|.LF77.
-JJL.FLLL-7|L-7LJF---7F7|7F7FJ|F7L---JL--JL7|FJL7F-JL-7|FF7F|LJ|F7||FJL7FJL7LJL7|||LJL-7F--JFJ|L--7F-JL-JF-7F7LJ|||F-------7L7L--77.FF-F.L77
FLFJ-J.LLFJL--JF7|F--J|||FJ|L7|||F---------J|L-7|L7-F7|L7|L7L7FJ|LJ|L-7|L7FJF-7|LJL7F--J|F7FJFJF--J|F7F--JJLJ|F-J|LJF---7F7L7|F7FJ-L-J|.F.L7
|-7J.J...L-7F7FJ|||F7FJLJL7L-JLJ|L------7F7-|F-JL7L7|||FJ|FJFJL7L7FJ|FJL7|L7|FJL7F-JL-7FJ||L7||L--7|||L-----7LJF7|F-JF7-LJL-J|||||.L|FJ7L-7|
|FJ..|-7FLLLJLJ.LJLJLJF-7-L7F7F7L---7F--J||FJ|F7FJFJ|||L7||FJF-J7||F7L-7LJFJ||F7|L-7F7||FJL7||F7F-JLJ|7F7F-7L-7|||L--JL-----7LJ|L-7-LF-L..77
F-JJ-|.FFF--7F-7JF---7L7|F7||LJL-7F7LJLF7|||FJ||L7L7|||FJ||L7|JF7||||F7|F-JJ||||L-7|||||L7FJ||||L--7FJFJ|L7|F7LJLJF-----7F--JF7L--J7.J-|7..|
7JJ-7J7FFJF7|L7|FJF-7L-JLJLJ|F--7LJ|F--J||LJL7||LL7|||||FJ|FJ|FJ||||||||L-7FJ|||F7|||||L7|L7|LJ|F7FJ|-L7L-JLJL---7L7F--7LJF7FJL-7JJL7.L7J7-L
LF-FF---JFJ|L7||L-J-L-----7FJ|F7L--J|F--JL7F-J||F7||||||L7|L7|L7||||||||F-JL7||||||||||FJ|FJ|F-J||L7|F7L--7-F--7LL-J|F-JJ-|||F--J7||77LJ||7|
7|FFL7F7FJ.L7LJL-7F7JF77F-J|JLJL7F-7||F7F7|L7FJ||||||LJ|FJL7|L7||||||||||F-7||||||||||||FJL7|L7FJ|FJ||L7F7L7|F-JF---JL-7FFJ|||F-7J-.FJ-LJ7-J
L-7--LJLJF--JF7F7LJL-JL-JF7|F---J|FJ|||||||FJL7LJ|||L-7||F7|L7||||||||||||FJ|||||||||||LJF-JL7||FJ|FJ|-||L7LJL--JF--7F7L7|FJ|LJFJ.L-J--F|L|.
.|||7.||-L---J||L7F7F-7F7|||L-7F7|L7|||||||L7FJF7||L7FJLJ|LJFJ||LJLJ||||||L7|LJ||||||||F7L---JLJL7|L7|FJL7L7F7F--JF7||L7LJL-JF-JJJF|JFF.J-FF
|J|-7F|FF--7F7||.LJLJFJ|||LJF-J|||FJ||||||L7|L7|LJL7||F--JF-JFJL7LF7LJ||||.|L-7||LJLJ|LJL--7F---7||F|||F7|FJ||L7|FJ|||FJF-7F7L--7JJLL|JL-F|J
|FJ||7LFJF7LJ|LJF7-F7L7|LJF-JF7|||L7|||LJL7|L7|L7F-JLJL-7FJJFJF7L7||F-J|||FJF-JLJLF7FJF-7F7LJF-7|||FJ|||||L7|L7L-JFJLJL7|F||L---JJ|..|-|FL77
F--|L-JL-J|F7L--JL-JL-JL7FJF7|LJ|L7||LJF--JL7||FJL---7F7||F-JFJL7LJ|L7FJLJL7|.F77FJLJFJ-||L-7L7LJ||L7|||||L||FL---JJF77|L7|L7F7JF7J---7F7|L7
FJJLJ.FF7|LJL------7F7F-J|FJ||F-JFJ||F-JF7F7|||L7F7F7||LJ||F7L-7|F7|FJ|F---JL7|L7|F7FJF-JL-7|FJF7LJFJ|LJLJFJL-------JL7L7|L7LJL-J||JL|-LJ-LF
-JFL.F7|L--7F------J||L-7LJ|LJL7FJ-LJ|F7|LJLJ|L7||||||L-7|||L7FJLJLJL-JL--7F7LJFJLJ|L7|F7F7||L-JL7.|FJF---JF7F----7F-7L7LJFJF7F--J77-|||7..|
|L|LFJ|L--7|L---7F-7||F7|F---7FJL7F7FJ||L7F--JFJLJ||||F-J||L7|L----7F-----J||F7|F--JFJLJ||LJL7F-7L7|L7|F7F7||L---7LJ7L7L-7L-J||F|.F77.-L-7F-
L7-FL7L---JL----J|FJ||||||F-7LJF-J|LJFJ|FJL-7FJF7LLJ|||F7|L7|L7F-7FJL--7F7FJ||||L7F7L7|FJL77FJL7L-JL-JLJLJLJL7F--JF7F7L-7L--7|L777JLF7FJLF|J
|.LJ.L----7F7F--7||FJ||||||FL-7L-7L7FJ|||F--JL-JL7F7||||||FJ|-|L7|L7F-7|||||||||FJ|L7L7|F7L7|F7L----7F7F7F---JL---JLJL7J|F7FJ|FJL-.FL.L7.|L7
-JFL.|7FLFJ|LJF-J|||FJ||||L7-FJF-J.|L-7||L--7F7F7||LJ|||LJL7L7|FJ|FJL7LJ||L7LJ||L7L7L7|LJL-JLJ|F-7F7LJLJ||F--7F7F7F7F7L7||LJL||-F.F||-L-F|-.
JF-JFL-7-L7|F-JF-JLJL7||||FJFJFJF--JF7|||F--J|LJLJL7FJLJF--JFJLJJ||F-JF7|L7L7FJL7L-JJ|L-----7FJ|FJ||F7F7|||F-J|||||LJ|FJ|L--7LJJ|---F-J7-JFF
J7.L-7.-F-J||F7L--7F7||||LJLL7|FJF7FJ|||||F-7L--7F-JL7F-JF-7L---7LJL7FJ||LL-J|F7L-7F-JF---7FJL-JL7|LJLJ||LJ|F7||||L-7LJFJF7FJ-|7L-JJ..||.LFJ
F|-FJ---|F7|LJ|F--J|LJ|||JF--J||FJ||LLJ||LJ-|F7FJL7F7|L7FJFJF7F7|-F-J|FJL7F--J|L7FJL-7L-7|LJ|.F--JL--7FJ|F-J|||||L7FJF7L-JLJ.||F-JJ.-7L|7--7
FL-F7FJFLJ||F-JL-7LL7FJLJ.L--7|||7|L-7FJ|F--J||L-7||||FJL7L7|LJLJFJF7|L7FJ|F-7L7||LF-JF7L---7FJF7F7F7|L7|L-7|||LJ-|L-JL----7-|L7-||FLJ7L|7|J
-.FL||-FJ||||F-7FJ.LLJJF|-J|LLJ||FJF7|L7||F7FJ|F-J||||L--J7|L---7L-JLJFJL7||F|FJ|L7L-7|L----JL7|LJ||LJJLJF-J||L--7L7F7F-7F-J7JF---JLJ-|7LF77
L-7JLL.-JFLJ||||L7FLL|-J.|JLF--J|L7|LJFJ||||L7|L-7||||F----JF-7FJ|F---JF-J|L7||JL-JFFJL---7F-7|L-7|L---7FL7FJL7F-JL||||FJL7.F----J|F-7J--J|7
|--.7JF77.LFJL7L-J7|F|||77|.L7F7|FJL-7L7|LJL7||F7|LJ|||F---7L7||F-JF7F7|F-JFJLJF----JF7F--J|FJL-7||F---JF-J|F-J|F-7||LJL7FJ.|LJJ|JFL-JJ77F-J
F7-7|-F7-|JL-7L7LF7-L|JJL||-LLJLJL7F7|LLJ|F-J|||LJJFJ|||F--JFJLJ|F7|LJ|||F7L--7L-7F7FJ|L---JL--7LJ||F7|FJF7||F7LJFJ||JJJ||-77J.-7F7L7.LFLJ7|
||FF|7L7-|-|-|FJ-LJ.FJJ.F7|7.|7L-|LJLJ7JF7L-7||L--7|FJLJL-7FJF7-|||L-7||||L7F-JLFJ||L7L7F7F7F-7|F-JLJL7|FJ||||L7FJ|LJ--FJL7|FJFLJF7-|7J.L7L|
L-J|..FJL7.J.LJ|-L7J77.F|J7F-77|.F7LJ|L-|L--J||F7FJ|L7F---JL-J|FJ||F7|LJ|L7|L-7F|FJL-JFJ||||L7||L7F7F7|||-||||FJL-7.LFLL7FJJ|-F.-FJ7FL.F7|.|
|J-F7-77-LJLJ|J7-7JL|FJ-||-7LLJ-JLJ|||.LL7F7FJLJ|L7L7|L-7F7F-7|L-J||LJF-JFJ|F7|FJL--7FL-J|||FJ|L7||||LJ|L7LJ||L7F-JFFJJJLJ.||LLJLL-J.LJJ-L-7
|.7---L|-|F7J|-77|--.J|F77.|.L|..|-|-LJJ-LJ|L7|FJFJJLJF-J||L7LJ|7LLJ7FJF7L7LJLJL7F--JF---J||L7L-JLJ|L-7L7L7.LJ.|L7|F77|J|J7FL7L|7LF-L-|J.7-L
F77.|F7.FJ-J.JJLJ|JL|LLL-J.FF.|F-L7J7LJ77|-L-JFJFJJLF-JF7|L7L7L|J-|FFJFJ|FJ7F-7FJL7F-JF7F7|L7L---7FJF-JFJFJFJ-LL7|J77FJ.LJLJFL-FJ.F7.L7.FL-J
FLF-|JL7||FL-JL||F..JJFJ.L.|L.F|J-F-|7L-|F-JJLL-JJLFL7FJLJFJFJ.|--J-|FJFJ|F7L7LJF-J|F7|||LJ7|F7F-JL7L7FJFJ.|7.LLLJL--FJF||L77|.|FF--7.JF-|F|
L.|-77LFFF7JL7-LJ|--7F7-L77-.7.|..JJ.L7|.LJF7J|FJ|F|LLJ7L-L7||-|-JFFLJ-L7LJ|FJF7|-FJ||||L-7FJ|||-|FL-JL7|J7LLJ.F|.||J|FLJ-|LJ.FLFJ.|FFJL7J||
.FL-J--||LF-|-F-|7|JF-JLLJJ7.LFFJ7J..FF--.FF7.L|LL||-LLJL7JLJ7FL-.FL..F-JF7|L7|LJJL7|LJL7FJ|FJ||FLLJ||-LJ.F-|L7J|F7L.LF|7-L|7FLL|J---L-L7F|J
FJJ7.|-F|7JF|LLF-L77..|7.FF7-.LF7JLFJ|L7J..FJ-J..|||77||.||L.LJJ.F|.F-L-7|LJFJ|J|7.||.F-JL7LJL|L7||F|7.L|-LF--F-7LJ.L.F.|.||-JLLJ.-.|7J|L7J7
|JJF7.L|LJ.LL77|J-|J7-J|FFLJ7.JLJL7J|7LL7.F|7-L-L-LJL7-|7L7|.|7--JFF|.LLLJJLL-J.L|-LJFJF-7L7JFL7L7LJLF7FF-77LLJJLJ.7J-L-7.L7L|7L7FLFF77|F|JL
L7FJF-7F.LFJ|JL--7|-|FL-FJ7-|.L--L|--|7F-7|JL7-JJF|-FJ.LJ.-F7|--L7LJ|7-J7-F7-L-7LJ.|L|FJFJFJ.|.L-J.|7L7|||LJ-F77FJ-J-FLJ|F-7.|7-|JL-J.7-J..|
.JJJ|JFL7F|FJ7..LL|-|7FFL-J||JFL-J.F||.L.L-77|F---J|JFJ.L7LFJJ7LJLF7|7.LF-FJ7LF|7FJ7JLJLL7|JJ--JJ7.F|-|77F||JLL-|...FJ7F|7-|F|7L|.7|F-|J.FF7
J-LF|.|7|7|L-F-77-L-.|LJL7LLF.|JJ.L--J7JJ|LJFLF777LL-J-F.|-7JFJ.|FJ|L-7F7||-|7|---J7.||J7LJ.FL.L7LL7|-|L7-J|..|7J7.7J7F.L|J|7LL-7-L-J-|7FFJJ
LF.FJF7-|-L--FL7L-7|-F.F-JL|.LF7F7L7-7JJFLLFFJ.LJ7-L|FF|F|.|7|.7J7...|LLL-F-7J.JFFF-7F.LFJJ-7.|7L7JLF7|F|J.|F7FJ...J||JJFF7LJF.FL7L-J.L-77|7
F--JJL-7J|LJLJJLF-L7---J-|.J-.JLJJLL7JL7JJ.7.L|LLJ-.L-J-7J-L7LLJ---FJ-LJJ..JLL7.L-JLLLL-7-FJLF77L---7JJLJ.LFJL--F-F-JJ.LLJ|-F7-JJ.JJ.JJF7--7'''
method = solve
run_test(method, [small_vector], 8)
run_test(method, [large_vector], 6725)

method = solve2
run_test(method, [small_vector], 1)
run_test(method, [large_vector], 383)
