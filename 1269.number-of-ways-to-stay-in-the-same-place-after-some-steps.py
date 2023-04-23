#
# @lc app=leetcode id=1269 lang=python3
#
# [1269] Number of Ways to Stay in the Same Place After Some Steps
#

# @lc code=start
from numpy import full


class Solution:
    def numWays(self, steps: int, arrLen: int) -> int:
        arrLen = min(arrLen, steps // 2 + 1)
        cache = {}
        return self.solve(steps, arrLen, 0, cache) % 1000000007


    def solve(self, steps, arr_len, idx, cache):
        self.print('from', idx, 'steps', steps)
        if steps not in cache:
            cache[steps] = {}
        if idx not in cache[steps]:
            if steps == 0:
                if idx == 0:
                    self.print('reached 0')
                    s = 1
                else:
                    self.print('cannot reach 0 from', idx)
                    s = 0
            elif idx > steps:
                self.print('cannot reach 0 from', idx)
                s = 0
            elif idx == steps:
                self.print('only lefts', idx)
                s = 1
            else:
                s = 0
                if idx < arr_len - 1:
                    self.print('test right')
                    s += self.solve(steps - 1, arr_len, idx + 1, cache)
                self.print('test stay')
                s += self.solve(steps - 1, arr_len, idx, cache)
                if idx > 0:
                    self.print('test left')
                    s += self.solve(steps - 1, arr_len, idx - 1, cache)
            cache[steps][idx] = s
        self.print('from', idx, 'steps', steps, 'options', cache[steps][idx])
        return cache[steps][idx]
    
    def print(self, *args):
        if False:
            print(*args)

# @lc code=end

from test_utils import run_test

method = Solution().numWays

run_test(method, [3, 2], 4)
run_test(method, [2, 4], 2)
run_test(method, [4, 2], 8)
run_test(method, [27, 7], 127784505)

