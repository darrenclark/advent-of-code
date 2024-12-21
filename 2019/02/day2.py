import intcode

INPUT = 'input.txt'

with open(INPUT) as f:
    input_mem = intcode.parse(f.read())

mem = input_mem.copy()

mem[1] = 12
mem[2] = 2

ic = intcode.Intcode(mem)
ic.run()

print('Part 1:', ic.mem[0])

pt2a, pt2b = 0, 0
for a in range(100):
    for b in range(100):
        mem = input_mem.copy()
        mem[1] = a
        mem[2] = b
        ic = intcode.Intcode(mem)
        ic.run()
        if ic.mem[0] == 19690720:
            pt2a = a
            pt2b = b
            break

print('Part 2:', pt2a * 100 + pt2b)
