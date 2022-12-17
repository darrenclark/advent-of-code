import fileinput


def parse_line(line):
    [a, b] = line.split(",")
    return [parse_range(a), parse_range(b)]

def parse_range(string):
    [lower, upper] = string.split("-")
    lower = int(lower)
    upper = int(upper)
    return range(lower, upper + 1)

def fully_contains(r1, r2):
    return r1.start <= r2.start and r2.stop <= r1.stop

def overlaps(r1, r2):
    return (r1.start <= r2.start < r1.stop) or (r2.start <= r1.start < r2.stop)

lines = [x.strip() for x in fileinput.input() if x != ""]

num_fully_contains = 0
num_overlapping = 0

for line in lines:
    [a, b] = parse_line(line)
    if fully_contains(a, b) or fully_contains(b, a):
        num_fully_contains += 1
    if overlaps(a, b):
        num_overlapping += 1

print("Fully containing count (part 1):", num_fully_contains)
print("Overlapping count (part 2):", num_overlapping)
