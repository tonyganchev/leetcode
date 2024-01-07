from test_utils import run_test


rcount = 0


class Block:
    def __init__(self, letter, size):
        self.letter = letter
        self.length = size

    def __repr__(self):
        return f"{self.letter}{self.length}"


class SplitBlock:
    def __init__(self, from_idx, from_block, from_block_idx, to_idx, to_block, to_block_idx):
        self.from_idx = from_idx
        self.from_block = from_block
        self.from_block_idx = from_block_idx
        self.to_idx = to_idx
        self.to_block = to_block
        self.to_block_idx = to_block_idx
        self.merged_length = to_idx - from_idx
        self.gap = self.merged_length - from_block.length - to_block.length

    @property
    def letter(self):
        return self.from_block.letter

    def __repr__(self):
        return f'{self.from_idx}|{self.from_block}|-{self.gap}-|{self.to_block}|{self.to_idx}'


class LetterOccurrence:
    def __init__(self, block, idx, block_idx):
        self.block = block
        self.index = idx
        self.block_idx = block_idx


class BlockList:
    @classmethod
    def from_string(cls, s):
        bl = BlockList()
        bl.blocks = BlockList._blocks_from_string(s)
        bl.length = len(s)
        bl._reindex()
        return bl

    @classmethod
    def _blocks_from_string(cls, s):
        blocks = []
        block_start = 0
        for i in range(1, len(s)):
            if s[i] != s[block_start]:
                blocks.append(Block(s[block_start], i - block_start))
                block_start = i
        blocks.append(Block(s[block_start], len(s) - block_start))
        return blocks

    def __init__(self):
        self.blocks = []
        self.length = 0

    def __repr__(self):
        return repr(self.blocks) + f':{self.length}'

    def __hash__(self):
        return hash(repr(self))

    def shoot(self, from_block_idx, to_block_idx):
        bl = BlockList()
        bl.length = self.length - \
            sum(b.length for b in self.blocks[from_block_idx: to_block_idx])
        if from_block_idx == 0:
            bl.blocks = self.blocks[to_block_idx:]
        elif to_block_idx == len(self.blocks):
            bl.blocks = self.blocks[: from_block_idx]
        else:
            bl.blocks = self.blocks[: from_block_idx]
            if to_block_idx < len(self.blocks):
                if self.blocks[to_block_idx].letter == bl.blocks[-1].letter:
                    bl.blocks[-1] = Block(
                        bl.blocks[-1].letter,
                        bl.blocks[-1].length +
                        self.blocks[to_block_idx].length,
                    )
                else:
                    bl.blocks.append(self.blocks[to_block_idx])
            bl.blocks.extend(self.blocks[to_block_idx + 1:])
        bl._reindex()
        return bl

    def _reindex(self):
        self.block_lengths = self._block_lengths_map()
        self.block_lengths_desc = sorted(
            [k for k in self.block_lengths.keys()], reverse=True)
        self.max_no_splits = self._max_no_splits()
        self.splits = self._splits()

    def _block_lengths_map(self):
        block_lengths = {}
        for b in self.blocks:
            block_lengths.setdefault(b.length, 0)
            block_lengths[b.length] += 1
        return block_lengths

    def _max_no_splits(self):
        max_no_splits = 0
        remaining_blocks = 3
        for l in self.block_lengths_desc:
            change = min(self.block_lengths[l], remaining_blocks)
            max_no_splits += change * l
            remaining_blocks -= change
            if remaining_blocks == 0:
                break
        return max_no_splits

    def _splits(self):
        splits = []
        previous_occurrences = {}
        idx = 0
        for i, b in enumerate(self.blocks):
            previous_occurrences.setdefault(b.letter, [])
            for po in previous_occurrences[b.letter]:
                splits.append(SplitBlock(
                    po.index, po.block, po.block_idx, idx + b.length, b, i))
            previous_occurrences[b.letter].append(LetterOccurrence(b, idx, i))
            idx += b.length
        return splits


# @cache
def solve(block_list: BlockList, best: int = 1) -> int:
    global rcount
    # print(block_list, best)
    if len(block_list.splits) == 0:
        return max(best, block_list.max_no_splits)
    # else:
    #     print(block_list.splits)
    if len(block_list.blocks) <= 3:
        return max(best, block_list.length)
    if block_list.length <= best:
        return best

    for split in block_list.splits:
        # print(split)
        rcount += 1
        best = max(best, solve(block_list.shoot(split.from_block_idx + 1, split.to_block_idx), best))
        # for i in range(split.from_block_idx + 1, split.to_block_idx):
        #     best = max(best, solve(block_list.shoot(i, i + 1), best))
    return best


def solution(s):
    global rcount
    rcount = 0
    block_list = BlockList.from_string(s)
    # print(block_list.block_lengths)
    r = solve(block_list)
    # print(rcount)
    return r


method = solution


run_test(method, ('aaa',), 3)
run_test(method, ('aabb',), 4)
run_test(method, ('aba',), 3)
run_test(method, ("aabacbba",), 6)
run_test(method, ('aabxbaba',), 6)
run_test(method, ('xxxyxxyyyxyyy',), 11)
run_test(method, ('aaaaaabbbccccaaaaa',), 15)
run_test(method, ('aabbccddeeffgghh',), 6)
run_test(method, ('aabbccddeeffgghhii',), 6)
run_test(method, ('aabbccddeeffgghhiijj',), 6)
run_test(method, ('aabbccddeeffgghhiijjkk',), 6)
run_test(method, ('abcdefghijklm',), 3)
run_test(method, ('abcdefghijklmnopqrs',), 3)
run_test(method, ('abcdefghijklmnopqrstuvwxyz',), 3)
run_test(method, ('abadefghijk',), 4)
run_test(method, ('yriyaefxumrrdlivhhqc',), 6)
run_test(method, ('iofcmqnklvxozbrnxuscnrqcimzrwb',), 6)
run_test(method, ('jqvazcxyvlpxwxtvohtbpiqtkjvbnaiwigjlfksu',), 8)
run_test(method, ('hcurymglpwseemozpcwhzbuzmvcrdqwlmwejmynhxvjig',),7)
run_test(method, ('qlyygouyruievxakbkvgpigxhmrsjuxahgrdbwestrprj',),9)
run_test(method, ('atdakkgmkjqlvlycmxfpgnwalqdlomlwfgocuaglfitagu',),11)
run_test(method, ('hcurymglpwseemozpcwhzbuzmvcrdqwlmwejmynhxvjig',),7)
# run_test(method, ('abadefghijklmnopqraaaawxyz',), 8)
import random
import string
run_test(method, (''.join(random.choices(string.ascii_lowercase, k = 47)),), 3)
# run_test(method, (''.join(random.choices(string.ascii_lowercase, k = 200)),), 3)
# run_test(method, (''.join(random.choices(string.ascii_lowercase, k = 2000)),), 3)
# run_test(method, (''.join(random.choices(string.ascii_lowercase, k = 20000)),), 3)
# run_test(method, (''.join(random.choices(string.ascii_lowercase, k = 200000)),), 3)