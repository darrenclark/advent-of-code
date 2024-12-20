import intcode

INPUT = 'input.txt'

with open(INPUT) as f:
    prog = intcode.parse(f.read())

prog[1] = 12
prog[2] = 2

ic = intcode.Intcode(prog)
ic.run()

print('Part 1:', ic.prog[0])
