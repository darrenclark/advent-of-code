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

def run(initial):
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

    zw = [a for a in gates if a.startswith('z')]
    zw.sort()

    ans = 0
    for i, z in enumerate(zw):
        ans |= value(z) << i
    return ans

print('Part 1:', run(initial))


def verify():
    def to_input(x, y):
        xs = {f'x{i:02d}':x >> i & 1 for i in range(45)}
        ys = {f'y{i:02d}':y >> i & 1 for i in range(45)}
        return xs | ys

    def find_gate(ia, ib, it):
        for g in gates:
            a,t,b = gates[g]
            if ((a == ia and b == ib) or (a == ib and b == ia)) and t == it:
                return g
        return None

    def find_carry(a, b):
        return find_gate(a, b, 'AND')

    def find_sum(a, b):
        return find_gate(a, b, 'XOR')


    def verify_adds_work():
        success = True
        for i in range(45):
            # test x input
            if run(to_input(1 << i, 0)) != 1 << i:
                print(f"x input broken at {i}")
                success = False

            # test y input
            if run(to_input(0, 1 << i)) != 1 << i:
                print(f"y input broken at {i}")
                success = False

            # test carry
            if run(to_input(1 << i, 1 << i)) != 1 << (i+1):
                print(f"carry broken at {i}")
                success = False

        return success

    def verify_connections():
        cin = None
        for i in range(45):
            a = f'x{i:02d}'
            b = f'y{i:02d}'

            c = find_carry(a, b)
            if not c:
                raise RuntimeError(f'no carry for {i}')

            s = find_sum(a, b)
            if not s:
                raise RuntimeError(f'no sum for {i}')

            if c.startswith('z'):
                print(f'Unepxected carry for {i}: {c}')

            if i == 0:
                cin = c
                continue

            z = find_gate(s, cin, 'XOR')
            if z is None:
                print(f'no output for {i}')
                return False
            elif not z.startswith('z'):
                print(f'wrong outut for {i}, got {z}')
                return False

            cb1 = find_gate(cin, s, 'AND')
            if cb1 is None:
                print(f'no AND gate in carry block for {i}')
                return False
            cb2 = find_gate(cb1, c, 'OR')
            if cb2 is None:
                print(f'no OR gate in carry block for {i}')
                return False
            cin = cb2

        return True

    def show_circuit():
        import graphviz

        NODE_COLOR={
            'OR': '#ADD8E6',
            'XOR': '#FFCCCB',
            'AND': '#90EE90',
        }

        dot = graphviz.Graph()
        for a in initial:
            dot.node(a, style='bold')
        for g in gates:
            style='filled'
            if g.startswith('z'):
                style += ',bold'
            dot.node(g, label=g + '\n' + gates[g][1], style=style, fillcolor=NODE_COLOR[gates[g][1]])
        for g in gates:
            a,t,b = gates[g]
            dot.edge(g, a)
            dot.edge(g, b)
        dot.render('/tmp/circuit.gv', view=True)

    adds_work = verify_adds_work()
    connections = verify_connections()
    if not adds_work or not connections:
        show_circuit()
        raise RuntimeError('More wires to swap')

swapped = []
def swap_output_wires(a, b):
    ga = gates[a]
    gb = gates[b]
    gates[a] = gb
    gates[b] = ga
    swapped.append(a)
    swapped.append(b)


swap_output_wires('z10', 'ggn')
swap_output_wires('ndw', 'jcb')
swap_output_wires('z32', 'grm')
swap_output_wires('z39', 'twr')

# To modify for another input:
#   1. Remove swap_output_wires(..) above
#   2. Run, and look at generated graph to see which wires need to be swapped (they're adders)
#   3. Add swap_output_wires(..) line above
#   4. Rinse & repeate until all 8 wires to swap are found
verify()

print('Part 2:', ",".join(sorted(swapped)))
