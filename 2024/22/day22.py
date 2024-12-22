INPUT = 'input.txt'
with open(INPUT) as f:
    input = f.read()

initial = [int(x) for x in input.strip().split('\n')]

def next(x):
    x = (x ^ (x * 64) % 16777216)
    x = (x ^ (x // 32) % 16777216)
    x = (x ^ (x * 2048) % 16777216)
    return x

def next_n(x, n):
    for _ in range(n):
        x = next(x)
    return x

ans = sum(next_n(x, 2000) for x in initial)
print('Part 1:', ans)

def prices(x, n):
    p = x % 10
    for _ in range(n):
        x = next(x)
        yield (x % 10, (x % 10) - p)
        p = x % 10

def prices_with_seq(x, n):
    seq = []
    for p,d in prices(x, n):
        if len(seq) < 3:
            seq.append(str(d))
            continue
        elif len(seq) == 3:
            seq.append(str(d))
        else:
            seq = seq[1:] + [str(d)]

        yield p, ",".join(seq)

def prices_dict(x, n):
    d = {}
    for p,s in prices_with_seq(x, n):
        if s not in d:
            d[s] = p
    return d

pds = [prices_dict(x, 2000) for x in initial]
opts = set()
for d in pds:
    opts.update(d.keys())

ans = max(sum(pd.get(k, 0) for pd in pds) for k in opts)
print('Part 2:', ans)
