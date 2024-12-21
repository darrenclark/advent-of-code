INPUT = 'input.txt'
with open(INPUT) as f:
    input = f.read()

# planet => plant it orbits
parents = dict()

for l in input.strip().split('\n'):
    [a, b] = l.split(')')
    parents[b] = a

def num_ancestors(x):
    if x in parents:
        return 1 + num_ancestors(parents[x])
    else:
        return 0

ans = 0
for x in parents:
    ans += num_ancestors(x)

print('Part 1:', ans)
