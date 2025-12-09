import math

INPUT = 'input.txt'
PT1_PAIRS = 1000  # 1000 for input, 10 for sample_input

with open(INPUT) as f:
    def to_xyz(r):
        return tuple(map(int, r.split(',')))

    input = [to_xyz(r) for r in f.read().splitlines()]


def dist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)

def normalize_key(a, b):
    return (a, b) if a < b else (b, a)

def sorted_distances():
    ds = {}

    for i in range(len(input)):
        for j in range(i+1, len(input)):
            d = dist(input[i], input[j])
            key = normalize_key(input[i], input[j])
            ds[key] = d

    sd = list(ds.items())
    sd.sort(key=lambda x: x[1])

    return sd

sd = sorted_distances()


pt2c = {}
cs = set()
c = 1
remaining = set(input)

def add_to_cluster(a, b):
    global c

    if a not in pt2c and b not in pt2c:
        pt2c[a] = c
        pt2c[b] = c
        cs.add(c)
        c += 1
    elif a in pt2c and b not in pt2c:
        pt2c[b] = pt2c[a]
    elif b in pt2c and a not in pt2c:
        pt2c[a] = pt2c[b]
    elif pt2c[a] != pt2c[b]:
        # merge 2 clusters
        new_c = pt2c[a]
        old_c = pt2c[b]
        for k2, v2 in list(pt2c.items()):
            if v2 == old_c:
                pt2c[k2] = new_c
        cs.remove(old_c)

    remaining.discard(a)
    remaining.discard(b)

for k, v in sd[:PT1_PAIRS]:
    a, b = k
    add_to_cluster(a, b)

def top_cluster_sizes(pt2c, top_n):
    sizes = {}
    for k, v in pt2c.items():
        if v not in sizes:
            sizes[v] = 0
        sizes[v] = sizes[v] + 1

    sorted_sizes = list(sizes.values())
    sorted_sizes.sort(reverse=True)

    return sorted_sizes[:top_n]


def product(xs):
    acc = 1
    for x in xs:
        acc = acc * x
    return acc

print("Part 1:", product(top_cluster_sizes(pt2c, top_n=3)))

for k, v in sd[PT1_PAIRS:]:
    a, b = k
    add_to_cluster(a, b)

    if not remaining:
        print('Part 2:', a[0] * b[0])
        break
