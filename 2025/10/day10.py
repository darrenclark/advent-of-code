# /// script
# dependencies = [
#   "python-constraint==1.4.0",
# ]
# ///

from constraint import Problem

INPUT = 'input.txt'

with open(INPUT) as f:
    def parse_line(l):
        lights = []
        buttons = []
        joltage = []

        for p in l.strip().split():
            if p[0] == '[':
                for c in p[1:-1]:
                    lights.append(int(c == '#'))
            elif p[0] == '(':
                b = []
                for c in p[1:-1].split(','):
                    b.append(int(c))
                buttons.append(b)
            elif p[0] == '{':
                for c in p[1:-1].split(','):
                    joltage.append(int(c))

        return lights, buttons, joltage


    input = [parse_line(l) for l in f.read().splitlines()]

def solve(lights, buttons):
    p = Problem()
    vars = [f'b{i}' for i in range(len(buttons))]
    p.addVariables(vars, range(0, 2))

    for i, l in enumerate(lights):
        v = [f'b{j}' for j in range(len(buttons)) if i in buttons[j]]
        def c(*args, light=l):
            return sum(args) % 2 == light
        p.addConstraint(c, v)

    return min(sum(s.values()) for s in p.getSolutions())

def part1():
    acc = 0
    for lights, buttons, joltage in input:
        acc += solve(lights, buttons)
    print('part 1:', acc)

part1()
