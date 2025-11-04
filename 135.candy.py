#
# @lc app=leetcode id=135 lang=python3
#
# [135] Candy
#

# @lc code=start
from typing import List


class Solution:
    def candy(self, ratings: List[int]) -> int:
        if len(ratings) == 1:
            return 1
        candy_diff = [0]
        min_diff = 0
        for i in range(1, len(ratings)):
            if ratings[i] > ratings[i - 1]:
                candy_diff.append(candy_diff[i - 1] + 1)
            else:
                candy_diff.append(candy_diff[i - 1] - 1)
                min_diff = min(min_diff, candy_diff[-1])
        print(candy_diff)
        r = sum(v - min_diff + 1 for v in candy_diff)

        return r

# @lc code=end

from test_utils import run_test

method = Solution().candy

run_test(method, [[1,0,2]], 5)
run_test(method, [[1,2,2]], 4)
run_test(method, [[1,3,2,2,1]], 7)
