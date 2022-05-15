#
# @lc app=leetcode id=2241 lang=python3
#
# [2241] Design an ATM Machine
#

# @lc code=start
from typing import List


class ATM:

    def __init__(self):
        self.bank_notes = [20, 50, 100, 200, 500]
        self.bank_note_supply = { bn: 0 for bn in self.bank_notes }


    def deposit(self, banknotesCount: List[int]) -> None:
        for i in range(len(banknotesCount)):
            self.bank_note_supply[self.bank_notes[i]] += banknotesCount[i]


    def withdraw(self, amount: int) -> List[int]:
        bns = reversed(self.bank_notes)
        bank_notes_used = {}
        for bn in bns:
            available = self.bank_note_supply[bn]
            bank_notes_used[bn] = min(amount // bn, available)
            amount -= bn * bank_notes_used[bn]
        if amount > 0:
            return [-1]
        assert amount == 0
        for bn, bnc in bank_notes_used.items():
            self.bank_note_supply[bn] -= bnc
        result = []
        for bn in self.bank_notes:
            result.append(0 if bn not in bank_notes_used else bank_notes_used[bn])
        return result

# Your ATM object will be instantiated and called as such:
# obj = ATM()
# obj.deposit(banknotesCount)
# param_2 = obj.withdraw(amount)
# @lc code=end

def run_operations(ops, args):
    assert len(ops) == len(args)
    atm = None
    results = []
    for i in range(len(ops)):
        op = ops[i]
        if op == 'ATM':
            assert atm is None
            atm = ATM()
            results.append(None)
        else:
            assert atm is not None
            results.append(atm.__getattribute__(op)(*args[i]))
    return results

from test_utils import run_test

method = run_operations
run_test(method, args=[
    ["ATM", "deposit", "withdraw", "deposit", "withdraw", "withdraw"],
    [[], [[0,0,1,2,1]], [600], [[0,1,0,1,1]], [600], [550]]
], expected=[None, None, [0,0,1,0,1], None, [-1], [0,1,0,0,1]])