from collections import defaultdict

INPUT = 'input.txt'
with open(INPUT) as f:
    input = f.read().strip().split('\n')


def to_graph(keypad_string):
    grid = keypad_string.strip().split('\n')
    w = len(grid[0])
    h = len(grid)

    g = defaultdict(list)
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            k1 = grid[y][x]
            if k1 != '.':
                for dx,dy in [(0,-1),(0,1),(-1,0),(1,0)]:
                    nx,ny = x+dx,y+dy
                    if 0 <= nx < w and 0 <= ny < h and grid[ny][nx] != '.':
                        k2 = grid[ny][nx]
                        g[k1].append(k2)
    return g

num_keypad_graph = to_graph('''
789
456
123
.0A
''')

dir_keypad_graph = to_graph('''
.^A
<v>
''')


def dijkstra(graph, start):
    dist = defaultdict(lambda: float('inf'))
    dist[start] = 0
    uv = set(graph.keys())

    while uv:
        n = min(uv, key=lambda x: dist[x])
        uv.remove(n)
        d = dist[n]

        for m in graph[n]:
            if m in uv:
                dist[m] = min(dist[m], d+1)

    return dist

num_keypad = {k: dict(dijkstra(num_keypad_graph, k)) for k in num_keypad_graph}
dir_keypad = {k: dict(dijkstra(dir_keypad_graph, k)) for k in dir_keypad_graph}

print(num_keypad)
print(dir_keypad)
