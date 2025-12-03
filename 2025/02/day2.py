INPUT = 'input.txt'

with open(INPUT) as f:
    input = [p.strip() for p in f.read().split(',')]

pt1 = 0
pt2 = 0

def is_invalid_pt1(i):
    s = str(i)
    return len(s) % 2 == 0 and s[:len(s)//2] == s[len(s)//2:]

def is_invalid_pt2(i):
    s = str(i)

    for l in range(1, len(s)//2 + 1):
        if len(s) % l != 0: continue

        if all(s[0:l] == s[j:j+l] for j in range(0, len(s), l)):
            return True


for r in input:
    [first, last] = map(int, r.split('-'))

    for i in range(first, last + 1):
        if is_invalid_pt1(i):
            pt1 += i
        if is_invalid_pt2(i):
            pt2 += i

print('part 1:', pt1)
print('part 2:', pt2)
