from collections import defaultdict
import heapq
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
        graph[(x-1,y, 'W')].append(((x,y, 'W'), 1))
        add_edges(x-1,y)
    if grid[y][x+1] != '#':
        graph[(x,y, 'E')].append(((x+1,y, 'E'), 1))
        graph[(x+1,y, 'E')].append(((x,y, 'E'), 1))
        add_edges(x+1,y)
    if grid[y-1][x] != '#':
        graph[(x,y, 'N')].append(((x,y-1, 'N'), 1))
        graph[(x,y-1, 'N')].append(((x,y, 'N'), 1))
        add_edges(x,y-1)
    if grid[y+1][x] != '#':
        graph[(x,y, 'S')].append(((x,y+1, 'S'), 1))
        graph[(x,y+1, 'S')].append(((x,y, 'S'), 1))
        add_edges(x,y+1)

add_edges(sx,sy)


def dijkstra(graph, start):
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    q = [(0, start)]

    while q:
        d,n = heapq.heappop(q)

        if d > dist[n]:
            continue

        for m, w in graph[n]:
            md = d+w
            if md < dist[m]:
                dist[m] = md
                heapq.heappush(q, (md, m))

    return dist



start_node = (sx,sy,'E')
# visibly inspecting graph in my input, the N node will always be the only one on the shortest path
end_node = (ex,ey,'N')
dist = dijkstra(graph, (sx,sy,'E'))

print('Part 1: ', dist[end_node])

s = set([(ex,ey)])
seen = set()
def dfs(n):
    if n in seen:
        return
    seen.add(n)
    for m,w in graph[n]:
        if dist[n] - dist[m] == w:
            s.add((m[0],m[1]))
            dfs(m)
dfs(end_node)
print('Part 2: ', len(s))
