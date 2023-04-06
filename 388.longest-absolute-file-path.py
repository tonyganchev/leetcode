#
# @lc app=leetcode id=388 lang=python3
#
# [388] Longest Absolute File Path
#

# @lc code=start
class Solution:
    def lengthLongestPath(self, input: str) -> int:
        raw_entires = input.splitlines()
        print(raw_entires)
        stack = []
        max_len = 0
        for raw_entry in raw_entires:
            i = 0
            while i < len(raw_entry) and raw_entry[i] == '\t':
                i += 1
            if len(stack) > i:
                stack = stack[:i]
            entry = raw_entry[i:]
            full_entry = (stack[-1] + '/' if len(stack) > 0 else '') + entry
            if entry.find('.') != -1:
                max_len = max(max_len, len(full_entry))
            else:
                stack.append(full_entry)
            print(full_entry)
        return max_len

# @lc code=end

print(Solution().lengthLongestPath("dir\n\tsubdir1\n\t\tfile1.ext\n\t\tsubsubdir1\n\tsubdir2\n\t\tsubsubdir2\n\t\t\tfile2.ext"))
