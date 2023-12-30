from dataclasses import dataclass
from functools import cache

input = open('input.txt', 'r').read()

@dataclass
class Wiring:
    op: str | None
    src_a: int | str
    src_b: int | str | None
    dest: str

def parse(line):
    def wire_or_value(s):
        try:
            return int(s)
        except ValueError:
            return s

    split = line.split(' ')
    if len(split) == 3:
        # ... -> ...
        return Wiring(op=None, src_a=wire_or_value(split[0]), src_b=None, dest=split[2])
    elif len(split) == 4:
        # NOT ... -> ...
        return Wiring(op=split[0], src_a=wire_or_value(split[1]), src_b=None, dest=split[3])
    elif len(split) == 5:
        # ... AND ... -> ...
        return Wiring(op=split[1], src_a=wire_or_value(split[0]), src_b=wire_or_value(split[2]), dest=split[4])
    else:
        raise Exception()

parsed_lines = [parse(line) for line in input.split('\n') if line != ""]
parsed = dict(map(lambda w: (w.dest, w), parsed_lines))

def part1():
    @cache
    def get_value(w):
        if type(w) == int:
            return w

        wiring = parsed[w]

        if wiring.op == None:
            return get_value(wiring.src_a)
        elif wiring.op == 'NOT':
            return ~get_value(wiring.src_a)
        elif wiring.op == 'AND':
            return get_value(wiring.src_a) & get_value(wiring.src_b)
        elif wiring.op == 'OR':
            return get_value(wiring.src_a) | get_value(wiring.src_b)
        elif wiring.op == 'RSHIFT':
            return get_value(wiring.src_a) >> get_value(wiring.src_b)
        elif wiring.op == 'LSHIFT':
            return get_value(wiring.src_a) << get_value(wiring.src_b)
        else: raise Exception()

    return get_value('a') & 0xffff

part_1_result = part1()
print(f'Part 1: {part_1_result}')

def part2(part_1_result):
    parsed['b'] = Wiring(op=None, src_a=part_1_result, src_b=None, dest='b')

    @cache
    def get_value(w):
        if type(w) == int:
            return w

        wiring = parsed[w]

        if wiring.op == None:
            return get_value(wiring.src_a)
        elif wiring.op == 'NOT':
            return ~get_value(wiring.src_a)
        elif wiring.op == 'AND':
            return get_value(wiring.src_a) & get_value(wiring.src_b)
        elif wiring.op == 'OR':
            return get_value(wiring.src_a) | get_value(wiring.src_b)
        elif wiring.op == 'RSHIFT':
            return get_value(wiring.src_a) >> get_value(wiring.src_b)
        elif wiring.op == 'LSHIFT':
            return get_value(wiring.src_a) << get_value(wiring.src_b)
        else: raise Exception()

    return get_value('a') & 0xffff

print(f'Part 2: {part2(part_1_result)}')
