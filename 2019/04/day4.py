INPUT = 'input.txt'

with open(INPUT) as f:
    input = f.read()

a, b = input.strip().split("-")
a = list(int(x) for x in a)
b = list(int(x) for x in b)

def any_same(c):
    for i,j in zip(c, c[1:]):
        if i == j: return True
    return False

def possible(a, b, c, n):
    if n == 6:
        return 1 if any_same(c) else 0
    else:
        p = 0
        c = c + [0]
        for i in range(0 if n == 0 else c[n-1], 10):
            c[n] = i
            if c >= a[:n + 1] and c <= b[:n + 1]:
                p += possible(a, b, c, n+1)
        return p

print('Part 1:', possible(a, b, [], 0))
