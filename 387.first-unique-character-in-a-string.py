#
# @lc app=leetcode id=387 lang=python3
#
# [387] First Unique Character in a String
#

# @lc code=start
class Solution:
    def firstUniqChar(self, s: str) -> int:
        occ_cnt = [0 for i in range(26)]
        for c in s:
            orda = ord('a')
            occ_cnt[ord(c) - orda] += 1
        for i in range(len(s)):
            if occ_cnt[ord(s[i]) - ord('a')] == 1:
                return i
        return -1
# @lc code=end

print(Solution().firstUniqChar('leetcode'))
