
#
# @lc app=leetcode id=205 lang=python3
#
# [205] Isomorphic Strings
#

# @lc code=start
class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        st = {}
        ts = {}
        for i in range(len(s)):
            cs = s[i]
            ct = t[i]
            if cs in st:
                if st[cs] != ct:
                    return False # s char already mapped to another t char
            elif ct in ts:
                return False # t char already mapped to another s char
            st[cs] = ct
            ts[ct] = cs
        return True

# @lc code=end

