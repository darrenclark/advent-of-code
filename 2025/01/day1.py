INPUT = 'input.txt'

with open(INPUT) as f:
    input = [int(l) for l in f.read().replace("L", "-").replace("R", "").strip().split()]

dial = 50
pw = 0
pw2 = 0

for i in input:
    pw2 += abs((dial + i) // 100)
    if dial == 0 and i < 0:
        # started on 0, the above adds one too many
        pw2 -= 1
    if (dial + i) % 100 == 0 and i < 0:
        # landing on a 0, so we need to add one more
        pw2 += 1

    dial = (dial + i) % 100

    if dial == 0:
        pw += 1

print('part 1: ', pw)
print('part 2: ', pw2)
