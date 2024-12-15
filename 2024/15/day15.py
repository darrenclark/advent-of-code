import copy

INPUT = 'input.txt'

with open(INPUT) as f:
    [grid_str, moves_str] = f.read().split('\n\n')
    grid = [list(line) for line in grid_str.split('\n')]
    moves = "".join(moves_str.split())


dirs = {
    '^': (0,-1),
    'v': (0,1),
    '<': (-1,0),
    '>': (1,0)
}

def part1(grid, moves):
    w = len(grid[0])
    h = len(grid)

    rx,ry = 0,0
    for y in range(h):
        for x in range(w):
            if grid[y][x] == '@':
                rx,ry = x,y
                break

    def push(x, y, dx, dy):
        c = grid[y][x]

        if grid[y+dy][x+dx] == '#':
            return False
        elif grid[y+dy][x+dx] == 'O':
            if push(x+dx, y+dy, dx, dy):
                grid[y+dy][x+dx] = c
                grid[y][x] = '.'
                return True
            return False
        elif grid[y+dy][x+dx] == '.':
            grid[y+dy][x+dx] = c
            grid[y][x] = '.'
            return True
        else:
            raise RuntimeError('unexpected character')

    for m in moves:
        dx,dy = dirs[m]
        if push(rx, ry, dx, dy):
            rx += dx
            ry += dy

    #for line in grid:
    #   print("".join(line))

    ans = 0
    for y in range(h):
        for x in range(w):
            if grid[y][x] == 'O':
                ans += x + y * 100

    print('Part 1:', ans)

part1(copy.deepcopy(grid), moves)

def part2(orig_grid, moves):
    grid = []
    for line in orig_grid:
        row = []
        for c in line:
            if c == '#':
                row.extend(['#', '#'])
            elif c == 'O':
                row.extend(['[', ']'])
            elif c == '@':
                row.extend(['@', '.'])
            elif c == '.':
                row.extend(['.', '.'])
            else:
                raise RuntimeError('unexpected character')
        grid.append(row)

    #for line in grid:
    #    print("".join(line))

    w = len(grid[0])
    h = len(grid)

    rx,ry = 0,0
    for y in range(h):
        for x in range(w):
            if grid[y][x] == '@':
                rx,ry = x,y
                break

    def can_push(x, y, m):
        dx,dy = dirs[m]

        if grid[y+dy][x+dx] == '#':
            return False
        elif grid[y+dy][x+dx] == '.':
            return True
        elif grid[y+dy][x+dx] == '[':
            if m == '^' or m == 'v':
                return can_push(x+dx, y+dy, m) and can_push(x+dx+1, y+dy, m)
            elif m == '<':
                return can_push(x+dx, y+dy, m)
            elif m == '>':
                return can_push(x+dx+1, y+dy, m)  # can we move adjacent ] to the right?
        elif grid[y+dy][x+dx] == ']':
            if m == '^' or m == 'v':
                return can_push(x+dx, y+dy, m) and can_push(x+dx-1, y+dy, m)
            elif m == '<':
                return can_push(x+dx-1, y+dy, m) # can we move adjacent [ to the left?
            elif m == '>':
                return can_push(x+dx, y+dy, m)
        else:
            raise RuntimeError('unexpected character')

    def push(x, y, m):
        dx,dy = dirs[m]
        c = grid[y][x]

        if c == '.':
            return
        elif c == '#':
            raise RuntimeError('unexpected wall')
        elif c == '@':
            push(x+dx, y+dy, m)
            grid[y+dy][x+dx] = c
            grid[y][x] = '.'
        elif c == '[':
            if m == '^' or m == 'v':
                push(x+dx, y+dy, m)
                grid[y+dy][x+dx] = c
                grid[y][x] = '.'

                push(x+dx+1, y+dy, m)
                grid[y+dy][x+dx+1] = ']'
                grid[y][x+1] = '.'
            elif m == '<':
                push(x+dx, y+dy, m)
                grid[y+dy][x+dx] = c
                grid[y][x] = ']'
                grid[y][x+1] = '.'
            elif m == '>':
                push(x+dx+1, y+dy, m)
                grid[y+dy][x+dx] = '['
                grid[y+dy][x+dx+1] = ']'
                grid[y][x] = '.'
        elif c == ']':
            if m == '^' or m == 'v':
                push(x+dx, y+dy, m)
                grid[y+dy][x+dx] = c
                grid[y][x] = '.'

                push(x+dx-1, y+dy, m)
                grid[y+dy][x+dx-1] = '['
                grid[y][x-1] = '.'
            elif m == '<':
                push(x+dx-1, y+dy, m)
                grid[y+dy][x+dx] = ']'
                grid[y+dy][x+dx-1] = '['
                grid[y][x] = '.'
            elif m == '>':
                push(x+dx, y+dy, m)
                grid[y+dy][x+dx] = c
                grid[y][x] = '['
                grid[y][x-1] = '.'
        else:
            raise RuntimeError('unexpected character')

    for m in moves:
        dx,dy = dirs[m]
        if can_push(rx, ry, m):
            push(rx, ry, m)
            rx += dx
            ry += dy

        #for line in grid:
        #   print("".join(line))

    ans = 0
    for y in range(h):
        for x in range(w):
            if grid[y][x] == '[':
                ans += x + y * 100

    print('Part 2:', ans)



part2(copy.deepcopy(grid), moves)
