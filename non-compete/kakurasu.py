from typing import List

def variants_from_to(f: int, n: int) -> List[int]:
    if f > n:
        return [[]]
    else:
        sx = variants_from_to(f + 1, n)
        r = []
        for v in sx:
            r.append([0] + v)
            r.append([f] + v)
        return r


def filter_variant(mask, s, v):
    if sum(v) != s:
        return False
    for i, n in enumerate(v):
        if mask[i] == 0 and n != 0:
            return False
        if mask[i] == 1 and n == 0:
            return False
    return True

vs = variants_from_to(1, 8)

def fltr(v):
    return filter_variant([1, -1, -1, -1, -1, -1, 0, 0], 18, v)

vs = filter(fltr, vs)

for v in vs:
    print(str(v) + " = " + str(sum(v)))
