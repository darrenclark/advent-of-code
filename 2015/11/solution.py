input = open('input.txt', 'r').read()

parsed = input.split('\n')[0]

def has_straight(p):
    last_2 = list(p[0:2])

    for c in p[2:]:
        if ord(c) == ord(last_2[1]) + 1 == ord(last_2[0]) + 2:
            return True

        last_2.append(c)
        last_2.pop(0)

    return False

def all_letters_valid(p):
    return 'i' not in p and 'o' not in p and 'l' not in p

def has_two_pairs(p):
    pairs = 0
    l = None
    for c in p:
        if c == l:
            pairs += 1
            l = None
        else:
            l = c
    return pairs >= 2

def is_valid(p):
    return has_straight(p) and all_letters_valid(p) and has_two_pairs(p)

def increment(p, n):
    next = ord(p[n]) + 1
    if next > ord('z'):
        return increment(p[:n] + 'a' + p[n + 1:], n - 1)
    else:
        return p[:n] + chr(next) + p[n + 1:]

def gen_passwords(initial):
    p = initial

    while True:
        p = increment(p, len(p) - 1)
        yield p

def next_password(current):
    for p in gen_passwords(current):
        if is_valid(p):
            return p
    return ''

def part1():
    return next_password(parsed)

part_1_answer = part1()
print(f'Part 1: {part_1_answer}')

def part2(part_1_answer):
    return next_password(part_1_answer)

print(f'Part 2: {part2(part_1_answer)}')
