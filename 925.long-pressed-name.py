#
# @lc app=leetcode id=925 lang=python3
#
# [925] Long Pressed Name
#

# @lc code=start
import re

class Solution:
    def isLongPressedName(self, name: str, typed: str) -> bool:
        letters = []        
        for i, c in enumerate(name):
            if len(letters) == 0 or letters[-1][0] != c:
                letters.append([c, 1])
            else:
                letters[-1][1] += 1

        rp = '^'
        for c, n in letters:
            rp += c + '{' + str(n) + ',}'
        rp += '$'
        print(rp)
        return re.search(rp, typed) is not None
# @lc code=end

