input = open('input.txt', 'r').read()

def part1():
    x, y = 0, 0

    presents = {}
    presents[(x, y)] = 1

    for c in input:
        if c == '<':
            x -= 1
        elif c == '^':
            y -= 1
        elif c == '>':
            x += 1
        elif c == 'v':
            y += 1
        else:
            continue

        presents[(x, y)] = presents.get((x, y), 0) + 1

    return len(presents)

print(f'Part 1: {part1()}')

def part2():
    x = [0, 0]
    y = [0, 0]

    presents = {}
    presents[(0, 0)] = 2

    for i, c in enumerate(input):
        if c == '<':
            x[i%2] -= 1
        elif c == '^':
            y[i%2] -= 1
        elif c == '>':
            x[i%2] += 1
        elif c == 'v':
            y[i%2] += 1
        else:
            continue

        presents[(x[i%2], y[i%2])] = presents.get((x[i%2], y[i%2]), 0) + 1

    return len(presents)

print(f'Part 2: {part2()}')
