import intcode

INPUT = 'input.txt'

with open(INPUT) as f:
    prog = intcode.parse(f.read())

ic = intcode.Intcode(prog)
ic.input = [1]
ic.run()

tests = ic.output[:-1]
assert len(tests) > 0
assert sum(tests) == 0

diag_code = ic.output[-1]
print('Part 1:', diag_code)
