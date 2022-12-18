import fileinput

lines = [x.strip() for x in fileinput.input() if x != ""]

if len(lines) != 1:
    raise ValueError


def find_start_of(ds, n):
    for i in range(n - 1, len(ds)):
        if len(set(ds[i - n : i])) == n:
            return i
    return None


ds = lines[0]


print("Start of packet (pt1):", find_start_of(ds, 4))
print("Start of message (pt2):", find_start_of(ds, 14))
