def part_one(inputData: str) -> int:
    return 0


################################ TESTING #################################
testInput = """...#......
               .......#..
               #.........
               ..........
               ......#...
               .#........
               .........#
               ..........
               .......#..
               #...#....."""

print("Part 1 test input:", part_one(testInput)) # expect 

with open("input.txt", 'r') as file:
    fileInput = file.read()
    print("Part 1 file input:", part_one(fileInput))