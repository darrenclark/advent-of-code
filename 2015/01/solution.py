input = open('input.txt').read()

def part1():
    return input.count('(') - input.count(')')

print(f"Part 1: {part1()}")

def part2():
    floor = 0
    for i,v in enumerate(input):
        if v == '(':
            floor += 1
        elif v == ')':
            floor -= 1

        if floor == -1:
            return i + 1

print(f"Part 2: {part2()}")
