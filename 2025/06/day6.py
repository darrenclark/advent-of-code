INPUT = 'input.txt'

with open(INPUT) as f:
    input_raw = f.read()

def part1():
    input = [l.split() for l in input_raw.strip().splitlines()]

    pt1 = 0

    for i in range(len(input[0])):
        acc = int(input[0][i])
        op = (lambda a, b: a + b) if input[len(input)-1][i] == '+' else (lambda a, b: a * b)
        for j in range(len(input) - 2):
            acc = op(acc, int(input[j+1][i]))
        pt1 += acc

    print(pt1)

part1()

def part2():
    input = input_raw.splitlines()

    pt2 = 0

    max_x = len(input[0])
    max_y = len(input)

    terms = []
    op = lambda a, b: a + b
    for x in range(max_x):
        is_sep = all(" " == input[y][x] for y in range(max_y))
        if is_sep:
            if terms:
                acc = terms[0]
                for t in terms[1:]:
                    acc = op(acc, t)
                pt2 += acc
            terms = []
        else:
            t = ""
            for y in range(max_y):
                if input[y][x] == "*":
                    op = (lambda a, b: a * b)
                elif input[y][x] == "+":
                    op = (lambda a, b: a + b)
                elif input[y][x] != " ":
                    t += input[y][x]
            if t:
                terms.append(int(t))

    if terms:
        acc = terms[0]
        for t in terms[1:]:
            acc = op(acc, t)
        pt2 += acc

    print(pt2)



part2()
