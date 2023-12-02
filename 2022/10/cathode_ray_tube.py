import fileinput

CRT_WIDTH = 40
CRT_HEIGHT = 6

class CPU:
    cycle = 0
    x = 1
    signal_strengths = []
    crt = [['.'] * CRT_WIDTH for _ in range(0, CRT_HEIGHT)]

    def run_instruction(self, instruction: str):
        if instruction == 'noop':
            self.inc_cycle()
        elif instruction.startswith('addx'):
            [_, dx] = instruction.split(' ')
            dx = int(dx)
            self.inc_cycle()
            self.inc_cycle()
            self.x += dx

    def inc_cycle(self):
        self.cycle += 1
        if self.cycle == 20 or (self.cycle - 20) % 40 == 0:
            self.signal_strengths.append(self.cycle * self.x)

        crt_x = (self.cycle - 1) % CRT_WIDTH
        crt_y = (self.cycle - 1) // CRT_WIDTH

        if crt_x >= self.x - 1 and crt_x <= self.x + 1:
            self.crt[crt_y][crt_x] = '#'

    def sum_signal_strengths(self):
        return sum(self.signal_strengths)

    def print_crt(self):
        for row in self.crt:
            print(''.join(row))

cpu = CPU()

for line in fileinput.input():
    line = line.strip()
    if line != "":
        cpu.run_instruction(line)

print("Sum of signal strengths (part 1):", cpu.sum_signal_strengths())
print("CRT (part 2):")
cpu.print_crt()
