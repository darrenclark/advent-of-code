INPUT = 'input.txt'

with open(INPUT) as f:
    input = f.read()

wire1, wire2 = input.strip().split('\n')

directions = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, -1),
    'D': (0, 1),
}

def to_segments(line):
    segments = []

    x,y = 0,0
    for p in line.split(','):
        dir = p[0]
        dist = int(p[1:])

        dx,dy = directions[dir]
        dx *= dist
        dy *= dist

        segments.append(((x,y), (x+dx, y+dy)))

        x += dx
        y += dy

    return segments

def intersection(s1, s2):
    s1h = s1[0][1] == s1[1][1]
    s2h = s2[0][1] == s2[1][1]

    if s1h == s2h:
        return None # parallel

    h = s1 if s1h else s2
    v = s1 if not s1h else s2


    if h[0][1] <= max(v[0][1], v[1][1]) and h[0][1] >= min(v[0][1], v[1][1]) and v[0][0] <= max(h[0][0], h[1][0]) and v[0][0] >= min(h[0][0], h[1][0]):

        return (v[0][0], h[0][1])
    return None

wire1 = to_segments(wire1)
wire2 = to_segments(wire2)


ii = []

for s1 in wire1:
    for s2 in wire2:
        i = intersection(s1, s2)
        if i and i != (0, 0):
            ii.append(i)

ans = min(abs(x)+abs(y) for x,y in ii)
print('Part 1:', ans)
