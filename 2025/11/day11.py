from functools import cache

INPUT = 'input.txt'

with open(INPUT) as f:
    def parse_line(l):
        a, b = l.split(':')

        return a, b.strip().split()

    input = dict(parse_line(l) for l in f.read().splitlines())

def count_paths(a):
    if a == 'out':
        return 1
    else:
        return sum(count_paths(b) for b in input[a])

print("part 1:", count_paths('you'))

@cache
def count_paths_pt2(a, dac, fft):
    if a == 'out':
        if dac and fft:
            return 1
        else:
            return 0
    else:
        return sum(count_paths_pt2(b, dac or a == "dac", fft or a == "fft") for b in input[a])

print('Part 2:', count_paths_pt2('svr', False, False))
