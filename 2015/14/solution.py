from dataclasses import dataclass

input = open('input.txt', 'r').read()

@dataclass
class Reindeer:
    name: str
    speed: int
    duration: int
    rest: int

    def distance(self, n):
        period = self.duration + self.rest
        dist_per_period = self.speed * self.duration
        res = (n // period) * dist_per_period

        rem = n % period
        res += min(self.duration, rem) * self.speed

        return res

def parse(line):
    split = line.split()
    return Reindeer(name=split[0], speed=int(split[3]), duration=int(split[6]), rest=int(split[13]))

parsed = [parse(line) for line in input.split('\n') if line != ""]

def part1():
    return max([r.distance(2503) for r in parsed])

print(f'Part 1: {part1()}')

def part2():
    points = {}
    for r in parsed:
        points[r.name] = 0

    for t in range(1, 2503 + 1):
        distances = {}
        for r in parsed:
            distances[r.name] = r.distance(t)
        max_distance = max(distances.values())
        for k, v in distances.items():
            if v == max_distance:
                points[k] += 1

    return max(points.values())

print(f'Part 2: {part2()}')
