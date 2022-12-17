import fileinput

calories_by_elf = list()
current_calories = 0

for line in fileinput.input():
    stripped = line.strip()
    if stripped == "":
        calories_by_elf.append(current_calories)
        current_calories = 0
    else:
        current_calories += int(stripped)

calories_by_elf.append(current_calories)
calories_by_elf.sort(reverse=True)

print("Most calories:", calories_by_elf[0])
print("Sum of top 3 calories:", sum(calories_by_elf[0:3]))
