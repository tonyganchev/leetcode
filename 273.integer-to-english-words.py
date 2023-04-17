#
# @lc app=leetcode id=273 lang=python3
#
# [273] Integer to English Words
#

# @lc code=start
class Solution:
    def __init__(self) -> None:
        self.names = {
            1: 'One',
            2: 'Two',
            3: 'Three',
            4: 'Four',
            5: 'Five',
            6: 'Six',
            7: 'Seven',
            8: 'Eight',
            9: 'Nine',
            10: 'Ten',
            11: 'Eleven',
            12: 'Twelve',
            13: 'Thirteen',
            14: 'Fourteen',
            15: 'Fifteen',
            16: 'Sixteen',
            17: 'Seventeen',
            18: 'Eighteen',
            19: 'Nineteen'
        }
        self.tens = {
            2: 'Twenty',
            3: 'Thirty',
            4: 'Forty',
            5: 'Fifty',
            6: 'Sixty',
            7: 'Seventy',
            8: 'Eighty',
            9: 'Ninety'
        }
    def numberToWords(self, num: int) -> str:
        if num == 0:
            return 'Zero'
        r = ''
        bil = num // 1000000000
        if bil > 0:
            r += self.numberToWords(bil) + ' Billion '
        num %= 1000000000
        if num > 0 :
            mil = num // 1000000
            if mil > 0:
                r += self.numberToWords(mil) + ' Million '
            num %= 1000000
            if num > 0:
                tho = num // 1000
                if tho > 0:
                    r += self.numberToWords(tho) + ' Thousand '
                num %= 1000
                if num > 0:
                    hun = num // 100
                    if hun > 0:
                        r += self.numberToWords(hun) + ' Hundred '
                    num %= 100
                    if num > 0:
                        if num > 19:
                            dec = num // 10
                            r += self.tens[dec] + ' '
                            num %= 10
                        if num > 0:
                            r += self.names[num] + ' '
        return r[:-1]

# @lc code=end

print(Solution().numberToWords(123))
print(Solution().numberToWords(12345))
print(Solution().numberToWords(1234567))
print(Solution().numberToWords(20))

