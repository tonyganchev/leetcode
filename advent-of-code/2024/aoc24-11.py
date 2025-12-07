from math import floor, log10
from functools import cache

@cache
def blink(stone, times):
    if times > 300:
        print(f'  d {stone}: {times}')
    if times == 0:
        return 1
    times -= 1
    if stone == 0:
        return blink(1, times)
    else:
        m = floor(log10(stone)) + 1
        if m > 0 and m % 2 == 0:
            p = 10 ** (m // 2)
            return blink(stone // p, times) + blink(stone % p, times)
        else:
            return blink(stone * 2024, times)

def solve(input, times):
    stones = [int(s) for s in input.split(' ')]
    result = 0
    for s in stones:
        # print(f'{s}------------------------------------------')
        r = blink(s, times)
        print(f'{s}: {r}')
        result += r
    return result

def part1(input):
    return solve(input, 25)
def part2(input):
    return solve(input, 75)
# print(solve('125 17',25))
print(solve('5 127 680267 39260 0 26 3553 5851995', 75))
