#
# @lc app=leetcode id=2249 lang=python3
#
# [2249] Count Lattice Points Inside a Circle
#

# @lc code=start
from math import ceil, floor, sqrt
from typing import List


class Solution:
    def countLatticePoints(self, circles: List[List[int]]) -> int:
        points = set()
        for x, y, r in circles:
            ps = self.lattice_points_in_circle(x, y, r)
            for p in ps:
                points.add(str(p))
        return len(points)

    def lattice_points_in_circle(self, cx: int, cy: int, r: int) -> int:
        points = []
        for x in range(cx - r, cx + r + 1):
            sx = sqrt(r ** 2 - (x - cx) ** 2)
            y1 = floor(cy + sx)
            y2 = ceil(cy - sx)
            for y in range(y2, y1 + 1):
                points.append([x, y])
        return points


# @lc code=end

print(Solution().countLatticePoints([[2,2,1]]))
print(Solution().countLatticePoints([[2,2,2],[3,4,1]]))