#
# @lc app=leetcode id=1298 lang=python3
#
# [1298] Maximum Candies You Can Get from Boxes
#

# @lc code=start
from typing import List

AVAILABLE = 0x02
OPEN = 0x01
PROCESSED = 0x04

class Solution:
    def maxCandies(self, status: List[int], candies: List[int], keys: List[List[int]], containedBoxes: List[List[int]], initialBoxes: List[int]) -> int:
        q = initialBoxes[:]
        for i in initialBoxes:
            status[i] |= AVAILABLE
        candy_count = 0
        while len(q) > 0:
            changed = False
            for qi in range(len(q)):
                i = q[qi]
                if status[i] == AVAILABLE | OPEN:
                    changed = True
                    status[i] |= PROCESSED
                    candy_count += candies[i]
                    for b in containedBoxes[i]:
                        status[b] |= AVAILABLE
                        q.append(b)
                    for k in keys[i]:
                        status[k] |= OPEN
                        q.append(k)
                    q.pop(qi)
                    break
            if not changed:
                break

        return candy_count
# @lc code=end

from test_utils import run_test

method = Solution().maxCandies

run_test(method, [[1,0,1,0], [7,5,4,100], [[],[],[1],[]], [[1,2],[3],[],[]], [0]], 16)
run_test(method, [[1,0,0,0,0,0], [1,1,1,1,1,1], [[1,2,3,4,5],[],[],[],[],[]], [[1,2,3,4,5],[],[],[],[],[]], [0]], 6)
