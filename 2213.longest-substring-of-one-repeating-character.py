from typing import Any, List, Tuple

#
# @lc app=leetcode id=2213 lang=python3
#
# [2213] Longest Substring of One Repeating Character
#

# @lc code=start



class StringRepetition:
    def __init__(self, begin: int, end: int) -> None:
        assert(begin <= end)
        self.begin = begin
        self.end = end

    def len(self) -> int:
        return self.end - self.begin

    def __str__(self) -> str:
        return '[{},{})'.format(self.begin, self.end)
    
    def __repr__(self) -> str:
        return str(self)

    def split(self, index: int) -> Tuple[Any]:
        assert index >= self.begin and index < self.end
        return (StringRepetition(self.begin, index),
            StringRepetition(index, index + 1),
            StringRepetition(index + 1, self.end))



class StringRepetitionMap:
    def __init__(self) -> None:
        self._repetitions = []
        self._repetitions_order = []

    def add(self, begin: int, end: int) -> int:
        r = StringRepetition(begin, end)
        idx = len(self._repetitions)
        self._repetitions.append(r)
        self._place_in_order(idx)
        return idx

    def longest(self):
        return self._repetitions[0].len()

    def _place_in_order(self, idx: int) -> None:
        for i in range(len(self._repetitions_order)):
            if self._repetitions[idx].len() > self._repetitions[i].len():
                self._repetitions_order.insert(i, idx)
                return
        self._repetitions_order.append(idx)



class StringMap:
    def __init__(self, s: str) -> None:
        self.chars = [c for c in s]
        self.repetition_map = StringRepetitionMap()
        self.repetitions = []
        cur_seq_begin = 0
        for i in range(1, len(self.chars)):
            if self.chars[i] != self.chars[cur_seq_begin]:
                idx = self.repetition_map.add(cur_seq_begin, i)
                for _ in range(cur_seq_begin, i):
                    self.repetitions.append(idx)
                cur_seq_begin = i
        if cur_seq_begin < len(self.chars) - 1:
            idx = self.repetition_map.add(cur_seq_begin, len(self.chars))
            for _ in range(cur_seq_begin, len(self.chars)):
                self.repetitions.append(idx)

    def change(self, char: str, index: int) -> int:
        if self.chars[index] == char:
            return self.repetition_map.longest()
        



class Solution:
    def longestRepeating(self, s: str, queryCharacters: str, queryIndices: List[int]) -> List[int]:
        sm = StringMap(s)
        return [sm.change(queryCharacters[i], queryIndices[i]) for i in range(len(queryCharacters))]



# @lc code=end



from test_utils import run_test



def test(s: str, queryCharacters: str, queryIndices: List[int]) -> List[int]:
    return Solution().longestRepeating(s, queryCharacters, queryIndices)


if __name__ == '__main__':

    method = test

    run_test(method, ['babacc', 'bcb', [1, 3, 3]], [3, 3, 4])
    run_test(method, ['abyzz', 'aa', [2, 1]], [2, 3])
