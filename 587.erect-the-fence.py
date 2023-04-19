#
# @lc app=leetcode id=587 lang=python3
#
# [587] Erect the Fence
#

# @lc code=start
from typing import List

# Jarvis March O(nh) - Tom Switzer <thomas.switzer@gmail.com>

TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)

def cmp(a, b):
    return (a > b) - (a < b)

def turn(p, q, r):
    """Returns -1, 0, 1 if p,q,r forms a right, straight, or left turn."""
    return cmp((q[0] - p[0])*(r[1] - p[1]) - (r[0] - p[0])*(q[1] - p[1]), 0)

def _dist(p, q):
    """Returns the squared Euclidean distance between p and q."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    return dx * dx + dy * dy

def _next_hull_pt(points, p):
    """Returns the next point on the convex hull in CCW from p."""
    q = p
    for r in points:
        t = turn(p, q, r)
        if t == TURN_RIGHT or t == TURN_NONE and _dist(p, r) > _dist(p, q):
            q = r
    return tuple(q)

def convex_hull(points):
    """Returns the points on the convex hull of points in CCW order."""
    hull = [tuple(min(points))]
    for p in hull:
        q = _next_hull_pt(points, p)
        if q != hull[0]:
            hull.append(tuple(q))
    return hull

class Solution:
    def outerTrees(self, trees: List[List[int]]) -> List[List[int]]:
        hull = convex_hull(trees)
        sh = set(hull)
        for p in trees:
            p = tuple(p)
            if p not in sh:
                for i in range(len(hull) - 1):
                    x1, y1 = hull[i]
                    x2, y2 = hull[i + 1]
                    if self.colinear(x1, y1, x2, y2, p[0], p[1]):
                        sh.add(p)
                        hull.insert(i + 1, p)
        return hull

    def colinear(self, x1, y1, x2, y2, x, y):
        if x1 == x2:
            if x1 == x:
                return (y1 < y and y < y2) or (y1 > y and y > y2)
            else:
                return False
        if (x1 < x and x < x2) or (x1 > x and x > x2):
            return (x2 - x1) * (y - y1) == (x - x1) * (y2 - y1) 

# @lc code=end

from test_utils import run_test

method = Solution().outerTrees

run_test(method, [[[1,1],[2,2],[2,0],[2,4],[3,3],[4,2]]], [(1,1),(2,0),(4,2),(3,3),(2,4)])
run_test(method, [[[1,2],[2,2],[4,2]]], [(4,2),(2,2),(1,2)])
run_test(method, [[[3,0],[4,0],[5,0],[6,1],[7,2],[7,3],[7,4],[6,5],[5,5],[4,5],[3,5],[2,5],[1,4],[1,3],[1,2],[2,1],[4,2],[0,3]]],
         [(4,5),(2,5),(6,1),(3,5),(2,1),(1,4),(1,2),(7,4),(7,3),(7,2),(3,0),(0,3),(5,0),(5,5),(4,0),(6,5)])
         