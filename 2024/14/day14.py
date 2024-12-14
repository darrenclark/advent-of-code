import re
from collections import defaultdict
import itertools

#INPUT = 'sample_input.txt'
#WIDTH = 11
#HEIGHT = 7

INPUT = 'input.txt'
WIDTH = 101
HEIGHT = 103

robots = []

with open(INPUT) as f:
    for l in f.readlines():
        [px, py, dx, dy] = re.findall(r'-?\d+', l)
        robots.append( ((int(px), int(py)), (int(dx), int(dy))) )

def simulate(r, n):
    ((px, py), (dx, dy)) = r
    px = (px + dx * n) % WIDTH
    py = (py + dy * n) % HEIGHT
    return (px, py)

f = [simulate(r, 100) for r in robots]

def cmp(a, b):
    return (a > b) - (a < b) 

q = defaultdict(int)
for (px, py) in f:
    cx = cmp(px, WIDTH//2)
    cy = cmp(py, HEIGHT//2)
    if cx == 0 or cy == 0:
        continue
    q[(cx, cy)] += 1

s = 1
for v in q.values():
    s *= v

print('Part 1: ', s)

# Determined by via commented code out below
print('Part 2: ', 6446)

#for i in itertools.count(start=0):
#    f = set([simulate(r, i) for r in robots])
#
#    s = ""
#    p = False
#
#    for y in range(HEIGHT):
#        c = 0
#        for x in range(WIDTH):
#            if (x, y) in f:
#                s += '#'
#                c += 1
#            else:
#                s += '.'
#        s += '\n'
#        if c > 30:
#            p = True
#
#    if not p:
#        continue
#
#    print("===== ", i, " =====")
#    print(s)
