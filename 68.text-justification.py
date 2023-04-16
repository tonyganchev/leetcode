#
# @lc app=leetcode id=68 lang=python3
#
# [68] Text Justification
#

# @lc code=start
from typing import List



class Line:
    def __init__(self) -> None:
        self.words = []
        self.word_length = 0
    
    def min_len(self) -> int:
        return self.word_length + len(self.words) - 1
    
    def add_word(self, word: str) -> None:
        self.words.append(word)
        self.word_length += len(word)
    
    def __repr__(self) -> str:
        return str(self.words)



class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        line = Line()
        lines = [line]
        for w in words:
            if line.min_len() + len(w) + 1 > maxWidth:
                line = Line()
                lines.append(line)
            line.add_word(w)
        result = []
        for i in range(len(lines)):
            line = lines[i]
            if i == len(lines) - 1 or len(line.words) == 1:
                line_str = ' '.join(line.words) + ' ' * (maxWidth - line.min_len())
                result.append(line_str)
            else:
                spaces_to_place = maxWidth - line.word_length
                mandatory_delimiter_length = spaces_to_place // (len(line.words) - 1)
                mandatory_delimiter = ' ' * mandatory_delimiter_length
                extra_spaces = spaces_to_place % (len(line.words) - 1)
                line_str = ''
                for i in range(len(line.words) - 1):
                    w = line.words[i]
                    line_str += w + mandatory_delimiter
                    if extra_spaces > 0:
                        line_str += ' '
                        extra_spaces -= 1
                line_str += line.words[-1]
                result.append(line_str)
        return result



# @lc code=end

from test_utils import run_test

method = Solution().fullJustify

run_test(method, [["This", "is", "an", "example", "of", "text", "justification."], 16], ["This    is    an", "example  of text", "justification.  "])
run_test(method, [["What","must","be","acknowledgment","shall","be"], 16], ["What   must   be", "acknowledgment  ", "shall be        "])
run_test(method, [["Science","is","what","we","understand","well","enough","to","explain","to","a","computer.","Art","is","everything","else","we","do"], 20], ["Science  is  what we", "understand      well", "enough to explain to", "a  computer.  Art is", "everything  else  we", "do                  "])
