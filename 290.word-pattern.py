#
# @lc app=leetcode id=290 lang=python3
#
# [290] Word Pattern
#

# @lc code=start
class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        pm = {}
        used = {}
        words = s.split(' ')
        if len(words) != len(pattern):
            return False
        for i in range(len(words)):
            if pattern[i] in pm:
                if pm[pattern[i]] != words[i]:
                    return False
            else:
                if words[i] in used and used[words[i]] != pattern[i]:
                    return False
                pm[pattern[i]] = words[i]
                used[words[i]] = pattern[i]
        return True
# @lc code=end

# print(Solution().wordPattern('abba', 'dog cat cat dog'))
# print(Solution().wordPattern('abba', 'dog cat cat fish'))
# print(Solution().wordPattern('aaaa', 'dog cat cat dog'))
# print(Solution().wordPattern('aaaa', 'dog dog dog dog'))
print(Solution().wordPattern('abc', 'dog cat dog'))