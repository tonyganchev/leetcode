#
# @lc app=leetcode id=1866 lang=python3
#
# [1866] Number of Ways to Rearrange Sticks With K Sticks Visible
#

from typing import List

# @lc code=start

from functools import cache
from itertools import permutations

@cache
def fact(n):
    assert n >= 0
    return 1 if n <= 1 else n * fact(n - 1)

def variants_for_peaks(
    n: int,
    barriers: List[int]
    ) -> int:

    elements = list(range(1, n + 1))
    valid_count = 0
    
    # Pre-calculate constraints for non-barrier elements
    # Map element -> The barrier it must be AFTER
    constraints = {}
    for el in elements:
        if el in barriers:
            continue
            
        # Find the first barrier that is greater than the element
        # Case 3 Example: For el=1, barriers=[3,4]. First barrier > 1 is 3.
        forcing_barrier = next((b for b in barriers if b > el), None)
        
        if forcing_barrier:
            constraints[el] = forcing_barrier

    # Iterate through all permutations of 1 to n
    for p in permutations(elements):
        
        # Rule 1: First element must be the first barrier
        if p[0] != barriers[0]:
            continue
            
        # Rule 2: Barriers must be in relative order
        p_barriers = [x for x in p if x in barriers]
        if p_barriers != barriers:
            continue
            
        # Rule 3: Check "Value Push" constraints
        is_valid = True
        for el, barrier in constraints.items():
            # The element must appear at a higher index than its forcing barrier
            if p.index(el) < p.index(barrier):
                is_valid = False
                break
        
        if is_valid:
            valid_count += 1

    return valid_count

def peaks(n: int, k: int, cur_peaks: List[int]) -> int:
    if len(cur_peaks) == k + 1:
        v = variants_for_peaks(n, cur_peaks[1 : ])
        # print(cur_peaks[1 : ], v)
        return v
    variants_count = 0
    test_from = n if len(cur_peaks) == k else cur_peaks[-1] + 1
    test_to = n - k + len(cur_peaks)
    for i in range(test_from, test_to + 1):
        cur_peaks.append(i)
        variants_count += peaks(n, k, cur_peaks)
        cur_peaks.pop()
    return variants_count % (10 ** 9 + 7)


class Solution:
    def rearrangeSticks(self, n: int, k: int) -> int:
        return peaks(n, k, [0])

# @lc code=end

from test_utils import run_test

method = variants_for_peaks

run_test(method, [4, [1, 4]], 2)
run_test(method, [4, [2, 4]], 3)
run_test(method, [4, [3, 4]], 6)
run_test(method, [5, [1, 5]], 6)
run_test(method, [5, [2, 5]], 8)
run_test(method, [5, [3, 5]], 12)
run_test(method, [5, [4, 5]], 24)

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
# run_test(method, [16, 11], 78558480) # verified

# run_test(method, [20, 11], 647427950) # verified

