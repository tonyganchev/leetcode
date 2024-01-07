from numpy import Infinity
from test_utils import run_test
from typing import List, Tuple
from math import sqrt, ceil, floor
import re

class Game:
    def __init__(self, time, best_dist):
        self.time = time
        self.best_dist = best_dist
    @classmethod
    def from_string(cls, s) -> Tuple:
        tot_time, tot_dist = s.splitlines()
        tot_time = tot_time.split(':')[1].split()
        tot_dist = tot_dist.split(':')[1].split()
        return tuple(Game(int(tot_time[i]), int(tot_dist[i])) for i in range(len(tot_time)))

def solve(data: str) -> int:
    games = Game.from_string(data)
    options = 1
    for game in games:
        lo = ceil(0.5 * (game.time - sqrt(game.time ** 2.0 - 4.0 * game.best_dist)) + 0.0000001)
        hi = floor(0.5 * (game.time + sqrt(game.time ** 2.0 - 4.0 * game.best_dist)) - 0.0000001)
        variants = hi - lo + 1
        options *= variants
    return options



def solve2(data: List[str]):
    data = data.replace(' ', '')
    games = Game.from_string(data)
    options = 1
    for game in games:
        lo = ceil(0.5 * (game.time - sqrt(game.time ** 2.0 - 4.0 * game.best_dist)) + 0.0000001)
        hi = floor(0.5 * (game.time + sqrt(game.time ** 2.0 - 4.0 * game.best_dist)) - 0.0000001)
        variants = hi - lo + 1
        options *= variants
    return options


small_vector = '''Time:      7  15   30
Distance:  9  40  200'''
large_vector = '''Time:        50     74     86     85
Distance:   242   1017   1691   1252'''
method = solve
run_test(method, [small_vector], 288)
run_test(method, [large_vector], 1731600)

method = solve2
run_test(method, [small_vector], 71503)
run_test(method, [large_vector], 40087680)
