#
# @lc app=leetcode id=1866 lang=python3
#
# [1866] Number of Ways to Rearrange Sticks With K Sticks Visible
#

from typing import List

# @lc code=start

from functools import cache
from itertools import combinations

@cache
def fact(n):
    assert n >= 0
    return 1 if n <= 1 else n * fact(n - 1)

def count_sequences_optimized(n, barriers):
    # Rule: If barriers are empty or k=1, result is (n-1)!
    k = len(barriers)
    if k <= 1:
        return fact(n - 1)
    
    # The Magic Formula
    numerator = fact(n - 1)
    
    denominator = 1
    last_barrier = barriers[-1]
    
    # Product of (Last_Barrier - Current_Barrier) for all previous barriers
    for i in range(k - 1):
        denominator *= (last_barrier - barriers[i])
        
    return numerator // denominator

class Solution:
    def rearrangeSticks(self, n: int, k: int) -> int:
        total_valid_count = 0
        elements = range(1, n)
        
        # Iterate through all combinations of k barriers
        for b_set in combinations(elements, k - 1):
            # b_set comes out sorted from combinations, which is what we want
            total_valid_count += count_sequences_optimized(n, list(b_set) + [n])
            
        return total_valid_count % (10 ** 9 + 7)

# @lc code=end

from test_utils import run_test

def test(n, k):
    return Solution().rearrangeSticks(n, k)
method = test

run_test(method, [4, 2], 11) # verified
run_test(method, [2, 1], 1) # verified
run_test(method, [5, 2], 50) # verified
run_test(method, [3, 2], 3) # verified
run_test(method, [5, 5], 1) # verified
run_test(method, [11, 11], 1) # verified
run_test(method, [12, 11], 66) # verified
run_test(method, [13, 11], 2717) # verified
run_test(method, [14, 11], 91091) # verified
run_test(method, [15, 11], 2749747) # verified
run_test(method, [16, 11], 78558480) # verified
run_test(method, [20, 11], 647427950) # verified
run_test(method, [105, 20], 647427950) # verified
