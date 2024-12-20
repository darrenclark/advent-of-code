INPUT = 'input.txt'

with open(INPUT) as f:
    prog = list(int(i) for i in f.read().split(','))

def run(prog):
    ip = 0
    while True:
        op = prog[ip]
        arg1 = prog[ip+1]
        arg2 = prog[ip+2]
        arg3 = prog[ip+3]
        ip += 4

        match op:
            case 1:
                prog[arg3] = prog[arg1] + prog[arg2]
            case 2:
                prog[arg3] = prog[arg1] * prog[arg2]
            case 99:
                return prog
            case _:
                raise RuntimeError(f'Unexpected opcode: {op}')

prog[1] = 12
prog[2] = 2
print('Part 1:', run(prog)[0])
