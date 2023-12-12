from typing import List, Dict, Tuple
from collections import deque

def part_one(inputData: str) -> int:
    directionDeque, _, *nodeMaps = inputData.split('\n')
    directionDeque = deque(directionDeque)
    nodeMaps = nodeStringsToDict(nodeMaps)

    currentNode, stepCounter = "AAA", 0
    while currentNode != "ZZZ":
        if directionDeque[0] == 'L':
            currentNode = nodeMaps[currentNode][0]
        else:
            currentNode = nodeMaps[currentNode][1]
        stepCounter += 1
        directionDeque.rotate(-1)
    return stepCounter


def nodeStringsToDict(nodeStringList: List[str]) -> Dict[str, Tuple[str, str]]:
    return {node.strip(): tuple(tup.strip('()').split(", ")) 
            for node, tup in (line.split(" = ") for line in nodeStringList)}
    

################################ TESTING #################################
testInput1 = """RL

                AAA = (BBB, CCC)
                BBB = (DDD, EEE)
                CCC = (ZZZ, GGG)
                DDD = (DDD, DDD)
                EEE = (EEE, EEE)
                GGG = (GGG, GGG)
                ZZZ = (ZZZ, ZZZ)"""

testInput2 = """LLR

                AAA = (BBB, BBB)
                BBB = (AAA, ZZZ)
                ZZZ = (ZZZ, ZZZ)"""

print("Part 1 first test input:", part_one(testInput1))
print("Part 1 second test input:", part_one(testInput2))

with open("input.txt", 'r') as file:
    fileInput = file.read()
    print("Part 1 file input:", part_one(fileInput))