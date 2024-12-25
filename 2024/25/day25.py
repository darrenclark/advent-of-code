INPUT='input.txt'
with open(INPUT) as f:
    input = f.read()

a = []
b = []

w,h = 0,0
for gin in input.strip().split('\n\n'):
    g = gin.split('\n')

    h = len(g)
    w = len(g[0])
    c = [0]*w
    for y in range(h):
        for x in range(w):
            if g[y][x] == '#':
                c[x] += 1

    if g[0][0] == '#':
        a.append(c)
    elif g[0][0] == '.':
        b.append(c)
    else:
        raise RuntimeError()

ans = 0
for i in a:
    for j in b:
        fits = True
        for ii,jj in zip(i, j):
            if ii + jj > h:
                fits = False
                break
        if fits:
            ans += 1

print('Part 1:', ans)
