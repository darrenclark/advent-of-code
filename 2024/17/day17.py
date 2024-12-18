import itertools

INPUT = 'input.txt'

a,b,c = 0,0,0
prog = []

with open(INPUT) as f:
    [reg_str, prog_str] = f.read().split('\n\n')
    regs = []
    for line in reg_str.split('\n'):
        regs.append(int(line.split()[-1]))
    a,b,c = regs

    prog = list(map(int, prog_str.split()[-1].split(',')))


def run(prog, a, b, c):
    def combo_operand(op):
        match op:
            case 0 | 1 | 2 | 3:
                return op
            case 4:
                return a
            case 5:
                return b
            case 6:
                return c
            case _:
                raise ValueError(f"Unknown operand {op}")

    ip = 0
    out = []
    while ip in range(len(prog)):
        match prog[ip]:
            case 0:
                num = a
                den = pow(2, combo_operand(prog[ip+1]))
                a = num // den
                ip += 2
            case 1:
                b = b ^ prog[ip+1]
                ip += 2
            case 2:
                b = combo_operand(prog[ip+1]) % 8
                ip += 2
            case 3:
                if a == 0:
                    ip += 2
                else:
                    ip = prog[ip+1]
            case 4:
                b = b ^ c
                ip += 2
            case 5:
                out.append(combo_operand(prog[ip+1]) % 8)
                ip += 2
            case 6:
                num = a
                den = pow(2, combo_operand(prog[ip+1]))
                b = num // den
                ip += 2
            case 7:
                num = a
                den = pow(2, combo_operand(prog[ip+1]))
                c = num // den
                ip += 2
    return out


out = run(prog, a, b, c)
print("Part 1: ", ",".join(map(str, out)))

# 7 LSB determine output of program (for my input at least)
#
# start at back of program, and try adding 3 bits until we
# get to 

def search(n, pa):
    if n >= len(prog):
        return pa

    to_search = range(pow(2, 3))
    if n == 0:
        # last digit is a special case, we're only trying 1 bit
        to_search = [0, 1]

    for x in to_search:
        r1 = run(prog, (pa << 3) | x, b, c)
        if r1[0] == prog[-n-1]:
            r2 = search(n+1, pa << 3 | x)
            if r2 is not None:
                return r2

    return None

pt2_a = search(0, 0)
assert prog == run(prog, pt2_a, b, c)

print("Part 2: ", pt2_a)
