input = open('input.txt', 'r').read()

def parse(line):
    return line

parsed = [parse(line) for line in input.split('\n') if line != ""]

def part1():
    def has_3_vowels(s):
        vowels = 0
        for c in s:
            if c in 'aeiou':
                vowels += 1
        return vowels >= 3

    def has_double(s):
        last = None
        for c in s:
            if c == last:
                return True
            last = c
        return False

    def does_not_have_naughty_string(s):
        return 'ab' not in s and 'cd' not in s and 'pq' not in s and 'xy' not in s

    def is_nice(s):
        return has_3_vowels(s) and has_double(s) and does_not_have_naughty_string(s)

    return len([s for s in parsed if is_nice(s)])

print(f'Part 1: {part1()}')

def part2():

    def two_pair(s):
        for i in range(2, len(s)):
            if s[i-2:i] in s[i:]:
                return True

        return False

    def xyx(s):
        last_3 = []

        for c in s:
            last_3.append(c)
            if len(last_3) > 3:
                last_3.pop(0)
            elif len(last_3) < 3:
                continue

            if last_3[0] == last_3[2]:
                return True

        return False


    def is_nice(s):
        return two_pair(s) and xyx(s)

    return len([s for s in parsed if is_nice(s)])

print(f'Part 2: {part2()}')
