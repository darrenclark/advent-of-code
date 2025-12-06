INPUT = 'input.txt'

with open(INPUT) as f:
    input = [list(l.strip()) for l in f.read().strip().splitlines()]


adj = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

def to_remove(grid):
    for y in range(0, len(grid)):
        for x in range(0, len(grid[0])):
            if grid[y][x] != '@':
                continue

            a = 0
            for dy, dx in adj:
                ny, nx = y + dy, x + dx
                if ny < 0 or ny >= len(grid) or nx < 0 or nx >= len(grid[0]):
                    continue

                if grid[ny][nx] == '@':
                    a += 1
            if a < 4:
                yield (x, y)

print('Part 1', len(list(to_remove(input))))

pt2 = 0

while rm := list(to_remove(input)):
    pt2 += len(rm)
    for x, y in rm:
        input[y][x] = '.'

print('Part 2', pt2)
