from typing import List

#
# @lc app=leetcode id=93 lang=python3
#
# [93] Restore IP Addresses
#

# @lc code=start


class Solution:
    def __init__(self) -> None:
        self.c = {}

    def restoreIpAddresses(self, s: str) -> List[str]:
        return self.restore_octets(s, 4)

    def restore_octets(self, s: str, octet_count: int) -> List[str]:
        if octet_count in self.c:
            if s in self.c[octet_count]:
                return self.c[octet_count][s]
        else:
            self.c[octet_count] = {}
        octets_to_test = self.possible_octets(s)
        r = []
        for ott in octets_to_test:
            if octet_count == 1:
                if len(ott) == len(s):
                    r.append(ott)
            else:
                nr = self.restore_octets(s[len(ott):], octet_count - 1)
                for n in nr:
                    r.append('{}.{}'.format(ott, n))
        self.c[octet_count][s] = r
        return r

    def possible_octets(self, s):
        if len(s) == 0:
            return []
        if s[0] == '0':
            return ['0'];
        if len(s) == 1:
            return [s]
        r = [s[0], s[:2]]
        if len(s) == 2 or int(s[0]) > 2 or (s[0] == '2' and (int(s[1]) > 5 or (s[1] == '5' and int(s[2]) > 5))):
            return r
        r.append(s[:3])
        return r
        
# @lc code=end

# print(Solution().possible_octets('0'))
# print(Solution().possible_octets('1'))
# print(Solution().possible_octets('2'))
# print(Solution().possible_octets('10345'))
# print(Solution().possible_octets('01'))
# print(Solution().possible_octets('012'))
# print(Solution().possible_octets('1354'))
print(Solution().possible_octets('216'))
# print(Solution().possible_octets('245'))
# print(Solution().possible_octets('255'))
# print(Solution().possible_octets('265'))
# print(Solution().possible_octets('256'))
# print(Solution().possible_octets('355'))
# print('-----------')
# print(Solution().restoreIpAddresses('1111'))
# print(Solution().restoreIpAddresses('111'))
# print(Solution().restoreIpAddresses('01111'))
# print(Solution().restoreIpAddresses('25525511135'))
print(Solution().restoreIpAddresses('172162541'))