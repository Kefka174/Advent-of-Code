import re

def part_one(inputData: str) -> int:
    stringPairs = re.findall("mul\((\d+),(\d+)\)", inputData)
    muljobs = list((int(x), int(y)) for x, y in stringPairs)
    total = 0
    for (x, y) in muljobs:
        total += x * y
    return total

def part_two(inputData: str) -> int:
    strings = re.findall("mul\(\d+,\d+\)|do\(\)|don't\(\)", inputData)
    total = 0
    multEnabled = True
    for string in strings:
        if string == "do()":
            multEnabled = True
        elif string == "don't()":
            multEnabled = False
        elif multEnabled:
            x, y = re.findall("(\d+),(\d+)", string)[0]
            total += int(x) * int(y)
    return total

################################ TESTING #################################
testInput1 = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
testInput2 = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""

print("Part 1 test input:", part_one(testInput1)) # expect 161
print("Part 2 test input:", part_two(testInput2)) # expect 48

with open("input.txt", 'r') as file:
    fileInput = file.read()
    print("Part 1 file input:", part_one(fileInput))
    print("Part 2 file input:", part_two(fileInput))