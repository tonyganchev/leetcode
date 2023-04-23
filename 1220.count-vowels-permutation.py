#
# @lc app=leetcode id=1220 lang=python3
#
# [1220] Count Vowels Permutation
#

# @lc code=start
class Solution:
    def countVowelPermutation(self, n: int) -> int:
        prec = {
            'a': ['e', 'i', 'u'],
            'e': ['a', 'i'],
            'o': ['i'],
            'u': ['o', 'i'],
            'i': ['e', 'o']
        }

        perms = { l: 1 for l in prec.keys() }

        while n > 1:
            new_perms = { l: 0 for l in prec.keys() }
            for l, k in perms.items():
                for pl in prec[l]:
                    new_perms[pl] += k
            perms = new_perms
            n -= 1
        
        return sum(perms.values()) % 1000000007
# @lc code=end

# a -> e
# e -> a i
# i -> a e o u
# o -> i u
# u -> a

# e i u -> a
# a i -> e
# i -> o
# o i -> u
# e o -> i

from test_utils import run_test

method = Solution().countVowelPermutation

run_test(method, [1], 5)
run_test(method, [2], 10)
run_test(method, [5], 68)
run_test(method, [50], 227130014)
run_test(method, [5000], 598627501)
run_test(method, [20000], 759959057)
