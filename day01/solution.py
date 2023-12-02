from typing import List, Tuple

def part_one(codes: List[str]) -> int: ########## clean up with regex
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


def part_two(codes: List[str]) -> int:
    digits = [("one", 1), ("two", 2), ("three", 3), ("four", 4), 
              ("five", 5), ("six", 6), ("seven", 7), ("eight", 8), 
              ("nine", 9), ('1', 1), ('2', 2), ('3', 3), ('4', 4), 
              ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9)]
    trie, sum = Trie(digits), 0
    for code in codes:
        firstDigit, lastDigit = None, None
        index = 0
        while not firstDigit:
            valAtIndex = trie.findVal(code, index)
            if valAtIndex:
                firstDigit = valAtIndex
            index += 1
        index = len(code) - 1
        while not lastDigit:
            valAtIndex = trie.findVal(code, index)
            if valAtIndex:
                lastDigit = valAtIndex
            index -= 1
        sum += (firstDigit * 10) + lastDigit
    return sum

class Trie:
    def __init__(self, words: List[Tuple[str, int]]) -> None:
        self.root = self.TrieNode()
        for word, value in words:
            self.insert(word, value)

    def insert(self, word: str, value: int) -> None:
        currentNode = self.root
        for letter in word:
            if letter not in currentNode.children:
                currentNode.children[letter] = self.TrieNode()
            currentNode = currentNode.children[letter]
        currentNode.value = value

    def findVal(self, string: str, index: int) -> int:
        currentNode = self.root
        while (not currentNode.value) and (index < len(string)):
            if string[index] not in currentNode.children:
                return None
            currentNode = currentNode.children[string[index]]
            index += 1
        return currentNode.value

    class TrieNode:
        def __init__(self, value = None) -> None:
            self.children = {}
            self.value = value


##########################################################################
testInput1 = ["1abc2", "pqr3stu8vwx", "a1b2c3d4e5f", "treb7uchet"]
print(part_one(testInput1))
testInput2 = ["two1nine", "eightwothree", "abcone2threexyz", "xtwone3four", 
              "4nineeightseven2", "zoneight234", "7pqrstsixteen"]
print(part_two(testInput2))

with open("input.txt", 'r') as file:
    fileInput = file.read().split()
    print(part_one(fileInput))
    print(part_two(fileInput))