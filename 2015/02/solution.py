input = open('input.txt', 'r').read()

def parse(line):
    return tuple(map(int, line.split('x')))

parsed = [parse(line) for line in input.split('\n') if line != ""]

def part1():
    def paper(lwh):
        (l, w, h) = lwh

        lw = l * w
        hw = h * w
        lh = l * h

        return min(lw, hw, lh) + 2 * lw + 2 * hw + 2 * lh

    return sum(map(paper, parsed))

print(f'Part 1: {part1()}')

def part2():
    def ribbon(lwh):
        (l, w, h) = lwh

        smallest_perimeter = min(2 * l + 2 * w, 2 * h + 2 * w, 2 * l + 2 * h)
        bow = l * w * h

        return smallest_perimeter + bow

    return sum(map(ribbon, parsed))

print(f'Part 2: {part2()}')
