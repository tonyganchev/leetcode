#
# @lc app=leetcode id=1224 lang=python3
#
# [1224] Maximum Equal Frequency
#

# @lc code=start
from typing import List


class Solution:
    def maxEqualFreq(self, nums: List[int]) -> int:
        freq_per_num = {}
        freq_count = {}
        best_prefix = 1
        for i in range(len(nums)):
            if nums[i] not in freq_per_num:
                freq_per_num[nums[i]] = 1
                if 1 not in freq_count:
                    freq_count[1] = 1
                else:
                    freq_count[1] += 1
            else:
                freq_count[freq_per_num[nums[i]]] -= 1
                if freq_count[freq_per_num[nums[i]]] == 0:
                    freq_count.pop(freq_per_num[nums[i]])
                freq_per_num[nums[i]] += 1
                if freq_per_num[nums[i]] not in freq_count:
                    freq_count[freq_per_num[nums[i]]] = 1
                else:
                    freq_count[freq_per_num[nums[i]]] += 1
            if len(freq_count) == 2:
                a, b = sorted(freq_count.items())
                if b[0] - a[0] == 1 and b[1] == 1 or a[0] == 1 and a[1] == 1:
                    best_prefix = i + 1
            elif len(freq_count) == 1:
                (f, c), = freq_count.items()
                if f == 1 or c == 1:
                    best_prefix = i + 1
        return best_prefix

# @lc code=end

from test_utils import run_test

method = Solution().maxEqualFreq

run_test(method, [[2,2,1,1,5,3,3,5]], 7)
run_test(method, [[1,1,1,2,2,2,3,3,3,4,4,4,5]], 13)
run_test(method, [[10,2,8,9,3,8,1,5,2,3,7,6]], 8)
run_test(method, [[1,2]], 2)
