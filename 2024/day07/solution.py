from typing import Callable

def part_one(inputData: str) -> int:
    functions = [
        lambda a, b : a + b,
        lambda a, b : a * b
    ]
    successSums = 0
    for line in inputData.split('\n'):
        goal = int(line.split(': ')[0])
        vals = list(map(int, line.split(': ')[1].split()))
        if recursiveTotal(goal, vals[0], functions, vals):
            successSums += goal
    return successSums

def part_two(inputData: str) -> int:
    functions = [
        lambda a, b : a + b,
        lambda a, b : a * b,
        lambda a, b : int(str(a) + str(b))
    ]
    successSums = 0
    for line in inputData.split('\n'):
        goal = int(line.split(': ')[0])
        vals = list(map(int, line.split(': ')[1].split()))
        if recursiveTotal(goal, vals[0], functions, vals):
            successSums += goal
    return successSums


def recursiveTotal(goal: int, currentTotal: int, functions: list[Callable[[int, int], int]], 
                   vals: list[int], valIndex: int = 1) -> bool:
    if currentTotal > goal: # would need to be removed if subtraction is a valid function
        return False
    if valIndex == len(vals):
        return (currentTotal == goal)
    
    for function in functions:
        newCurrent = function(currentTotal, vals[valIndex])
        if recursiveTotal(goal, newCurrent, functions, vals, valIndex + 1):
            return True
    return False

################################ TESTING #################################
testInput = """190: 10 19
               3267: 81 40 27
               83: 17 5
               156: 15 6
               7290: 6 8 6 15
               161011: 16 10 13
               192: 17 8 14
               21037: 9 7 18 13
               292: 11 6 16 20"""

print("Part 1 test input:", part_one(testInput)) # expect 3749
print("Part 2 test input:", part_two(testInput)) # expect 11387

with open("input.txt", 'r') as file:
    fileInput = file.read()
    print("Part 1 file input:", part_one(fileInput))
    print("Part 2 file input:", part_two(fileInput))