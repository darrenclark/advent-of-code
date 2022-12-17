import fileinput
from enum import Enum

# Part 1:
# A, X = Rock (1 point)
# B, Y = Paper (2 points)
# C, Z = Scissors (3 points)

# Part 2:
# X = lose
# Y = draw
# Z = win

# Scoring:
#
# loss = 0 points
# draw = 3 points
# win = 6 points


class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @staticmethod
    def from_char(char):
        if char in ['A', 'X']:
            return Shape.ROCK
        elif char in ['B', 'Y']:
            return Shape.PAPER
        elif char in ['C', 'Z']:
            return Shape.SCISSORS
        else:
            raise ValueError

    def points(self):
        return self.value

class Outcome(Enum):
    WIN = 6
    DRAW = 3
    LOSS = 0

    def points(self):
        return self.value

    @staticmethod
    def from_char(char):
        if char == 'X':
            return Outcome.LOSS
        elif char == 'Y':
            return Outcome.DRAW
        elif char == 'Z':
            return Outcome.WIN
        else:
            raise ValueError

    @staticmethod
    def for_game(me, opp):
        if me == Shape.ROCK and opp == Shape.ROCK:
            return Outcome.DRAW
        elif me == Shape.ROCK and opp == Shape.PAPER:
            return Outcome.LOSS
        elif me == Shape.ROCK and opp == Shape.SCISSORS:
            return Outcome.WIN
        elif me == Shape.PAPER and opp == Shape.ROCK:
            return Outcome.WIN
        elif me == Shape.PAPER and opp == Shape.PAPER:
            return Outcome.DRAW
        elif me == Shape.PAPER and opp == Shape.SCISSORS:
            return Outcome.LOSS
        elif me == Shape.SCISSORS and opp == Shape.ROCK:
            return Outcome.LOSS
        elif me == Shape.SCISSORS and opp == Shape.PAPER:
            return Outcome.WIN
        elif me == Shape.SCISSORS and opp == Shape.SCISSORS:
            return Outcome.DRAW

    def determine_other_shape(self, shape):
        for other in [Shape.ROCK, Shape.PAPER, Shape.SCISSORS]:
            if Outcome.for_game(other, shape) == self:
                return other

lines = [x.strip().split(' ') for x in fileinput.input() if x != ""]  # type: ignore

points = 0

for [opp, me] in lines:
    opp = Shape.from_char(opp)
    me = Shape.from_char(me)
    points += me.points() + Outcome.for_game(me, opp).points() # type: ignore

print("Points (part 1):", points)

points = 0

for [opp, outcome] in lines:
    opp = Shape.from_char(opp)
    outcome = Outcome.from_char(outcome)
    me = outcome.determine_other_shape(opp)
    points += me.points() + outcome.points() # type: ignore

print("Points (part 2):", points)

