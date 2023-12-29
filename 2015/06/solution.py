from dataclasses import dataclass
import re

input = open('input.txt', 'r').read()

@dataclass
class Instruction:
    action: str
    from_x: int
    from_y: int
    to_x: int
    to_y: int

    def apply(self, is_on):
        if self.action == 'toggle':
            return not is_on
        elif self.action == 'turn on':
            return True
        elif self.action == 'turn off':
            return False
        else: raise Exception()

    def brightness(self):
        if self.action == 'toggle':
            return 2
        elif self.action == 'turn on':
            return 1
        elif self.action == 'turn off':
            return -1
        else: raise Exception()

line_re = re.compile('(turn on|turn off|toggle) (\\d+),(\\d+) through (\\d+),(\\d+)')

def parse(line):
    m = line_re.match(line)
    if m is None: raise Exception()

    action = m.group(1)
    from_x = int(m.group(2))
    from_y = int(m.group(3))
    to_x = int(m.group(4))
    to_y = int(m.group(5))

    return Instruction(action=action,from_x=from_x,from_y=from_y,to_x=to_x,to_y=to_y)

parsed = [parse(line) for line in input.split('\n') if line != ""]

def part1():
    lights = [[False]*1000 for _ in range(0, 1000)]

    for i in parsed:
        for x in range(i.from_x, i.to_x + 1):
            for y in range(i.from_y, i.to_y + 1):
                lights[y][x] = i.apply(lights[y][x])

    lit = 0
    for row in lights:
        for light in row:
            if light:
                lit += 1

    return lit

print(f'Part 1: {part1()}')

def part2():
    lights = [[0]*1000 for _ in range(0, 1000)]

    for i in parsed:
        for x in range(i.from_x, i.to_x + 1):
            for y in range(i.from_y, i.to_y + 1):
                lights[y][x] += i.brightness()
                lights[y][x] = max(lights[y][x], 0)

    brightness = 0
    for row in lights:
        for light in row:
            brightness += light

    return brightness

print(f'Part 2: {part2()}')
