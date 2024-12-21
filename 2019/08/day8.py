INPUT = 'input.txt'
with open(INPUT) as f:
    input = f.read()

input = input.strip()

w=25
h=6
a=w*h

assert len(input) % a == 0

chunks = []
for i in range(len(input) // a):
    chunks.append(list(input[i*a:i*a+a]))

def count(c, n):
    return sum(1 for x in c if n == x)

lowest = min(range(len(chunks)), key=lambda i: count(chunks[i], '0'))
ans = count(chunks[lowest], '1') * count(chunks[lowest], '2')
print('Part 1:', ans)
