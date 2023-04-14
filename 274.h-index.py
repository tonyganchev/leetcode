from typing import List

#
# @lc app=leetcode id=274 lang=python3
#
# [274] H-Index
#

# @lc code=start


class Solution:
    def hIndex(self, citations: List[int]) -> int:
        # citations.sort()
        
        papers_per_cit = {}
        for c in citations:
            if c not in papers_per_cit:
                papers_per_cit[c] = 0
            papers_per_cit[c] += 1
        print(papers_per_cit);

        cits = sorted([c for c in set(citations)])
        print(cits)

        cit_map = {}
        for i in range(len(cits)):
            for j in range(i + 1):
                c = cits[j]
                if c not in cit_map:
                    cit_map[c] = 0
                cit_map[c] += papers_per_cit[cits[i]]
        print(cit_map)
        h = 0
        for cit_count, paper_count in cit_map.items():
            hc = min(cit_count, paper_count)
            h = max(h, hc)
        return h

# @lc code=end
print(Solution().hIndex([4,4,0,0]))
print(Solution().hIndex([6,6,4,8,4,3,3,10]))
