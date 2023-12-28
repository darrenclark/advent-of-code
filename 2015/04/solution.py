import hashlib

input = 'iwrupvqb'

def md5(string):
    return hashlib.md5(string.encode()).hexdigest()

def solve(n):
    expected = '0' * n

    i = 0
    while True:
        i += 1
        s = input + str(i)
        if md5(s)[0:n] == expected:
            return i

def part1():
    return solve(5)

print(f'Part 1: {part1()}')

def part2():
    return solve(6)

print(f'Part 2: {part2()}')
