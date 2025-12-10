INPUT = 'sample_input.txt'

with open(INPUT) as f:
    def to_xy(line):
        x, y = line.split(',')
        return (int(x), int(y))

    input = [to_xy(l) for l in f.read().splitlines()]

def area(a, b):
    ax, ay = a
    bx, by = b

    return (abs(ax - bx) + 1) * (abs(ay - by) + 1)

pt1 = max(area(a, b) for i, a in enumerate(input) for b in input[i+1:])

print("Part 1:" , pt1)

def pt2_valid(a, b):
    ax, ay = a
    bx, by = b

    # 
