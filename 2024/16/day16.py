from collections import defaultdict
import sys

sys.setrecursionlimit(100000)

INPUT = 'input.txt'

with open(INPUT) as f:
    grid = [list(l.strip()) for l in f.readlines()]

w = len(grid[0])
h = len(grid)

sx,sy = 0,0
ex,ey = 0,0

for y in range(h):
    for x in range(w):
        if grid[y][x] == 'S':
            sx,sy = x,y
        if grid[y][x] == 'E':
            ex,ey = x,y

for row in grid:
    print("".join(row))

graph = defaultdict(list)

v = set()
def add_edges(x,y):
    if (x,y) in v:
        return

    v.add((x,y))

    graph[(x,y, 'W')].append(((x,y, 'N'), 1000))
    graph[(x,y, 'W')].append(((x,y, 'S'), 1000))

    graph[(x,y, 'E')].append(((x,y, 'N'), 1000))
    graph[(x,y, 'E')].append(((x,y, 'S'), 1000))

    graph[(x,y, 'N')].append(((x,y, 'E'), 1000))
    graph[(x,y, 'N')].append(((x,y, 'W'), 1000))

    graph[(x,y, 'S')].append(((x,y, 'E'), 1000))
    graph[(x,y, 'S')].append(((x,y, 'W'), 1000))

    if grid[y][x-1] != '#':
        graph[(x,y, 'W')].append(((x-1,y, 'W'), 1))
        add_edges(x-1,y)
    if grid[y][x+1] != '#':
        graph[(x,y, 'E')].append(((x+1,y, 'E'), 1))
        add_edges(x+1,y)
    if grid[y-1][x] != '#':
        graph[(x,y, 'N')].append(((x,y-1, 'N'), 1))
        add_edges(x,y-1)
    if grid[y+1][x] != '#':
        graph[(x,y, 'S')].append(((x,y+1, 'S'), 1))
        add_edges(x,y+1)

add_edges(sx,sy)


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


dist = dijkstra(graph, (sx,sy,'E'))

ans = min(
    dist[(ex,ey,'E')],
    dist[(ex,ey,'W')],
    dist[(ex,ey,'N')],
    dist[(ex,ey,'S')],
)
print('Part 1: ', ans)
