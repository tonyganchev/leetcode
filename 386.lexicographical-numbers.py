from typing import List

#
# @lc app=leetcode id=386 lang=python3
#
# [386] Lexicographical Numbers
#

# @lc code=start


class Solution:
    def lexicalOrder(self, n: int) -> List[int]:
        r = []
        for i in range(1, 10):
            r.extend(self.lex_ord(i, n))
        return r

    def lex_ord(self, root, limit) -> List[int]:
        if root > limit:
            return []
        r = [root]
        for i in range(10):
            r.extend(self.lex_ord(root * 10 + i, limit))
        return r

# @lc code=end

print(Solution().lexicalOrder(13))
print(Solution().lexicalOrder(23))