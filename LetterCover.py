def perm(p, q, i, best_so_far, s):
    if len(s) > best_so_far:
        return best_so_far
    while i < len(p) and (p[i] in s or q[i] in s):
        i += 1
    if i == len(p):
        # print(best_so_far, s, p[:i + 1])
        return min(best_so_far, len(s))
    for c in (p[i], q[i]):
        if i == len(p) - 1:
            new_uniques = len(s) + (0 if c in s else 1)
            # print(s, c, new_uniques)
            best_so_far = min(best_so_far, new_uniques)
        else:
            news = s.union({c})
            best_so_far = perm(p, q, i + 1, best_so_far, news)
    return best_so_far


class Choice:
    def __init__(self, p, q):
        [first, second] = sorted([p, q])
        self.first = first
        self.second = second

    def __str__(self):
        return f'{self.first}/{self.second}'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.first == other.first and self.second == other.second

    def __hash__(self):
        return hash(self.first + self.second)

def solution(p, q):
    unique_digits = set()
    all_choices = set()
    for i in range(len(p)):
        if p[i] == q[i]:
            unique_digits.add(p[i])
        else:
            all_choices.add(Choice(p[i], q[i]))
    non_trivial_choices = set()
    for c in all_choices:
        if c.first not in unique_digits and c.second not in unique_digits:
            non_trivial_choices.add(c)
    print(unique_digits)
    print(non_trivial_choices)

    p = [c.first for c in non_trivial_choices]
    q = [c.second for c in non_trivial_choices]
    return perm(p, q, 0, len(unique_digits) + len(p), unique_digits)

from test_utils import run_test

method = solution

run_test(method, ['aaaaaaaaaaaaabbbbbbbbbcccc','cccccccdddddddeeeeeeeeeeff'], 3)
run_test(method, ['abcdefghijklmnopqrstuvwxyz','aacceeggiikkmmooqqssuuwwyy'], 13)
run_test(method, [
    'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz',
    'aacceeggiikkmmooqqssuuwwyyaacceeggiikkmmooqqssuuwwyy'], 13)
run_test(method, [
    'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz',
    'aacceeggiikkmmooqqssuuwwyyaacceeggiikkmmooqqssuuwwyyabcdefghijklmnopqrstuvwxyz'], 26)
run_test(method, [
    'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz',
    'aacceeggiikkmmooqqssuuwwyyaacceeggiikkmmooqqssuuwwyyabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'], 26)

import random
import string

run_test(method, [
    ''.join(random.choices(string.ascii_lowercase, k = 10000)),
    ''.join(random.choices(string.ascii_lowercase, k = 10000))
], 26)