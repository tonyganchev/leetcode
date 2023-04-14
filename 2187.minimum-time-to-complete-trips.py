#
# @lc app=leetcode id=2187 lang=python3
#
# [2187] Minimum Time to Complete Trips
#

# @lc code=start
from typing import List

class Solution:
    def minimumTime(self, time: List[int], totalTrips: int) -> int:
        time.sort()
        max_time = totalTrips * time[0]
        min_time = 1

        while max_time - min_time > 0:
            m = (max_time + min_time) // 2
            trips = sum(m // t for t in time)
            if trips >= totalTrips:
                max_time = m
            else:
                min_time = m + 1
        return min_time

# @lc code=end

print(Solution().minimumTime([3, 2, 1], 5))
print(Solution().minimumTime([2], 1))
print(Solution().minimumTime([5,10,10], 9))