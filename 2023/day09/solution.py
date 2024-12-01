from typing import List

def part_one(inputData: str) -> int:
    total = 0
    for history in inputData.split('\n'):
        seq = [int(x) for x in history.split()]
        total += sum(levelValuesAtIndex(seq, -1))
    return total

def part_two(inputData: str) -> int:
    total = 0
    for history in inputData.split('\n'):
        seq = [int(x) for x in history.split()]
        firstValuesInEachLevel = levelValuesAtIndex(seq, 0)
        
        while len(firstValuesInEachLevel) > 1:
            firstValuesInEachLevel[-2] -= firstValuesInEachLevel[-1]
            firstValuesInEachLevel.pop()
        total += firstValuesInEachLevel[0]
    return total


def levelValuesAtIndex(sequence: List[int], index: int) -> List[int]:
    valuesAtIndex = []
    while not all(x == 0 for x in sequence):
            valuesAtIndex.append(sequence[index])
            sequence = sequenceDifferences(sequence)
    return valuesAtIndex

def sequenceDifferences(sequence: List[int]) -> List[int]:
    differences = [0] * (len(sequence) - 1)
    for i in range(len(sequence) - 1):
        differences[i] = sequence[i + 1] - sequence[i]
    return differences

################################ TESTING #################################
testInput1 = """0 3 6 9 12 15
                1 3 6 10 15 21
                10 13 16 21 30 45"""

print("Part 1 test input:", part_one(testInput1))
print("Part 2 test input:", part_two(testInput1))

with open("input.txt", 'r') as file:
    fileInput = file.read()
    print("Part 1 file input:", part_one(fileInput))
    print("Part 2 file input:", part_two(fileInput))