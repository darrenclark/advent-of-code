INPUT = 'input.txt'

with open(INPUT) as f:
    r, i = f.read().strip().split('\n\n')

    rr = [tuple(map(int, line.split('-'))) for line in r.splitlines()]
    ii = [int(line) for line in i.splitlines()]

def in_range(i, r):
    return r[0] <= i <= r[1]

pt1 = sum(1 for i in ii if any(in_range(i, r) for r in rr))
print("Part 1:" , pt1)

rs = sorted(rr, key=lambda x: x[0])

i = 0
while i < len(rs) - 1:
    a = rs[i]
    b = rs[i + 1]

    if a[1] < b[0]:
        # no overlap with next
        i += 1
        continue
    elif a[1] >= b[0]:
        rs[i] = (a[0], max(a[1], b[1]))
        del rs[i + 1]
        continue

pt2 = sum(b - a + 1 for a, b in rs)
print("Part 2:" , pt2)
