from typing import List
#
# @lc app=leetcode id=733 lang=python3
#
# [733] Flood Fill
#

# @lc code=start


class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        oc = image[sr][sc]
        if oc == color:
            return image
        h = len(image)
        w = len(image[0])
        jobs = [[sr, sc]]
        while len(jobs) > 0:
            r, c = jobs[0]
            jobs = jobs[1:]
            if r >= 0 and r < h and c >= 0 and c < w and image[r][c] == oc:
                image[r][c] = color
                jobs.append([r - 1, c])
                jobs.append([r + 1, c])
                jobs.append([r, c - 1])
                jobs.append([r, c + 1])

        return image

# @lc code=end

Solution().floodFill([[1,1,1],[1,1,0],[1,0,1]], 1, 1, 2)
