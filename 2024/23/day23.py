import sys
import functools
from collections import Counter, defaultdict
sys.setrecursionlimit(100000)

INPUT='input.txt'
with open(INPUT) as f:
    input = f.read()


conns = defaultdict(set)

for co in input.strip().split('\n'):
    a,b = co.split('-')
    conns[a].add(b)
    conns[b].add(a)

three_sets_with_t = set()
for a in conns:
    for b in conns[a]:
        for c in conns[b]:
            if c in conns[a]:
                if a.startswith('t') or b.startswith('t') or c.startswith('t'):
                    three_sets_with_t.add(tuple(sorted([a, b, c])))

print('Part 1:', len(three_sets_with_t))

@functools.cache
def search(l):
    best = l

    for a in conns:
        # only try new nodes
        if a in l: continue

        # see if new node 'a' is connected to all existing nodes 'l'
        connected = True
        for b in l:
            if b not in conns[a]:
                connected = False
                continue

        if connected:
            nl = tuple(sorted(list(l) + [a]))
            res = search(nl)
            if len(res) > len(best):
                best = res

    return best

print('Part 2:', ','.join(search(tuple())))
