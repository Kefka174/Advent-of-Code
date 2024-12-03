from typing import List

def part_one(inputData: str) -> int:
    reports = [list(map(int, line.split())) for line in inputData.split('\n')]
    safeReportCount = 0
    for report in reports:
        if isSafeReport(report):
            safeReportCount += 1
    return safeReportCount


def isSafeReport(report: List[int]) -> bool:
    reportShouldIncrease = report[0] < report[1]
    for i in range(1, len(report)):
        difference = report[i - 1] - report[i]
        if (reportShouldIncrease == (difference > 0)
            or abs(difference) < 1 or abs(difference) > 3):
            return False
    return True

################################ TESTING #################################
testInput = """7 6 4 2 1
               1 2 7 8 9
               9 7 6 2 1
               1 3 2 4 5
               8 6 4 4 1
               1 3 6 7 9"""

print("Part 1 test input:", part_one(testInput)) # expect 2
# print("Part 2 test input:", part_two(testInput)) # expect 4

with open("input.txt", 'r') as file:
    fileInput = file.read()
    print("Part 1 file input:", part_one(fileInput))
    # print("Part 2 file input:", part_two(fileInput))