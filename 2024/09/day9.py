INPUT = 'input.txt'

with open(INPUT) as f:
    input = list(map(int, list(f.read().strip())))

b = []
for (i, s) in enumerate(input):
    file_id = i//2 if i % 2 == 0 else 'free'
    b.append((file_id, s))

def defrag_by_block(b):
    while any([x[0] == 'free' for x in b]):
        last = b.pop()
        if last[0] == 'free':
            continue

        file_id = last[0]
        to_move = last[1]
        while to_move > 0:
            try:
                i = [x[0] for x in b].index('free')
                free_space = b[i][1]

                if to_move >= free_space:
                    b[i] = (file_id, b[i][1])
                    to_move -= free_space
                else:
                    b[i] = (file_id, to_move)
                    b.insert(i+1, ('free', free_space-to_move))
                    to_move = 0
            except ValueError:
                b.append((file_id, to_move))
                to_move = 0
    return b

def defrag_by_file(b):
    for file_id in range(b[-1][0], -1, -1):
        i = [x[0] for x in b].index(file_id)
        (file_id, size) = b[i]

        for j in range(0, i):
            if b[j][0] == 'free' and b[j][1] >= size:
                b[i] = ('free', size)
                if b[j][1] == size:
                    b[j] = (file_id, size)
                else:
                    b.insert(j+1, ('free', b[j][1]-size))
                    b[j] = (file_id, size)
                break

    return b

def compute_checksum(b):
    checksum = 0
    i = 0
    for (file_id, size) in b:
        if file_id == 'free':
            i += size
            continue
        for _ in range(size):
            checksum += i * file_id
            i += 1
    return checksum

def print_b(b):
    for (file_id, size) in b:
        if file_id == 'free':
            print('.' * size, end='')
        else:
            print(str(file_id) * size, end='')
    print()


print('Part 1:', compute_checksum(defrag_by_block(list(b))))

print('Part 2:', compute_checksum(defrag_by_file(list(b))))
