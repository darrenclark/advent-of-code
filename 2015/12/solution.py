import json

input = open('input.txt', 'r').read()

parsed = json.loads(input)

def part1():
    def sum_json(obj):
        if type(obj) == int:
            return obj
        elif type(obj) == list:
            return sum([sum_json(x) for x in obj])
        elif type(obj) == dict:
            return sum([sum_json(x) for x in obj.values()])
        else:
            return 0

    return sum_json(parsed)

print(f'Part 1: {part1()}')

def part2():
    def sum_json(obj):
        if type(obj) == int:
            return obj
        elif type(obj) == list:
            return sum([sum_json(x) for x in obj])
        elif type(obj) == dict:
            if 'red' in obj.values():
                return 0
            return sum([sum_json(x) for x in obj.values()])
        else:
            return 0

    return sum_json(parsed)

print(f'Part 2: {part2()}')
