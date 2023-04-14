from typing import List

#
# @lc app=leetcode id=119 lang=python3
#
# [119] Pascal's Triangle II
#

# @lc code=start


class Solution:
    def getRow(self, rowIndex: int) -> List[int]:
        r = [1]
        if rowIndex == 0:
            return r
        pr = self.getRow(rowIndex - 1)
        pr.append(0)
        for i in range(0, rowIndex):
            r.append(pr[i] + pr[i + 1])
        return r

# @lc code=end

