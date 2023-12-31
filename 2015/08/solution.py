input = open('input.txt', 'r').read()

def parse(line):
    return (line, eval(line))

parsed = [parse(line) for line in input.split('\n') if line != ""]

def part1():
    in_code = sum([len(x[0]) for x in parsed])
    in_mem = sum([len(x[1]) for x in parsed])
    return in_code - in_mem

print(f'Part 1: {part1()}')

def part2():
    def encode(s):
        out = ""
        for c in s:
            if c in "\\\"":
                out += "\\" + c
            else:
                out += c

        return "\"" + out + "\""

    encoded = sum([len(encode(x[0])) for x in parsed])
    in_code = sum([len(x[0]) for x in parsed])
    return encoded - in_code

print(f'Part 2: {part2()}')
