import re

INPUT = 'input.txt'

with open(INPUT) as f:
    input = f.read()

regex = re.compile('mul\\((\\d{1,3}),(\\d{1,3})\\)')

t = sum(int(a) * int(b) for (a, b) in regex.findall(input))
print("Part 1: ", t)


regex_pt2 = re.compile('mul\\((\\d{1,3}),(\\d{1,3})\\)|do\\(\\)|don' + "'" + 't\\(\\)')

t2 = 0
enabled = True

for m in regex_pt2.finditer(input):
    if m.group(0) == "do()":
        enabled = True
    elif m.group(0) == "don't()":
        enabled = False
    elif enabled:
        t2 += int(m.group(1)) * int(m.group(2))

print("Part 2: ", t2)
