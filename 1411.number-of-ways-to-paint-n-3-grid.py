#
# @lc app=leetcode id=1411 lang=python3
#
# [1411] Number of Ways to Paint N × 3 Grid
#

# @lc code=start
import numpy as np


class Solution:
    def numOfWays(self, n: int) -> int:

        # solution from https://leetcode.com/problems/number-of-ways-to-paint-n-3-grid/solutions/575485/c-python-o-logn-time/
        n, mod = n - 1, 10**9 + 7
        M = np.matrix([[3, 2], [2, 2]])
        res = [6, 6]
        while n:
            if n % 2:
                res = res * M % mod
            M = M * M % mod
            # Fix per https://leetcode.com/problems/number-of-ways-to-paint-n-3-grid/solutions/575485/c-python-o-logn-time/comments/673840
            n //= 2
        return (np.sum(res)) % mod
        # ---------------------------------

        row_perm = []
        for a in range(3):
            for b in range(3):
                if b != a:
                    for c in range(3):
                        if c != b:
                            row_perm.append((a, b, c))

        row_transitions = { rp: [] for rp in row_perm }
        for rp in row_perm:
            for trp in row_perm:
                can_place = True
                for i in range(3):
                    if rp[i] == trp[i]:
                        can_place = False
                        break
                if can_place:
                    row_transitions[rp].append(trp)
        
        q = row_perm
        i = 1
        cases = 0
        while len(q) > 0:
            nq = []
            for p in q:
                if i == n:
                    cases += 1
                else:
                    nq.extend(row_transitions[p])
            q = nq
            i += 1
        return cases
# @lc code=end

from test_utils import run_test

method = Solution().numOfWays

run_test(method, [1], 12)
run_test(method, [5], 5110)
run_test(method, [10], 5110)
run_test(method, [50], 5110)
run_test(method, [100], 5110)
run_test(method, [5000], 30228214)

