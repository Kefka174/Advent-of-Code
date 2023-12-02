from typing import List

def part_one(codes: List[str]) -> int:
    sum = 0
    for code in codes:
        firstDigit, lastDigit = None, None
        index = 0
        while not firstDigit:
            if code[index].isdigit():
                firstDigit = int(code[index])
            index += 1
        index = len(code) - 1
        while not lastDigit:
            if code[index].isdigit():
                lastDigit = int(code[index])
            index -= 1
        sum += (firstDigit * 10) + lastDigit
    return sum


testInput = ["1abc2", "pqr3stu8vwx", "a1b2c3d4e5f", "treb7uchet"]
print(part_one(testInput))

with open("input.txt", 'r') as file:
    print(part_one(file.read().split()))