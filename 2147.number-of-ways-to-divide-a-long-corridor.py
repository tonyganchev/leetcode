#
# @lc app=leetcode id=2147 lang=python3
#
# [2147] Number of Ways to Divide a Long Corridor
#

# @lc code=start
class Solution:
    def numberOfWays(self, corridor: str) -> int:
        seat_indices = []
        for i in range(len(corridor)):
            if corridor[i] == 'S':
                seat_indices.append(i)
        if len(seat_indices) % 2 == 1 or len(seat_indices) == 0:
            return 0
        ways = 1
        for i in range(2, len(seat_indices) - 1, 2):
            bush_count = seat_indices[i] - seat_indices[i - 1]
            ways *= bush_count
        return ways % 1000000007

# @lc code=end

print(Solution().numberOfWays('SSPPSPS'))
print(Solution().numberOfWays('PPSPSP'))
print(Solution().numberOfWays('S'))
print(Solution().numberOfWays('P'))
print(Solution().numberOfWays('SSPSSPSSSPPSPSPPS'))
print(Solution().numberOfWays('PPPPPSPPSPPSPPPSPPPPSPPPPSPPPPSPPSPPPSPSPPPSPSPPPSPSPPPSPSPPPPSPPPPSPPPSPPSPPPPSPSPPPPSPSPPPPSPSPPPSPPSPPPPSPSPSS'))

'''
PPPPP
SPPS
PP 3
SPPPS
PPPP 5
SPPPPS
PPPP 5
SPPS
PPP 4
SPS
PPP 4
SPS
PPP 4
SPS
PPP 4
SPS
PPPP 5
SPPPPS
PPP 4
SPPS
PPPP 5
SPS
PPPP 5
SPS
PPPP 5
SPS
PPP 4
SPPS
PPPP 5
SPS
P 2
SS
'''