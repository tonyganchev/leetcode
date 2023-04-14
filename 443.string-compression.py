from typing import List

#
# @lc app=leetcode id=443 lang=python3
#
# [443] String Compression
#

# @lc code=start

class Solution:
    def compress(self, chars: List[str]) -> int:
        group_begin = 0
        while True:
            if group_begin == len(chars):
                break
            group_end = group_begin
            while group_end < len(chars) and chars[group_end] == chars[group_begin]:
                group_end += 1
            group_length = group_end - group_begin

            nchars = chars[:group_begin]
            nchars.append(chars[group_begin])
            if group_length > 1:
                str_group_length = str(group_length)
                nchars.extend([c for c in str_group_length])
                group_begin += len(str_group_length)
            nchars.extend(chars[group_end:])
            group_begin += 1
            chars.clear()
            chars.extend(nchars)
        return len(chars)
            

# @lc code=end

# print(Solution().compress(["a","a","b","b","c","c","c"]))
# print(Solution().compress(["a"]))
# chars = ["a","b","b","b","b","b","b","b","b","b","b","b","b"]
# print(Solution().compress(chars))
# print(chars)
chars = ["a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a"]
print(Solution().compress(chars))
print(chars)
