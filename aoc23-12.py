from enum import IntEnum
from numpy import Infinity
from test_utils import run_test
from typing import List, Tuple
from math import sqrt, ceil, floor
import re
import numpy as np
from functools import cache

rcount = 0

class Chunk:
    def __init__(self, mp: str):
        self.mp = mp
        self.req = mp.find('#') >= 0
    def __repr__(self):
        return ''.join(self.mp)

@cache
def variants_single(ms: Chunk, nseq: Tuple[int]) -> int:
    global rcount
    rcount += 1
    if len(ms) < len(nseq) * 2 - 1:
        return 0
    if len(nseq) == 0:
        for c in ms:
            if c == '#':
                return 0
        return 1
    vs = 0
    for i in range(len(ms) - nseq[0] + 1):
        if (i == 0 or ms[i - 1] == '?') and (i + nseq[0] == len(ms) or ms[i + nseq[0]] == '?'):
            vs += variants_single(ms[i + nseq[0] + 1:], nseq[1:])
        if ms[i] == '#':
            break
    # print(ms, nseq, vs)
    return vs

@cache
def variants(mpseq: Tuple[Chunk], nseq: Tuple[int]) -> int:
    if len(nseq) == 0:
        for s in mpseq:
            for c in s.mp:
                if c == '#':
                    return 0
        return 1
    if len(mpseq) == 0:
        return 0
    vs = 0
    for nc in range(1 if mpseq[0].req else 0, len(nseq) + 1):
        lv = variants_single(mpseq[0].mp, nseq[:nc])
        rv = variants(mpseq[1:], nseq[nc:])
        vs += lv * rv
    # print(mpseq, nseq, vs)
    return vs


def solve_old(data: str, razdjurk: bool = False) -> int:
    tot = 0
    lines = data.splitlines()
    for line in lines:
        mp_s, seq_s = line.split()
        if razdjurk:
            mp_s = '?'.join(mp_s for _ in range(5))
            seq_s = ','.join(seq_s for _ in range(5))
        mpseq = tuple(Chunk(s) for s in mp_s.split('.') if s != '')
        nseq = tuple(int(s) for s in seq_s.split(','))
        vs = variants(mpseq, nseq)
        print(mpseq, nseq, vs, '----------')
        tot += vs

    global rcount
    print(rcount)
    rcount = 0

    return tot

solve = solve_old

# run_test(solve, ['???#?????#?.#???#??? 9,7', True], 1000)
# run_test(solve, ['.?.?..?????.?# 1,1,3,1', True], 1000)

# exit()

# run_test(solve, ['???#?????#?.#???#??? 9,7', False], 2)
# run_test(solve, ['??????????#.#?????.? 2,7,1,4,1'], 2)
# run_test(solve, ['??#??#?#?#?.?????? 9,1,1'], 20)
# run_test(solve, ['??#???#.#.?###..#? 1,1,3,1,4,1'], 1)
# run_test(solve, ['????#??#.??????? 2,4,1,1'], 30)
# run_test(solve, ['??? 1'], 3)
# run_test(solve, ['??? 2'], 2)
# run_test(solve, ['??? 3'], 1)
# run_test(solve, ['??? 1,1'], 1)
# run_test(solve, ['???.??? 1,1,1'], 6)
# run_test(solve, ['#?#?# 1'], 0)
# run_test(solve, ['.#?#???#???? 1,6'], 1)
# run_test(solve, ['.#?#???#???? 1,6,1'], 2)
# run_test(solve, ['???.???.#?#???#???? 1,1,1,1,1,6,2'], 1)
# run_test(solve, ['???.???.#?#???#???? 1,1,1,1,1,6,1'], 2)
# run_test(solve, ['???.???.#?#???#???? 1,1,1,1,6,1'], 12)
# run_test(solve, ['##.#?#?.?????#?????? 2,1,1,1,8'], 6)
# run_test(solve, ['?..#?????#?#?#????#? 1,12,1,1'], 1)
# run_test(solve, ['?????????..???#. 2,2,2,1,2'], 4)
# run_test(solve, ['?????????..???#. 2'], 1)
# run_test(solve, ['##.#?#?.?????#?????? 2,1,1,1,8'], 6)
# run_test(solve, ['##.#?#?.?????#?????? 2,1,1,1,8'], 6)
# run_test(solve, ['##.#?#?.?????#?????? 2,1,1,1,8'], 6)
# run_test(solve, ['##.#?#?.?????#?????? 2,1,1,1,8'], 6)

# run_test(solve, ['.# 1', True], 16)

small_vector = '''???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1'''

large_vector = '''???#?????#?.#???#??? 9,7
.?.?..?????.?# 1,1,3,1
??#??#?#?#?.?????? 9,1,1
????????????? 1,5,1,1
??#??#????##??. 6,3
#?#..#?#??? 3,5
???#.??.?#??? 3,1,2,1
?.?#??.??????????? 2,1,3,1
??#?#??#.#..?# 4,2,1,2
.????????..#?? 6,1
.??..?.???? 1,1,1
?.?##?#???#?#????# 1,10,1,1
??????????#.#?????.? 2,7,1,4,1
?.???..??.????#? 2,3
????.#??#???. 3,7
????#?????###?????#? 4,12
#.??#????. 1,5,1
?#???#??#.???#?.. 2,1,1,1,3
#???#????#? 7,1
??#..????#?#? 1,1,1,5
.##??#??#????????? 9,3
????#.#??#??#.. 4,1,2,1
...?.???...#?#??.??? 2,4,1
..####?.?????? 4,2
#.?.?##?#??#??#? 1,4,5
??#??#???##?.?.??#?? 11,5
????#?#?.?.#.?#???? 5,1,1,1,2,3
???.????...???#?#? 2,4,2,4
?..???....???#?? 3,4
????##??###.? 2,3,3,1
?#..????#?##?##?#?? 1,13
##?.?#????.?????..# 3,3,2,1,3,1
.???.??????? 1,1,2,1
##?##?#?.?????#? 2,5,3,2
###?#?.??#?#? 3,2,5
##?#?.?#???#??????#? 2,2,3,2,2,3
#?.#?#?.??????.?..?? 1,1,1,5,1,1
.???....#? 1,1
???.#???#?#.??. 1,3,3
#???####????..# 1,8,1,1
.?????????#? 1,2,3
#?#???##?.???? 9,2
.???...??. 2,2
??#?#????# 5,1
#??????#?###.#??? 12,1
???#..??.??#??? 1,1,1,4
????.?.?.?.??? 1,1,2
????#?#?#?#?????? 7,4,3
??#..?.#??##?..????. 1,1,1,6,2
.#?#??#?.?#????#??. 6,8
#????????##??.?? 2,1,2,4,2
?###???.??????#??.?? 6,3,4,1
?#?#????#??.? 1,1,4
###?????.?...??? 3,1,1,1,2
.??#????#.. 3,3
.?..##??#?..???? 1,3,2,2
?.?.?.?.?#?.?.. 1,1,1,3,1
?????#??#??.????.. 4,4,3
??.???..??..?.? 1,2
??#?.??#.#????#? 1,1,1,1,4
???#.???#?#??#?? 1,1,1,5,2
?###??????#??#??.# 4,1,8,1
?#.????.???? 1,1,1,1
?.?????.#.?? 2,1,1,1
?.?#?###?..#?#???.?? 6,5
???????#??? 1,3
?.??#?.?#.????#??? 1,1,1,6,1
.???.?.?.#? 1,1,1
.#????..??? 3,1,2
?###?#???????.#?#? 8,4,1,1
?????????..???#. 2,2,2,1,2
?#.????#??###???? 1,5,3,1
.?.?????#.????#?# 1,5,1,4
?#?#?#????????##???# 3,2,3,6
??????????#?.???.? 1,1,2,4,3,1
.?????????#??? 3,7,1
??###??##?? 3,4
#.?????##? 1,1,5
??????.??#.#?##??# 1,1,1,1,1,5
????...?????? 1,3
??##??#????#??#??? 7,1,5
?.??????????.? 1,1,1
?.?????#??#?? 1,7,2
?.?#?????..?? 6,1
??????###??????#?.? 8,2
?##??????.? 5,1
?.???#???.#? 4,2
??##??.?.#?#???? 4,4
.##..?????# 2,4
????#??#.??????? 2,4,1,1
..???#??.#.???#.#. 1,1,1,4,1
??????????#?????# 2,1,5,1,1
?.??????.???##??.?? 1,3,1,1,2,1
.?????##???#?? 1,7
?.????????? 2,3
?##?#??..#?#?. 6,3
.???#?????#?.??. 2,2
?###??????..?# 6,1,2
?..#?????#?#?#????#? 1,12,1,1
?#.?????.???#.#?##?? 1,1,3,2,4
???###?.?????? 1,5,5
.????.??#?#?#??? 2,1,8
???#??#???#??.? 1,9,1
.#???#?????? 5,2,1
????????????#?. 1,9,2
?.??#??.?.???#??.??? 3,4
???#?..?????####? 5,1,4
????.???#??..? 2,6
#?#.?#??##?#??# 1,1,2,4,2
.?.??.?.#?.??? 1,1,2,2
?##????#.????????##? 5,1,10
???..#??#???# 1,1,2,1
.????.?#??????? 1,1,4,1
?#???.?##?#???.??#?? 1,2,5,1,1,1
.#?..#????? 1,1,2
????#??#??.#.##??? 4,2,1,1,3,1
??.#??#..?#????#? 1,2,1,2,4
#.?.#??.#? 1,1,1
?????.??#???#?. 2,3,2
?????#??????.?? 3,3,3,2
?????????.???#?? 5,3
##????..????????? 5,2,1,1
?#???????# 2,1,1
??.?#?.?#???..#.? 1,2,5,1,1
##??.?.?##?.?? 4,3,2
.#????.????#?? 3,1,1,1
.#..?#?#??? 1,5
?#.?.??.?? 1,1,1
.?????#?.??##??? 2,1,6
??????.??????# 3,1,2,1
?.??.#?#?#??????. 7,1
?#?.#????#?????.?? 2,2,3,2,1
??#???.?##?????? 3,5
#??#?????##?#??#??.# 1,2,5,1,3,1
?????#????#?????? 10,3
.#??.?.?????#? 1,1,1,7
????.???..#?????? 2,1,7
?????#??#??????? 2,2,6,1
???.??.??#????#?. 1,2,9
#.?#?.??##???? 1,1,5,1
.?????#??. 3,2
????#???.???.??? 6,2,2
??###?#?????. 3,1,1,1
????#?.???????.?.?? 1,1,1,7,1,1
????#??.?. 4,1
.#??.??.??.? 2,1,2
.?.????#?#???# 2,5,1
????.?#???#? 1,1,7
??#.?#????##? 1,1,8
???..??#??.??##??? 1,1,1,2,5
#??#??##???#? 1,1,6
??????????? 6,1,1
??#???#?#????. 4,3,1
?..##?###?????? 1,10
.???##????#??.?##?.? 5,4,3,1
???#??.???#?.??# 5,2,2,1,1
??.???.?.?????????? 2,1,2
????.??????#?#????? 3,1,1,5,1
.????##?..#????.?.?? 5,5,1
????????#???##??#?? 8,5,3
?.?.??#??#??##?.? 2,6
???#?????? 4,2
???##?????? 8,1
?#??##???##???#?. 1,3,7
??#??????##?? 1,1,4
??..???.?????. 2,2,1,1
?#??##?.?#? 1,3,1
??.????????##?#?? 2,3,6
.#.#??.??#.? 1,3,2,1
.?#?#???.?????. 5,1,1
????##???#?. 2,3,1
?#??#??????# 1,6,1
?.#?#.??#.##??? 1,1,2,2,1
???#????##?#?#?? 1,1,1,8
??.#..?.?????????. 1,1,1,3,1,1
?.#?##????? 4,1,1
?????.####?? 1,4
?????????????.??? 1,7,1,1
?????#??#?????#?#? 2,3,2,6
??#.?????. 2,4
.??#????#.. 3,2
???#????.??#? 4,1,1
????.??.??.??? 1,1,1,3
??##?#??#????#?..# 7,6,1
???#???.????? 4,1,3
?#?###?.#??##???# 6,2,4,1
?.#?#??.?..??.?? 3,1
#?#?.#?#?????? 1,1,1,7
????#??.??.?.?#. 5,2,1,1
???.??.????.. 1,2
?##????.???. 4,1,1
#.#?##??#???????. 1,14
?#????.####??? 2,2,5,1
??.?????#???.??? 1,5,1,1
????####???#? 7,1
?.??????#????.????? 1,8,1,1
???.?#???#.??# 2,6,2
.???#??.?#?#?? 3,4
???.????##???# 2,7,1
?????????? 1,1,1
#??????#?.??#?????? 1,3,2,3,1,1
#????????. 3,4
??.??#??.?#??#####? 2,1,1,1,9
?#????..?#?? 2,1,3
????????.??? 1,1
?????#??????.#??#?.? 1,5,1,1,5
..?#?##?????.#??#? 9,2,2
????#????.#. 1,1,3,1
???.?#??##?#? 1,7
?#?????#??? 2,4
.??#???#??#?????# 4,6,1
??..??????# 1,3,1
?????.??.?????# 5,1,3,2
.#?#..????.??????? 3,1,1,1,3
?#?##??????#? 6,1,1
?.#?.#?#?##??..???? 1,1,8,1,1
??#?????##??. 5,4
#??#???##????????# 12,1,1
??#?.????? 2,1,1
#.??#????#?.???? 1,1,4,2,2
??.#????#?#????? 1,2,4,1
????#??.??#? 5,2
?#?#???#?.. 5,3
??.??#??##???##?# 1,3,4,2,1
????..??##??.??? 3,6,3
.???.#??##.#.? 1,5,1,1
?#?????##? 2,2,3
#?.???#??#?#?.? 2,7,1
??#??#??.#?#?#?## 1,3,8
.????.#.?????#? 4,1,2,3
#.???.??#???#??? 1,3,1,1,5
??#.#.???.?????? 2,1,1,1,2
??#?#?.#?#?.##??##? 6,3,2,3
?##??.?##?.???? 2,1,2,1,1
?#?.?.???? 3,1
???????##??????? 5,5
..????.?##?? 2,3
?.??.????#??.??? 1,1,1,4,1
.??????#???#?????? 2,8
..?###???.????????? 3,6
????#?#.?????#????? 2,4,1,1,3,1
??.?.??#??? 1,1,4
????#?#?#?#???# 1,5,1,3
..#???#???.??##???#? 7,1,2,3
??.#?..???#???#. 1,1,1,5
..??????#???? 1,1,2,1
???.??#??.??.? 1,4,2
#?.#???#?. 1,2,3
.????#??#?#??.?# 1,10,2
??#.???#?.. 2,1,2
?.?.???##???#?#? 1,11
???????????#?? 1,7,1,1
#?..#?.?#?#.? 1,1,4
????#????.??##?#??? 1,6,5
???.??#???#.#?# 1,1,6,3
????????.? 3,3
???.?.#??##????? 2,1,1,3,1
..????#.??. 1,1,2
???#??##??.#???..# 10,1,1,1
??????????.?????. 8,2
??????????..?.#...?. 5,1,1,1,1,1
??.????#???.???#? 1,5,1,2
???..???##??##?? 3,9
?#.??.?... 1,2,1
#?????#?##??????#?? 1,1,8,3,1
...?????.? 1,3
?##???##????..? 8,1
?.??????##?? 1,5
#????????#?#?#???. 1,13
?#??.???#??? 1,1,1,1
???#????#????#?? 8,3
.#.###???.#? 1,3,1,1
.?##.?????.#???? 3,3
????..????##?.#??#?# 1,1,1,4,1,4
?????????#??????? 6,1,2
#??##..?##?????? 1,3,6
?#....#?##???#?# 1,10
??##??????.??. 3,1,2,2
???.????#????##?.? 1,2,2,3,1
?????.#?.??. 2,2,2
???###.???#?.??. 4,3,1
?##?#???.?? 6,2
.???.?.?.??????? 1,1,1,4,1
????#????.##?#? 6,5
.??????#?#. 2,3
????.#?#????.?##? 3,5,1,4
?.#?#.???#?#??.??? 1,1,1,7,3
.#?#?????.?.?#?#?.? 4,4
????#????.? 1,4,1
??#?#..#.##?#??? 3,1,1,7
#????##?..??. 1,5,2
???#??.??? 3,1
??.#??.??? 1,1
#?#?###???..?.#?#. 1,8,1,1,1
#...?..??.?#??##?? 1,1,1,6,1
????##??????##...??. 1,8,2,1
.?#????##????#? 1,6,1
??#???..??. 6,1
.#?#.???#???#?# 3,4,1,1
#???#.#?###?## 1,2,1,6
?##?#?#??? 6,1
#??????.#??? 2,2,4
??#?.????#?#???? 3,1,5,1
???????#?#? 1,3
#?..???#?? 2,4
??????.##??#??#?? 1,1,1,8,1
??????????.? 3,1
#???#????..?? 7,1,1
??????.##???..?????. 1,2,5,3,1
????#?#?.???.. 4,2
##?.????#?#??##???? 3,13
.?????.?##?.? 1,3
??..??.????#?? 1,1,6
?.#.???.#?#?????. 1,1,8
?#??..#???? 2,1,1
.###??#???#??# 3,8
?#?#?.???#?.?? 3,5,1
?.?.???.?.???##??.? 2,4
?????#.??????? 1,1,4,1
??.??????..#?#?? 1,3,1,1,1
???#?#??#?..? 2,3,1,1
?.##?#?.??#?#? 4,3,1
#??..??.?#???.. 3,5
?????????#?????? 1,5,1,1,1
??#???????#??? 3,3
#.?.?##????????#?? 1,1,7,1,3
??????.#???????#? 4,3,5
.??#???.#????#? 4,1,5
??#??.???.??? 1,2,1,2
#?#??##??#?##?#.??# 1,8,4,2
.#?????.???##?????? 3,2,8
?????????.??? 2,3,1,1
?????##?.???#?? 4,1,3
??????.??#????????#? 2,1,3,3
#???????#??? 2,5,1
??.??#??#??#?????? 1,1,5,1,2,1
??#??????.?.? 2,1,1,1
#????##?#????? 2,1,6,1
.#?#???#??? 3,5
???????.???.?##??. 1,2,5
?.??.???#???#?? 1,1,2,3
?.##?#??###?.???#?. 1,10,1,3
??????#.????#??? 6,4
????????..##?? 2,2,1,4
.##???????###??#?. 4,11
.???#??????????#??? 1,1,1,1,3,4
???.#??#?.##.?#?? 1,1,3,2,1
?.?#.??#?#??? 2,3
.????.?.???#?# 1,1,1,6
??.#???#?? 1,3
???.?????? 3,2,1
.???????#????#???? 12,1
???????....#??#??#? 2,1,7
#????#?????.?????.? 2,4,1,3
???#??#???? 5,1
?#?..##?#.?? 2,4,1
???#??????##???#?#?. 3,10
#?????.???.??? 3,1,2
###?????##...??. 4,4,1
??????????#.??#?? 8,2
#?.????##..?#??? 2,1,2,1,1
????##??#?...????? 1,6,3
?#?.#?????#???#? 2,1,1,4,1
????.#?##.???????# 2,4,4,1
.??#????#? 4,1
????????##??#?#? 1,1,1,7
##.???#????#???##? 2,8,4
.?#??????. 2,1,1
???.?????.? 1,2
?#?#.???##?##??# 4,8
????????.?#??#???#?. 2,1,4,3
??#??#?.?.??#?##?#?? 6,1,1,5
???#????#?..#?#?# 2,5,5
#??#??#?..?? 7,1
...?#?#??#???.#?? 7,3
???#.???#?#?.??. 2,1,3
?#?#???#??? 4,3,1
?.?##???????????? 6,2
?????.?##?#?? 1,1,7
.#????#?.?#?? 7,1
????##??.?#?#?? 1,2,1,3
.?#??##?.???##? 1,4,3
????.#??.?????? 1,1,3,3
.?#????.??. 3,1
???#??.????#?.?? 4,4
??#????#.?? 2,3
??????.??????? 3,3
????#?#.?#?##?##? 3,8
??.?#.????#???? 1,3,3
#???.???##????#. 1,1,6,1,1
#??????.?###?#??#? 1,5,3,2,1
???###???.?.?#???? 1,3,1,1,4
?????????.#?. 4,1,1
?.????????.?.. 7,1
##???#??#?#??..??. 12,2
..??????.????#.??? 1,5
#?.#?.##?.? 1,1,2
???.????#??#???????? 1,15
?#??.?????? 3,4
?????.?????##??#? 2,1,1,6
??#?##?.?##??? 5,3
#???????????.?#. 1,1,3,3,2
.??#????#?#?#?##? 2,4,6
??????.??##.. 1,4
?????##?????#???#? 1,5,1,2,1
?.#???#?#? 5,1
#?????????? 2,5,1
?#????#?????????##?. 2,5,9
??#???????. 3,1,1
?##?????..###??#?#?? 2,3,3,5
?.#???##???#????? 1,8,1,3
?????#?.???.?? 2,3,1,1
#??#??##?#?##?????# 1,1,9,2
????.?#??#???#?????? 1,2,9,1
??#??#??#.? 7,1
????#????.#????? 7,5
???.?#?#??.???#??#?? 3,3,1,1,4,1
?##??????? 3,2
##.?#??????.?.?? 2,5,1,1,1
####?#???#?.????? 4,2,2,5
?????#?#???#.??#???# 10,1,4,1
?..??#?#.?.?. 5,1
?????...??#.??? 1,2,3,1
#?#?#??.????? 5,1,3
???.????????????. 1,10
?.?###?????.??? 7,1
.??#.????#????.?? 1,1,1,4,1
???###?##???#.??? 8,1
?????#.?#???#.#??? 1,1,1,1,1,3
??#???#??#?#? 1,4,1,1
??.????.??????? 1,1,2
?????????????. 2,5,1
.????#?#???????. 2,11
??.????#?#?#? 1,3,1,1
?????????#??#? 2,1,7
????.#?.??? 2,2,1
??.??????.#??#?. 3,5
???###.?????#??? 1,3,9
???#?????#?..?? 11,1
.??#???????????#? 10,3
??.#???.????????.? 3,4
?##.?#..?????#??. 3,2,7
#?#??????.?.#.???? 1,5,1,1,1,1
..??###??#?????.? 5,7
?.?.?###?##?#???? 1,10,2
?##???????#??????.# 7,3,2,1
????#?#?.? 2,5
?.??.?#.????##?#??. 1,2,6
??#?.#?#?##?#????#. 1,1,1,4,1,4
.###??.?.?.?#? 4,1,1
???#??###?#?.?.??. 10,1
#???????#????#?.#.? 4,2,2,1,1,1
?#????#..??? 1,1,1,1
?#?#???..???.. 7,1,1
???#?#??#?. 6,1
.#???????? 1,4,1
???.???.#?#???#???? 1,1,1,1,6,1
???#..#???####??. 4,3,6
???#??#??????#?# 6,1,2,1
?####?.?.?#??.?#?. 6,4,2
???????????.?? 8,1,1
?#?.?.??.???#?#?# 2,1,7
#?#?#?#?##???###?? 7,2,5
.??##..#???..? 3,1,1,1
?#..?.??.???# 1,1,3
?????.?#??? 1,2,3
.#?#.??.#??.??????? 3,1,1,1,5
?????..?..??? 1,1,1
???????#??#.????.??? 10,3
#?#?#?..?? 3,2,1
?????.#?##??#.? 1,1,5,1
?##?.??.?#?#???? 3,6
..??.????????##? 1,2,1,1,3
?#?..?????. 1,3
??##??.#?.??..# 4,1,1,1
??.???#?##..?##????. 5,3
?.?##?..???.?.? 1,3,2,1,1
..?.??##????# 1,7
???.??.???????#??#?. 1,10
???##?..#?????....?. 4,6,1
??#??.?????. 1,4
???#?????.#?? 4,1,1,2
.?#.?#???.#.???. 2,3,1,2
???#?#??#???##???? 7,4
?#?????###? 2,4
???.#.?????? 2,1,1,1
??#.??####? 1,5
??###?..?##??. 4,3
.????.??####?#? 4,9
.????????. 1,1,1
..????#???#??? 9,1
.???????????#?#??. 5,8
??.????#?? 1,3
?..??#.??# 1,1,1
?##.??#?#??? 2,5,1
.??#????#?? 3,1
.????????????# 6,1,1
.?.?##???##??#?? 1,4,2,4
????????##??.??? 3,1,5,1
.???????##????? 1,2,5,2
???????.?#.? 3,1
?#?..?.????.????# 3,2,5
?#???#?#???#??#?? 7,3,1,1
#??#???..???# 1,1,2,4
?.???#?#?????????..? 5,5
??.??###?#??????. 1,8,1
???#?###??#?????? 1,9,1
.??#?????????#???? 3,4,5
?#??#?????.???# 2,2,4,1,1
?.??#???.???. 1,3,1,1
??#???#.#.?###..#? 1,1,3,1,4,1
##?#.?#??..???##??? 4,1,5
#????##?..?? 2,4,1
.??????..#?#..? 2,2,1,1,1
????.?.#?????##? 1,2,1,1,6
#??#.#????##?. 1,2,8
???##??##?????#?? 4,4,4
????.????#???. 1,1,1,3
??#.#?.??.?#??.??? 1,2,1,2,1,1
???##????.?##??? 8,4
?.?????.##???#???#?? 3,1,3,5
???#??????#??#????#. 1,13
.??#?.????. 1,1,1
??#???.???? 1,1,2
???#####?#????#??.? 9,2,1
#..####?????##??.# 1,8,2,1,1
???##???##???????#.? 1,11,1,1
#???????#?#?.? 1,1,3,4
??.??.????? 1,2,3
??.??##??.? 1,4
.??????#...?? 1,1
##.#?#?.?????#?????? 2,1,1,1,8
????????#..?..???#?. 3,1,1,1,4
?.#??..????#.?.#??# 3,1,2,1,1
??#?#??#????#.?.??. 11,1,1,1
#?#????##??????????? 4,11,1
?????.??.#?#??????? 2,1,9
.?#???.?#?????? 3,7
?#?????.???# 3,1,1,1
???.?????#..? 1,1,2,1
##???##?.??? 3,3
.????##?#?#????#.?.. 7,6
?.???###??.?##? 6,3
#?.#?#??????#????#?. 1,1,1,1,6
?#??#????????? 4,1,2
?.??..???#?...??.? 4,1
.?????..?.??#??. 2,2
?????##??#???? 9,2
????#????????#?#???? 5,11
????.????? 2,2
??.???.??? 1,1,1
?#???#..????? 2,1,1,1
????.??##? 3,3
.?#???#????? 2,1,3
.#?#?#??#??.#???#? 9,1,1
???#??#??##?????# 11,1
..?..????.#?#?#?. 1,1,5
?.??????.? 1,1,1
.??#??#???? 7,1
#?.#..??????????# 2,1,9,1
???.???.???.?? 1,1,2,2
?#???#????#?##?????. 2,9,2
#????.###??.??? 1,2,5,1,1
.#..????????# 1,2,5
?.#????#???.#?.##? 1,1,4,1,1,2
?#????#?.#.#?.. 2,1,3,1,1
?#.?.#??#. 2,1,4
?#???.??#? 1,1,1
?????#?#.???#?????# 7,7,1
.#?#.?.??.##??? 3,1,1,5
??.?#??.???#.? 2,4
?.???????? 2,3
??????..????? 1,1,1,3
?#?#?#????..?? 5,1
..##??.?##. 3,3
?##.???#?#. 3,4
?..#.?.???##???### 1,1,1,1,9
#??#?.??##????? 4,9
.???????.#? 2,1,2
???????..??.? 4,1,1
????.?????.?.?? 2,1,1,1,1
?#??.?##???.?#??? 2,5,5
.???#??.??#?##?. 3,5
#.??????#??????.?#? 1,10,2
??#??#?????#?? 2,2,1,3
?.???????????. 1,1,1,3
.???#?.#??? 1,2,3
?????#???????# 8,2
??.??.#??.#????#??? 1,1,1,1,1,5
??#?#????.#??????.? 1,4,1,1,1,1
.?????#??#?.??. 2,6,1
?.#?##?#?##?. 6,2
??#?#?##???.?????. 10,1,1
?#??#?????## 4,1,2
??..????#???????#?? 2,7,4
??#????????.#.? 2,1,4,1,1
??#???#..#?#?##? 1,2,2,1,5
#?????#.????. 7,3
?.?.#?##???#??..?.? 1,1,10,1
??##.#???.??#.? 3,2,1,1,1
???.?#???. 1,2,1
??.?.?#???## 2,1,1,4
#?.#????#??? 2,7
???????.???????#??? 4,6,1
.???#.?..? 1,1,1
.??#.????#????? 1,1,3,1
???.#??????#?#??#.? 2,10
..#?#?.?????#.? 1,1,1,4,1
##???#????. 6,2
..??.?##?.?#?? 2,3,2
.?.??????###???.??#? 1,9,1,3
?.?.??.#.?#. 1,2,1,2
.#?#??#?.?##.?.#?#?? 4,1,2,3
.??###???#?#????? 3,6
?.#???????#??#. 1,2,4,2,1
?#?????#?.??#?. 2,1,1,3
?????.#?.??#????? 3,2,5,1
??.###????? 1,3,2
.????????#??.?????? 1,2,1,2,1,5
?.???.???###?##.. 1,9
#??????#.?? 2,5,1
##??????????..???? 4,1,2,4
??..?##.??.??#?? 2,3,1,4
.#?.???????#??. 1,8
#?#?..????#? 1,1,2,1
?#?#.?##??? 1,1,6
??#??##???#??? 4,3,1
.???#????# 4,1
#?????????###??? 1,1,1,4,1
??#?#?????.?#.?????# 10,1,2,3
.????#.?#?.?.?? 2,1,3,1,1
???????#?#??#??.? 1,10,1
#??.????#. 2,1,1
?.??.???#.? 1,1,2
..????#???????? 9,1,1
????????#?#??#?? 4,4,2
?#??..###?##? 3,6
???#?????? 1,1,2
#??#??..??.?.?#? 6,1,1,3
??#?.##???.??# 1,3,3
????###??????. 6,1
##??###??####?..??? 14,2
???.#????? 1,3
??.?.???..?. 2,1,1,1
.?#.??#?..???#??? 1,4,3,1
??.??.????????? 1,1,3,5
#?##?????.??.#?????# 9,1,2,2,1
?#???.??.#????#?#?? 5,10
???.?????..??.#.?.?. 5,1
??#?.#?#?# 2,5
#?#????#??.??.##? 8,2
.?.?.?#??##?.#.??#?? 1,1,7,1,1,3
????#?#??.?#???# 6,6
??.#?#??#?#??????? 1,1,8,3
????.????#??#? 1,1,1,6
?.?.?##?##??#.?? 1,3,2,1,2
.???.?#?##???? 1,7
?#.?????#??. 1,2
?#.????.???#?#??#?# 1,1,1,1,9
#?.#.??#???????.???. 1,1,4,2,1,3
?#.???????.#?#?# 1,1,1,1,3
.??..##.??#??##? 2,2,2,2
?.?#?..##?.?.. 1,2
?????#?.????? 1,3,3
##??..?????#?? 4,1,2
#..?###????.? 1,4,1
?#?#???????#??. 3,7
?#?.???#??.??. 1,4,2
???#.#?##??.?##??##? 4,1,4,7
???????#..? 4,1,1
???#?????#??#?.? 2,8
..?#.??##???#?.?.. 1,9
????##??.?? 4,2
??##??#?..???##?#?#? 6,8
?.##.?.??? 2,1
.??.????#?. 1,5
?#??.#?#????????# 3,4,3,1
??#.?.?..? 2,1,1
#????????#???.##?#?. 1,6,1,5
??.?#?.#??#??????? 2,4,6
??????#???? 6,1
?????#??????##.??.. 3,6
???????##???#??.#.?? 10,2,1,1,1
.????????????#??? 1,1,10
???????##???#????? 1,1,5,4,1
.??#.?#?.???.#.?#??? 3,2,1,1,4
???..##??? 2,4
??##???#.??.#? 8,2,1
.??.??.?##??..??#? 2,5,1,1
??.???????#??#??.?? 1,2,8,1
..#?????#??.??#. 7,2
?#????#?#??#? 2,3,1,2
???#??#????#??#?.? 9,1,2,1
?.??.????. 2,3
?.???#????#.????#??? 1,1,1,1,1,5
?.?##?#.??.??#?? 5,1
?#??###???# 7,1
#?????..??? 3,1,3
?.???..??## 2,4
.?#????.?#.?.# 3,2,1,1
??#??#.#??????#?#??? 5,2,8
??.???..???##. 2,3,1,3
???????#?# 1,4
??#?.?????#?#?#???. 2,12
??.?#???#?##.?#?? 1,8,2,1
??????????..?? 2,1
??????#????? 1,5
???.??###.? 4,1
???##????#?????? 3,1,3,3
???.???#???? 1,5
#???????.?#?#?#??? 5,1,7,1
#??#???#????????.?? 1,1,4,1,2,1
.?#?..?????????#?. 2,2,6
??..??.?.. 1,2
????.#?????????###?. 1,2,1,12
#?#?##??#.?.?. 9,1
????????#??#??? 4,7
?#????#???? 3,4,1
??????#??? 1,2,1
#??#.??.?# 4,1,1
?.?????#?# 1,6
#?#?.??#???????.?? 1,2,1,1,4,2
?????????.???? 2,5,3
?#??##?.?#??##??# 1,3,5,1
??#?#.?#?..#?? 3,2,1,1
??????#??.? 3,1,1
?.?????#????..###??. 6,4
?##??#????.??. 7,1,1
#.?????????# 1,1,1,1
.??#..#??.???? 3,3,1
.????#?##?#???? 7,2
???????#???#? 2,1,2,2
?..#?????# 1,4,1
???.#?#..??# 1,3,1,1
???.#????#???????.? 1,3,2,1,1,2
#???.??#.??.?#???. 1,1,2,1,2,1
#?????.?.?????? 1,2,1,1,5
??????.???..#?#??? 3,1,1,3,1
??#????????#??#??? 8,3,1,1
??.?#?#???##..?#?? 2,4,1,2,2,1
??#???????..?? 3,5,1
.???##?.???????.? 4,4
???#??????? 3,4
#.???????# 1,1,1
#?####..#?# 6,3
.??#???.?????????.. 5,5,3
?????#.?????#?#.?# 1,3,4,2
?#????#.?#?# 1,4,2,1
??#???##???.#?????? 9,1,1,2
.?#??????? 1,2,2
????????###?????. 5,4,4
?#?##??..#?? 7,3
??#?.?????#?? 2,7
..??.?...??. 1,1,2
??.???#??.?#??? 1,2,2,2,1
???#?.???? 4,1
???#??#??#?#?#?###? 1,16
??.????#?.#??.. 1,2,2,3
???#??????##???? 4,6
##?.??.?#?? 2,1,2
??.##?#?#?.?#??. 1,7,1
??#?#??#??#????.?#? 1,13,2
????###????.????.?#? 9,1,1,1,3
??#?#???#????????#. 1,1,1,1,1,8
.#??#????.?####? 5,5
..#??##???? 1,7
.????#?#?#?#.#?#?#?? 9,6
?????..????? 1,2
???????#?#??#??.?# 1,11,2
.?.??????#???#????? 1,1,7,1,1
.???.??##?#?. 1,6
.??#???.??????? 2,2,1,4
#??..#??##?##???? 3,1,2,3,1
.?#?#??#?#?#???? 11,1
?#?#?????????.?#?# 5,1,2,3
?##???#????#? 8,1
.##?????????..? 2,1,2,1,1
???????????????????# 3,8,1,1,2
??##????..###. 5,3
.?###??????#?? 7,2
?.?..#??.#?#?.## 1,1,1,3,2
???..???#.?????##?? 2,4,2,5
.???.?????. 1,1
?#????#???.?? 2,4,1
?.??#.??.??# 1,1,1,1
?#?????#??????.??? 10,1,2
.????###??#???..?.?. 10,1,1,1
.???##?.????..?#??? 5,1,1,3,1
?##?#?????#??.? 2,3,4,1
???#??#??###?# 1,1,9
?????.?#?#??????## 4,2,1,1,2,2
.#???..???###????? 1,1,1,5,1
?#?#???????# 1,1,4,1
.?#???????#.#?.??.? 7,1,1,1,1
??????#....#??#..#?? 5,4,3
??????#?#??? 1,1,2,1
.####???#..#????#??? 8,2,3,1
.#?#.????.? 3,2
.#?????.#?####??? 2,1,1,7
#????.?#??#?#..? 1,2,2,3
????..???? 1,4
.?###.?#??????. 4,5,1
.???#.???.? 2,1,1
??????#?.?.?.?.???#. 1,1,3,1,1,4
?#????..???.. 2,1,3
?.??#????.?##?? 1,6,4
?#?????.##??#?. 4,6
??##?????..#? 9,1
??.???..??#??# 3,4
??????..??#. 1,1,1,2
?#????.???.? 1,1,1,1
??????????#?# 1,1,8
#.??#??#???.#???#? 1,3,1,1,5
#.???????.?? 1,1,4,2
?#..????.???.#?? 2,1,1,1,3
???.?.?#?#???. 1,1,3,1
.#?#??????#??.? 7,2
????.?.????? 3,1,1,1
?.????#??##???? 3,6
???????#??.. 1,1,1
???.??#?.???? 2,3,1,1
.????#?.?#.??.???? 1,1,2,2,2,1
???#?#??.. 1,3
#?#??????????? 8,3
.?##..#??????.##? 3,7,2
????#.?####??#??? 1,1,7,1
?##??#??#?##?#?## 6,9
.????#??.??? 7,1
???##?.#??#???.#.? 4,7,1
???????#?????###? 1,11
????.???.?#.? 1,1,2
???????#?##??#?#??#? 1,1,1,5,7
???.??##??####.. 5,4
????????????. 2,4,2
??????#??? 1,1
?#.?????.. 1,1,1
.???#??#??#?????. 1,6,1,3
#???.#?.#??? 3,2,1,1
?.??#?#???.??????? 3,2
?.????#?##?#?..? 1,2,7
?#?????????.?#?.? 2,1,2,3,1
#???????.? 4,1,1
#???#.?#?? 2,1,2
?..????.###????? 1,1,7
.#?#???#??? 5,3
.#?.?????#?##?..#?# 1,2,1,3,1,1
??#??#?#???.??? 8,1,3
.?#?#?#??#..?? 6,1,1
??#??.?#??? 3,2
?????#?##??.??. 1,6,1
??#?#???## 5,2
??????#????##??? 1,7
.?##?..??. 2,2
??#??#??.??????? 5,5
.?#?#??????.? 3,2
?#???###?..??? 7,1
??????????? 1,2,1
??????#.#???.???? 1,3,1,1,4
??#..#?#?#?.??#?. 3,1,4,1,2
?#?#??###?????.?? 1,9,1
???#??#??#????? 1,5,1,1,1
?#???##???...?.?#? 9,2
??#???#???#?.?.#?. 2,1,6,1,2
??.????..?.? 2,1,1,1
???????????? 6,2
?.????#?#????#??#?? 2,1,1,1,4,1
.???????#?? 1,3
??????#??#???#.?#?#? 1,1,2,6,2,2
?#???.????.??.?? 2,3,2,1
???##..??????#?? 1,2,1,5
???????.?#??????# 6,6,1
??????????? 2,4,1
??#.???#?# 1,3
???.?????? 1,6
??#.????.? 1,1,1
??????#?#..??####?? 7,1,6
..?..??????#????? 1,1,7,1
?????#.#?????#????#? 6,2,7
???.????????? 1,6,2
#??##??#??##?. 1,2,2,2
?????????.?#?????? 1,1,1,5,1
.??.??..?#??##?## 1,1,2,2,2
??#?##???.? 4,1
???#??.?..???????... 3,5
???.#?#?#.? 2,3,1
.?????#???####.#.?? 1,3,4,1,1
?#???#???.??? 2,1,1,1
?????????.? 1,4
..??.??..???##?#??.? 2,2,1,6,1
#??#?#??#..?#?????? 9,3,1
??????.???#.???? 1,3,4,1,1
???#?????????? 2,1,4
???????##???#?#??#?. 1,13
##???????? 2,1,3
#.#????##????#??# 1,7,4,1
???.??.???#? 1,1,3
.??????#.????????#?? 7,1,1,1,1,1
?..?#????? 3,1
?..?.#????#????#?? 1,1,9,1
??.?.?.?#???#?? 1,1,2,1,1
?.????.???##?#?#?#?? 1,11
??????#???.# 2,1,3,1
.?????????##?. 4,5
?.???????.???#??#. 3,1,5
??#?#.???.?.???##?? 4,1,1,6
?#?#???#?????.####?? 12,6
##????#???? 3,3
??????###?? 1,5
?.?#?#?????##????? 12,2
??#?.#.?.????#??#?. 1,1,2,6
???.???#?#???.?## 1,1,4,1,3
?.??????????.???? 1,2,4,1,2
..?#??.????? 2,2
?#.??.?????#??# 1,1,1,3,2
?##??.?#????#?# 4,4,3
?..#??#???.#??#? 4,5
??.??????? 1,2
?#??..#???????..?? 2,6,2
.#????.????#?#????? 1,1,1,8,1
#?#???#??#???#?????? 7,9,1
?.##?#??.? 4,1
#?##?.????.##?.. 4,1,3
.?#?.???##?. 3,4
#.???##?????.#. 1,5,3,1
?????#?#?#??.?#??. 10,3
?.?#..??.#??#??????? 1,2,1,7,1,1
#####??##???.??????? 10,1,1,2,1
???.????##????#.## 2,1,9,2
.#?.?..??#?#?.. 2,4
##?#..?#??#?# 4,6
##?#???..#?#.?## 5,1,3,2
??#..#??##.. 3,1,2
??????.??.???. 1,4,1,2
?.????????#??#?#??? 1,1,1,1,8
#?##?????#???#.????? 14,1,2
??###.??????.?###?? 4,1,1,3,1
???????.???. 3,2
?#??##????.????.#.?? 2,2,1,4,1,1
.#?????.?????? 1,3,2,3
?##????.?? 4,2
#.##.?????###???? 1,2,9
???##??#.?#? 4,1,1
??##???#????? 3,3
?#???#?????.???#???? 10,1,1,1
?#??..#.?.#? 2,1,1,2
??????.??.##?#?? 1,1,1,2,2
??###????????. 5,1
????##???#.???? 6,1,1,1
.?.????##?? 1,1,3
.#??.???..????#.???. 2,2,2,1,3
?????.???#?##???. 1,1,4,2,1
.??#?.??#???#.? 1,2,3,1
..???????????????? 3,4
???#.?????. 4,1
?..????#???.??...? 1,7,2,1
???????#??#?#? 4,6
.?#???.?##???#?.## 4,7,2
#??.??#?.???. 3,2
???#???????#?.?#? 1,1,5,2
#.???###??.?##???#? 1,1,4,7
???#??.??????.??#.. 4,3
????.#?#?##.##???? 1,6,3
?#.??????? 1,6
#???##?#?..??????.?? 1,7,1,1,1,1
?????????.#? 1,1,1,1
.?..?#?##?? 5,1
..???????????? 2,8
...??.?..?#?#? 1,3
??#??#???????.?? 7,1,1
????#.???#?###.?? 5,8
.????####??#??.????? 11,2
?.??????????...?? 1,2,1,2,1
?.?##??????.?..#. 6,1
#??.?????????.? 3,1,3,1
???.#??#????.?. 2,7
???.#?.?.?#?#???? 2,1,1,2,5
??????.??##?.?.#?..? 2,4,2
?????#?????.????#? 11,5
?##.??????.??#?##?? 3,3,1,1,4,1
???.??#????#?????? 4,5
?.?.?.#?#??.??? 1,1,5,1
.?.??##???##. 6,2
.?????.#?. 2,1
..???.?.???##?#?? 1,1,1,8
??#??#??#??#?#?#?. 9,6
...????.????.???? 1,3
?#???.??.##?#???? 2,1,1,7
.#?.??#???#???#?? 2,1,5,1,3
#???.#??#. 1,1,1
#????????#?#??.#?.? 1,1,9,1,1
????#???????#? 2,3,4
.????#?.??? 6,1
.??.???##?#..?? 1,5,1
?#?????#??#.???#??# 6,2,1,1,1,2
.?????#?##..#??# 9,1,1
?#???.??#.????????? 4,1,5
???????#???#.?..??? 5,2,1,1,2
.???##?.?#? 6,2
??#???#???#?????? 3,11
????##??##.????#.? 9,4,1'''
method = solve
run_test(method, [small_vector], 21)
run_test(method, [large_vector], 7633)
run_test(method, [small_vector, True], 21)
run_test(method, [large_vector, True], 7633)