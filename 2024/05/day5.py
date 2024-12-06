import functools

INPUT = 'input.txt'

rules = []
updates = []

with open(INPUT) as f:
    for l in f.readlines():
        if l.find('|') >= 0:
            [a, b] = l.strip().split('|')
            rules.append((int(a), int(b)))
        elif l.find(',') >= 0:
            updates.append(list(map(int, l.strip().split(','))))

def valid_numbers_before(a):
    return [r[0] for r in rules if r[1] == a]

def valid_numbers_after(a):
    return [r[1] for r in rules if r[0] == a]

def valid_update(u):
    for i in range(len(u)):
        before = u[0:i]
        after = u[i+1:]

        v_before = valid_numbers_before(u[i])
        v_after = valid_numbers_after(u[i])

        for n in v_before:
            if n in after:
                return False
        for n in v_after:
            if n in before:
                return False

    return True

def middle(u):
    return u[len(u)//2]

s = sum(middle(u) for u in updates if valid_update(u))
print('Part 1:', s)

invalid_updates = [list(u) for u in updates if not valid_update(u)]

def sort_by_rules(a, b):
    if a == b:
        return 0
    elif b in valid_numbers_before(a):
        return -1
    elif b in valid_numbers_after(a):
        return 1
    elif a in valid_numbers_before(b):
        return 1
    elif b in valid_numbers_after(a):
        return -1
    else:
        return 0

for u in invalid_updates:
    u.sort(key=functools.cmp_to_key(sort_by_rules))

s = sum(middle(u) for u in invalid_updates)
print('Part 2:', s)
