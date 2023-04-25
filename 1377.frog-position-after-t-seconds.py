from typing import List

#
# @lc app=leetcode id=1377 lang=python3
#
# [1377] Frog Position After T Seconds
#

# @lc code=start
class Solution:
    def frogPosition(self, n: int, edges: List[List[int]], t: int, target: int) -> float:
        transitions = self.build_transition_map(edges)

        q = [(1, 1.0)]
        while len(q) > 0 and t >= 0:
            nq = []
            for node, probability in q:
                to_nodes = transitions.get(node)
                if node == target:
                    if t == 0 or to_nodes is None:
                        return probability
                    else:
                        return 0.0
                if to_nodes is not None:
                    next_probability = probability / len(to_nodes)
                    nq.extend((to_node, next_probability) for to_node in transitions[node])
            q = nq
            t -= 1
        return 0.0

    def build_transition_map(self, edges):
        all_transitions = {}
        for from_node, to_node in edges:
            if from_node not in all_transitions:
                all_transitions[from_node] = []
            all_transitions[from_node].append(to_node)
            if to_node not in all_transitions:
                all_transitions[to_node] = []
            all_transitions[to_node].append(from_node)
        if len(all_transitions) == 0:
            return all_transitions
        visited = set()
        q = [1]
        transitions = {}
        while len(q) > 0:
            nq = []
            for from_node in q:
                if from_node not in visited:
                    visited.add(from_node)
                    for to_node in all_transitions[from_node]:
                        if to_node not in visited:
                            if from_node not in transitions:
                                transitions[from_node] = []
                            transitions[from_node].append(to_node)
                            nq.append(to_node)
            q = nq
        return transitions

        

# @lc code=end

from test_utils import run_test

def test(n: int, edges: List[List[int]], t: int, target: int) -> float:
    return Solution().frogPosition(n, edges, t, target)

method = test

run_test(method, [1, [], 1, 1], 1.0)
run_test(method, [5, [[1,5],[1,4],[5,3],[3,2]], 3, 2], 0.5)
run_test(method, [3, [[2,1],[3,2]], 1, 2], 1.0)
run_test(method, [7, [[1,2],[1,3],[1,7],[2,4],[2,6],[3,5]], 2, 4], 0.16666666666666666)
run_test(method, [7, [[1,2],[1,3],[1,7],[2,4],[2,6],[3,5]], 1, 7], 0.3333333333333333)
run_test(method, [8, [[2,1],[3,2],[4,1],[5,1],[6,4],[7,1],[8,7]], 7, 7], 0.0)
