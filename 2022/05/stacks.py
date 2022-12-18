import fileinput
from dataclasses import dataclass
from enum import Enum


@dataclass
class CratesLine:
    crates: list[str | None]


class MoveMode(Enum):
    ONE_BY_ONE = "ONE_BY_ONE"
    ALL_AT_ONCE = "ALL_AT_ONCE"


@dataclass
class Move:
    count: int
    src: int
    dest: int


class Stacks:
    stacks: list[list[str]]
    mode: MoveMode

    def __init__(self, crates_lines: list[CratesLine], mode: MoveMode):
        self.stacks = []
        self.mode = mode
        num_stacks = len(crates_lines[0].crates)

        for i in range(0, num_stacks):
            stack = []
            for line in crates_lines:
                if line.crates[i] != None:
                    stack.insert(0, line.crates[i])
            self.stacks.append(stack)

    def __repr__(self):
        res = ""
        for i, stack in enumerate(self.stacks):
            res += f"{i + 1}: {stack}\n"
        return res.rstrip()

    def top(self):
        res = ""
        for stack in self.stacks:
            res += stack[len(stack) - 1]
        return res

    def apply(self, move: Move):
        if self.mode == MoveMode.ONE_BY_ONE:
            for _ in range(move.count):
                self.pop_and_push(move.src, move.dest, 1)
        else:
            self.pop_and_push(move.src, move.dest, move.count)

    def pop_and_push(self, src: int, dest: int, count: int):
        self.stacks[dest - 1] += self.stacks[src - 1][-count:]
        self.stacks[src - 1] = self.stacks[src - 1][:-count]


def parse_line(line: str):
    if "[" in line:
        return parse_crates_line(line)
    elif line.startswith("move"):
        return parse_move_line(line)
    else:
        return None


def parse_crates_line(line: str):
    results = []
    while line != "":
        part = line[0:3]
        if part == "   ":
            results.append(None)
        else:
            results.append(part[1:2])
        line = line[4:]
    return CratesLine(results)


def parse_move_line(line: str):
    [_, count, _, src, _, dest] = line.split(" ")
    return Move(int(count), int(src), int(dest))


lines = [x.replace("\n", "") for x in fileinput.input() if x != ""]
crates_lines: list[CratesLine] = []
moves: list[Move] = []

for line in lines:
    result = parse_line(line)
    if isinstance(result, CratesLine):
        crates_lines.append(result)
    if isinstance(result, Move):
        moves.append(result)

stacks_pt1 = Stacks(crates_lines, MoveMode.ONE_BY_ONE)
stacks_pt2 = Stacks(crates_lines, MoveMode.ALL_AT_ONCE)

for move in moves:
    stacks_pt1.apply(move)
    stacks_pt2.apply(move)

print("Crates on top (pt1):", stacks_pt1.top())
print("Crates on top (pt2):", stacks_pt2.top())
