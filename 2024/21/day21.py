import typing
import functools

INPUT = 'input.txt'
with open(INPUT) as f:
    input = f.read()

codes = input.strip().split('\n')

KEYPAD = {
    '7': (0, 0),
    '8': (1, 0),
    '9': (2, 0),
    '4': (0, 1),
    '5': (1, 1),
    '6': (2, 1),
    '1': (0, 2),
    '2': (1, 2),
    '3': (2, 2),
    '0': (1, 3),
    'A': (2, 3),
}
KEYPAD_INV = {v:k for k,v in KEYPAD.items()}

DIRPAD = {
    '^': (1, 0),
    'A': (2, 0),
    '<': (0, 1),
    'v': (1, 1),
    '>': (2, 1),
}
DIRPAD_INV = {v:k for k,v in DIRPAD.items()}

@functools.cache
def paths(s, e, pad):
    if s == e:
        return [""]

    PAD = KEYPAD if pad == 'key' else DIRPAD
    PAD_INV = KEYPAD_INV if pad == 'key' else DIRPAD_INV

    sx,sy = PAD[s]
    ex,ey = PAD[e]

    dx = ex - sx
    dy = ey - sy

    if dy == 0:
        k = ">" if dx > 0 else "<"
        return [k * abs(dx)]
    elif dx == 0:
        k = "v" if dy > 0 else "^"
        return [k * abs(dy)]
    else:
        ndx = dx // abs(dx)
        ndy = dy // abs(dy)

        res = []

        # horizontal
        if (sx + ndx, sy) in PAD_INV:
            n = PAD_INV[(sx + ndx, sy)]
            k = ">" if dx > 0 else "<"
            for p in paths(n, e, pad):
                res.append(k + p)
        # vertical
        if (sx, sy + ndy) in PAD_INV:
            n = PAD_INV[(sx, sy + ndy)]
            k = "v" if dy > 0 else "^"
            for p in paths(n, e, pad):
                res.append(k + p)

        return res

def presses(w, pad):
    ps = ['']
    for c,n in zip('A' + w, w):
        p = paths(c, n, pad)
        nps = []
        for p2 in ps:
            for p3 in p:
                nps.append(p2 + p3 + 'A')
        ps = nps
    return ps

def shortest(c):
    ans = None
    for p in presses(c, 'key'):
        for p2 in presses(p, 'dir'):
            for p3 in presses(p2, 'dir'):
                ans = min(len(p3), ans) if ans is not None else len(p3)
    return typing.cast(int, ans)

def complexity(c):
    return shortest(c) * int(c[:-1])

ans = sum(complexity(c) for c in codes)
print('Part 1:', ans)
