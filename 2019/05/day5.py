import intcode

INPUT = 'input.txt'

with open(INPUT) as f:
    mem = intcode.parse(f.read())

ic = intcode.Intcode(mem)
ic.input = [1]
ic.run()

tests = ic.output[:-1]
assert len(tests) > 0
assert sum(tests) == 0

diag_code = ic.output[-1]
print('Part 1:', diag_code)

ic = intcode.Intcode(mem)
ic.input = [5]
ic.run()
diag_code = ic.output[-1]
print('Part 2:', diag_code)
