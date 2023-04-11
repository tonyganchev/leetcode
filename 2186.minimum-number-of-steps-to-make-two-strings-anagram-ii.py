#
# @lc app=leetcode id=2186 lang=python3
#
# [2186] Minimum Number of Steps to Make Two Strings Anagram II
#

# @lc code=start
from typing import Dict, Set


class Solution:
    def minSteps(self, s: str, t: str) -> int:
        ac = set(s + t)
        os = self.occ_map(s, ac)
        ot = self.occ_map(t, ac)
        d = 0
        for c in ac:
            d += abs(os[c] - ot[c])
        return d

    def occ_map(self, s: str, ac: Set[str]) -> Dict[str, int]:
        d = { c: 0 for c in ac }
        for c in s:
            d[c] += 1
        return d

# @lc code=end

Solution().minSteps('abc', 'def')
