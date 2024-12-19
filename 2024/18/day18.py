from collections import defaultdict
import sys
import math

sys.setrecursionlimit(100000)

INPUT = 'input.txt'
GRID_W = 71
N_COORDS = 1024

#INPUT = 'sample_input.txt'
#GRID_W = 7
#N_COORDS = 12

GRID_H = GRID_W

sx,sy = 0,0
ex,ey = GRID_W-1,GRID_H-1

with open(INPUT) as f:
    def to_coord(l):
        x, y = l.split(',')
        return (int(x), int(y))

    coords = [to_coord(l) for l in f.readlines()]

def make_grid(coords):
    grid = [['.' for _ in range(GRID_W)] for _ in range(GRID_H)]
    for (x, y) in coords:
        grid[y][x] = '#'

    return grid


def run(grid):
    graph = defaultdict(list)
    v = set()
    def add_edges(x, y):
        if (x, y) in v:
            return
        v.add((x, y))

        if x > 0 and grid[y][x-1] != '#':
            graph[(x, y)].append(((x-1, y), 1))
            add_edges(x-1, y)
        if x < GRID_W-1 and grid[y][x+1] != '#':
            graph[(x, y)].append(((x+1, y), 1))
            add_edges(x+1, y)
        if y > 0 and grid[y-1][x] != '#':
            graph[(x, y)].append(((x, y-1), 1))
            add_edges(x, y-1)
        if y < GRID_H-1 and grid[y+1][x] != '#':
            graph[(x, y)].append(((x, y+1), 1))
            add_edges(x, y+1)

    add_edges(sx, sy)

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


    dist = dijkstra(graph, (sx,sy))
    return dist[(ex,ey)]

print('Part 1:', run(make_grid(coords[:N_COORDS])))

low = N_COORDS
high = len(coords) - 1
mid = low

while low <= high:
    mid = (high + low) // 2

    fails = math.isinf(run(make_grid(coords[:mid+1])))
    if not fails:
        low = mid + 1
    else:
        fails = math.isinf(run(make_grid(coords[:mid])))
        if fails:
            high = mid
        else:
            # mid is the first failure
            break

x,y = coords[mid]
print(f"Part 2: {x},{y}")
