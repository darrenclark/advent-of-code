from collections import defaultdict

INPUT = 'input.txt'

with open(INPUT) as f:
    input = f.read()

grid = [list(l.strip()) for l in input.strip().split('\n')]

w = len(grid[0])
h = len(grid)

adj4 = [(-1,0), (1,0), (0,-1), (0,1)]

sx,sy = 0,0
ex,ey = 0,0

for y in range(h):
    for x in range(w):
        if grid[y][x] == 'S':
            sx,sy = x,y
        if grid[y][x] == 'E':
            ex,ey = x,y


g = defaultdict(list)
q = [(sx,sy)]
v = set()
while q:
    x,y = q.pop()
    if (x,y) in v:
        continue
    v.add((x,y))
    for dx,dy in adj4:
        nx = x+dx
        ny = y+dy
        if grid[ny][nx] != '#':
            q.append((nx,ny))
            g[(x,y)].append(((nx,ny), 1))

def dijkstra(graph, start):
    dist = defaultdict(lambda: float('inf'))
    dist[start] = 0
    uv = set(graph.keys())

    while uv:
        n = min(uv, key=lambda x: dist[x])
        uv.remove(n)
        d = dist[n]

        for (m, w) in graph[n]:
            if m in uv:
                dist[m] = min(dist[m], d+w)

    return dist

def to_path(graph, dist, start, end):
    p = [start]
    c = start
    md = 0

    while c != end:
        adj = [x[0] for x in graph[c] if dist[x[0]] > md]
        n = min(adj, key=lambda x: dist[x])
        p.append(n)
        md = dist[n]
        c = n

    return p

path = to_path(g, dijkstra(g, (sx,sy)), (sx,sy), (ex,ey))

idx = {n:i for (i,n) in enumerate(path)}

ans = 0
for cx,cy in path:
    c = idx[(cx,cy)]
    for dx,dy in adj4:
        nx = cx+dx*2
        ny = cy+dy*2
        if 0 <= nx < w and 0 <= ny < h and (nx,ny) in idx:
            n = idx[(nx,ny)]
            if n > c + 2:
                savings = n - c - 2
                if savings >= 100:
                    ans += 1

print('Part 1:', ans)

ans = 0
for cx,cy in path:
    c = idx[(cx,cy)]
    for nx,ny in idx:
        d = abs(nx - cx) + abs(ny - cy)
        if d <= 20:
            n = idx[(nx,ny)]
            if n > c + d:
                savings = n - c - d
                if savings >= 100:
                    ans += 1
print('Part 2:', ans)
