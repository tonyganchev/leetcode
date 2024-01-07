#
# @lc app=leetcode id=1434 lang=python3
#
# [1434] Number of Ways to Wear Different Hats to Each Other
#

# @lc code=start
from typing import List


class Solution:
    def numberWays(self, hats: List[List[int]]) -> int:
        self.hats = hats #self.build_bitmask(hats)
        self.used = 0
        self.last_person = len(hats) - 1
        return self.solve(0)

    def solve(self, person):
        c = 0
        for hat in self.hats[person]:
            hbm = 1 << (hat - 1)
            if self.used & hbm == 0:
                if person == self.last_person:
                    c = (c + 1) % 1000000007
                else:
                    self.used |= hbm
                    c = (c + self.solve(person + 1)) % 1000000007
                    self.used &= ~hbm
        return c

    def build_bitmask(self, hats: List[List[int]]) -> List[int]:
        bitmasks = [0 for _ in hats]
        for i in range(len(hats)):
            for h in hats[i]:
                bitmasks[i] |= 1 << (h - 1)
        return bitmasks
# @lc code=end

from test_utils import run_test

def test(hats) -> int:
    return Solution().numberWays(hats)

method = test

run_test(method, [[[3,4],[4,5],[5]]], 1)
run_test(method, [[[3,5,1],[3,5]]], 4)
run_test(method, [[[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]]], 24)
run_test(method, [[
    [1,2,4,6,7,8,9,11,12,13,14,15,16,18,19,20,23,24,25],
    [2,5,16],
    [1,4,5,6,7,8,9,12,15,16,17,19,21,22,24,25],
    [1,3,6,8,11,12,13,16,17,19,20,22,24,25],
    [11,12,14,16,18,24],
    [2,3,4,5,7,8,13,14,15,17,18,21,24],
    [1,2,6,7,10,11,13,14,16,18,19,21,23],
    [1,3,6,7,8,9,10,11,12,14,15,16,18,20,21,22,23,24,25],
    [2,3,4,6,7,10,12,14,15,16,17,21,22,23,24,25]
]], 778256459)
