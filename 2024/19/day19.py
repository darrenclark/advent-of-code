import functools

INPUT = 'input.txt'

with open(INPUT) as f:
    [pieces_str, patterns_str] = f.read().split('\n\n')
    pieces = pieces_str.split(', ')
    patterns = patterns_str.split('\n')


@functools.cache
def possible_count(pattern):
    if pattern == "":
        return 1
    c = 0
    for piece in pieces:
        if pattern.startswith(piece):
            c += possible_count(pattern[len(piece):])
    return c

ans = sum(1 for pattern in patterns if possible_count(pattern) > 0)
print('Part 1:', ans)

ans = sum(possible_count(pattern) for pattern in patterns)
print('Part 2:', ans)
