import fileinput

def split_line(line):
    half_len = int(len(line)/2)
    first = line[0:half_len]
    second = line[half_len:]
    return [first, second]

def to_priority(ch):
    if "a" <= ch <= "z":
        return ord(ch) - ord('a') + 1
    elif "A" <= ch <= "Z":
        return ord(ch) - ord('A') + 27
    else:
        raise ValueError

def chunk_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

lines = [x.strip() for x in fileinput.input() if x != ""]

sum_priorities = 0

for line in lines:
    [first, second] = split_line(line)
    common = set(first).intersection(set(second))
    for ch in common:
        sum_priorities += to_priority(ch)

print("Sum priorities (part 1):", sum_priorities)

sum_priorities = 0

for group in chunk_list(lines, 3):
    common = set(group[0]).intersection(set(group[1])).intersection(set(group[2]))
    for ch in common:
        sum_priorities += to_priority(ch)

print("Sum priorities (part 2):", sum_priorities)
