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

def has_exactly_two_in_a_row(c):
    p = None
    n = 0

    for v in c:
        if v != p:
            if n == 2: return True
            p = v
            n = 1
        else:
            n += 1

    return n == 2

def possible(a, b, c, n, fn):
    if n == 6:
        return 1 if fn(c) else 0
    else:
        p = 0
        c = c + [0]
        for i in range(0 if n == 0 else c[n-1], 10):
            c[n] = i
            if c >= a[:n + 1] and c <= b[:n + 1]:
                p += possible(a, b, c, n+1, fn)
        return p

print('Part 1:', possible(a, b, [], 0, any_same))
print('Part 2:', possible(a, b, [], 0, has_exactly_two_in_a_row))
