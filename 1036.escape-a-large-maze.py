#
# @lc app=leetcode id=1036 lang=python3
#
# [1036] Escape a Large Maze
#

# @lc code=start
from typing import List

from numpy import full
import numpy


class Solution:
    def isEscapePossible(self, blocked: List[List[int]], source: List[int], target: List[int]) -> bool:
        if len(blocked) == 0:
            return True
       
        bottom, top, left, right = *blocked[0], *blocked[0]
        for x, y in blocked:
            bottom = min(bottom, y)
            top = max(top, y)
            left = min(left, x)
            right = max(right, x)
        print('Bounding box')
        print(top)
        print(left, right)
        print(bottom)
        if self.in_box(source[0], source[1], bottom, top, left, right):
            print('start between obstacles')
            if self.in_box(target[0], target[1], bottom, top, left, right):
                print('finish between obstacles')
                return self.can_escape(blocked, source, target, bottom, top, left, right, False, False, False, False)
            else:
                print('finish outside obstacles')
                return self.can_escape(blocked, source, None, bottom, top, left, right, True, True, True, True)
        else:
            print('start outside obstacles')
            if self.in_box(target[0], target[1], bottom, top, left, right):
                print('finish between obstacles')
                return self.can_escape(blocked, target, None, bottom, top, left, right, True, True, True, True)
            else:
                print('finish outside obstacles')
                touches_sides = left == 0 and right == 999999
                touches_top_bottom = bottom == 0 and top == 999999
                if touches_sides:
                    if source[1] < bottom and target[1] < bottom \
                            or target[1] > top and target[1] > top:
                        return True
                    else:
                        bottom = min(bottom, source[1])
                        top = max(top, source[1])
                        return self.can_escape(blocked, source, None, bottom, top, left, right,
                                               target[1] < source[1], target[1] > source[1], False, False)
                elif touches_top_bottom:
                    if source[0] < left and target[0] < left or source[0] > right and target[0] > right:
                        return True
                    else:
                        left = min(left, source[0])
                        right = max(right, source[0])
                        return self.can_escape(blocked, source, None, bottom, top, left, right,
                                               False, False, target[0] < source[0], target[0] > source[0])
                else:
                    return True

    def can_escape(self, blocked, source, target, bottom, top, left, right,
                   can_escape_bottom, can_escape_top, can_escape_left, can_escape_right):

        visited = set()
        blocked = set(tuple(b) for b in blocked)
        q = [source]
        while len(q) > 0:
            x, y = q.pop(0)
            if x >= left and y >= bottom and x <= right and y <= right \
                    and (x, y) not in visited and (x, y) not in blocked:
                if target is not None and target == (x, y) \
                        or x == left and left > 0 and can_escape_left \
                        or x == right and right < 1000000 and can_escape_right \
                        or y == bottom and bottom > 0 and can_escape_bottom \
                        or y == top and top < 1000000 and can_escape_top:
                    return True
                visited.add((x, y))
                q.append((x - 1, y))
                q.append((x + 1, y))
                q.append((x, y - 1))
                q.append((x, y + 1))
        return False
    
    def in_box(self, x, y, bottom, top, left, right):
        return x >= left and x <= right and y >= bottom and y <= top


# @lc code=end

from test_utils import run_test

method = Solution().isEscapePossible

run_test(method, [[[0,1],[1,0]], [0,0], [0,2]], False)
run_test(method, [[], [0,0], [999999,999999]], True)
run_test(method, [[[100,200],[300,400]], [0,0], [999999,999999]], True)
run_test(method, [[[691938,300406],[710196,624190],[858790,609485],[268029,225806],[200010,188664],[132599,612099],[329444,633495],[196657,757958],[628509,883388]], [655988,180910], [267728,840949]], True)
