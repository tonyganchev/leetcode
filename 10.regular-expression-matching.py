#
# @lc app=leetcode id=10 lang=python3
#
# [10] Regular Expression Matching
#

# @lc code=start
class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        changes = True
        while changes:
            changes = False
            for i, c in enumerate(p):
                if c == '*' \
                    and len(p) >= i + 3 \
                        and p[i - 1] == p[i + 1] \
                            and p[i + 2] == '*':
                    p = p[ : i - 1] + p[i + 1 : ]
                    changes = True
                    break
        return self._isMatch(s, p)

    def _isMatch(self, s: str, p: str) -> bool:
        if len(s) == 0:
            if len(p) == 0:
                return True
            if len(p) == 1:
                return False
            if p[1] == '*':
                return self._isMatch(s, p[2 : ])
            return False
        if len(p) == 0:
            return False
        assert p[0] != '*'
        if p[0] == '.' or s[0] == p[0]:
            if len(p) == 1 or p[1] != '*':
                return self._isMatch(s[1 : ], p[1 : ])
            return self._isMatch(s[1 : ], p) \
                or self._isMatch(s[1 : ], p[2 : ]) \
                    or self._isMatch(s, p[2 : ])
        if p[0] != '.' and s[0] != p[0] and len(p) > 1 and p[1] == '*':
            return self._isMatch(s, p[2 : ])
        return False
# @lc code=end

from test_utils import run_test

def test (a, b):
    return Solution().isMatch(a, b)
method = test

run_test(method, ['aaaaaaaaaaaaab', 'a*a*a*a*a*a*a*a*a*c'], False)
run_test(method, ['a', '..a*'], False)
run_test(method, ['a', '.*..a*'], False)
run_test(method, ['a', '.*a*a'], True)
run_test(method, ['ba', '.*a*a'], True)
run_test(method, ['', ''], True)
run_test(method, ['', '.*'], True)
run_test(method, ['', 'a*'], True)
run_test(method, ['aa', 'a'], False)
run_test(method, ['aa', 'aa'], True)
run_test(method, ['aa', '.b'], False)
run_test(method, ['aa', '.a'], True)
run_test(method, ['aa', 'a*'], True)
run_test(method, ['aa', '..'], True)
run_test(method, ['aa', '.*'], True)
run_test(method, ['aa', 'a*b*'], True)
run_test(method, ['aab', 'a*b*'], True)
run_test(method, ['aab', 'a*.*'], True)
run_test(method, ['si', 's*'], False)
run_test(method, ['sippi', 's*p*.'], False)
run_test(method, ['issippi', 'is*p*.'], False)
run_test(method, ['ssissippi', 's*is*p*.'], False)
run_test(method, ['mississippi', 'mis*is*p*.'], False)
run_test(method, ['bbbba', '.*a*a'], True)