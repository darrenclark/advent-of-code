input = open('input.txt', 'r').read()

parsed = input.split('\n')[0]

def look_and_say(s):
    res = ""
    curr = s[0]
    n_curr = 1
    for c in s[1:]:
        if c != curr:
            res += str(n_curr) + curr
            curr = c
            n_curr = 1
        else:
            n_curr += 1

    res += str(n_curr) + curr
    return res

def look_and_say_n(s, n):
    res = s
    for _ in range(0, n):
        res = look_and_say(res)
    return res


def part1():
    return len(look_and_say_n(parsed, 40))

print(f'Part 1: {part1()}')

def part2():
    return len(look_and_say_n(parsed, 50))

print(f'Part 2: {part2()}')
