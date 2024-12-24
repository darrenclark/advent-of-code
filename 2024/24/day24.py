import functools

INPUT='input.txt'
with open(INPUT) as f:
    input = f.read()

i, g = input.strip().split('\n\n')

initial = {a.split(': ')[0]:int(a.split(': ')[1]) for a in i.split('\n')}
gates = {}
for l in g.split('\n'):
    a, t, b, _, o = l.split(' ')
    gates[o] = (a, t, b)

@functools.cache
def value(w):
    if w in initial:
        return initial[w]
    (a, t, b) = gates[w]
    a = value(a)
    b = value(b)

    match t:
        case 'AND': return a & b
        case 'OR': return a | b
        case 'XOR': return a ^ b
        case _: raise RuntimeError(f'unexpected gate: {t}')

zw = [a for a in initial if a.startswith('z')] + [a for a in gates if a.startswith('z')]
zw.sort()

ans = 0
for i, z in enumerate(zw):
    ans |= value(z) << i
print('Part 1:', ans)
