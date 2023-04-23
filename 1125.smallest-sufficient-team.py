#
# @lc app=leetcode id=1125 lang=python3
#
# [1125] Smallest Sufficient Team
#

# @lc code=start
from typing import List, Set


class Solution:
    def smallestSufficientTeam(self, req_skills: List[str], people: List[List[str]]) -> List[int]:
        req_skills = set(req_skills)
        people = {i: set(skill for skill in people[i]) for i in range(len(people))}
        return self.smallest_team(req_skills, people)
    
    def smallest_team(self, req_skills: Set[str], people):
        # print('---------')
        # print('req', req_skills)
        # print('peo', people)
        smallest = None
        for s in req_skills:
            for i, p in people.items():
                if s in p:
                    new_req_skills = req_skills.difference(p)
                    if len(new_req_skills) == 0:
                        # print([i])
                        return [i]
                    new_people = { j : p for j, p in people.items() }
                    new_people.pop(i)
                    team = self.smallest_team(new_req_skills, new_people)
                    if team is not None and (smallest is None or len(team) + 1 < len(smallest)):
                        smallest = [i] + team
        # print(smallest)
        return smallest
# @lc code=end

from test_utils import run_test

def test(req, people):
    return set(Solution().smallestSufficientTeam(req, people))

method = test

run_test(method, [["java","nodejs","reactjs"], [["java"],["nodejs"],["nodejs","reactjs"]]], set([0,2]))
run_test(method, [["algorithms","math","java","reactjs","csharp","aws"], [["algorithms","math","java"],["algorithms","math","reactjs"],["java","csharp","aws"],["reactjs","csharp"],["csharp","math"],["aws","java"]]], set([2,1]))
run_test(method, [["rttqr","znubhmm","rgyljkdqpnp","pxlznqxi","ltv","utkcvlmvief","czemctygnzxosxt"], [[],["rgyljkdqpnp"],["rgyljkdqpnp","czemctygnzxosxt"],[],[],["znubhmm","rgyljkdqpnp","ltv"],["ltv"],["rgyljkdqpnp"],[],["znubhmm"],["rgyljkdqpnp"],[],["rgyljkdqpnp","pxlznqxi"],["ltv"],["rgyljkdqpnp"],["znubhmm","rgyljkdqpnp"],[],["czemctygnzxosxt"],["znubhmm","pxlznqxi","czemctygnzxosxt"],[],["czemctygnzxosxt"],["czemctygnzxosxt"],["znubhmm"],["pxlznqxi"],["czemctygnzxosxt"],["rgyljkdqpnp"],[],["rgyljkdqpnp","czemctygnzxosxt"],["znubhmm","utkcvlmvief"],["rttqr","rgyljkdqpnp","czemctygnzxosxt"],[],["pxlznqxi","czemctygnzxosxt"],["rttqr","pxlznqxi","czemctygnzxosxt"],[],[],["rttqr"],[],[],["pxlznqxi","czemctygnzxosxt"],["rgyljkdqpnp"]]], set([5,28,32]))
