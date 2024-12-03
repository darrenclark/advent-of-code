from collections import Counter

INPUT = 'input.txt'

left = []
right = []

with open(INPUT, 'r') as f:
    for line in f.readlines():
        [l, _, _, r] = line.split(' ')
        left.append(int(l.strip()))
        right.append(int(r.strip()))

left.sort()
right.sort()

sum = 0
for (l, r) in zip(left, right):
    sum += abs(l - r)
print("Part 1: ", sum)

right_counter = Counter(right)

sum = 0
for l in left:
    sum += right_counter[l] * l
print("Part 2: ", sum)
