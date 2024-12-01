from typing import List, Callable
from re import split
from collections import deque

def part_one(scratchcards: List[str]) -> int:
    sum = 0
    for card in scratchcards:
        wins = countScratchcardWins(card)
        if wins > 0:
            sum += pow(2, wins - 1)
    return sum

def part_two(scratchcards: List[str]) -> int:
    totalCardCount, cardCountQueue = 0, FirstKQueue()
    for card in scratchcards:
        cardCount = cardCountQueue.dequeue() or 1
        wins = countScratchcardWins(card)

        totalCardCount += cardCount
        cardCountQueue.modifyFirstK(wins, lambda x : x + cardCount, 1)
    return totalCardCount


def countScratchcardWins(scratchcard: str) -> int:
    _, winningString, myNumsString = split(": | \| ", scratchcard)
    winners = set(int(x) for x in winningString.split())
    playerNums = [int(x) for x in myNumsString.split()]
    
    winCount = 0
    for num in playerNums:
        if num in winners:
            winCount += 1
    return winCount

class FirstKQueue:
    def __init__(self) -> None:
        self.deque = deque()

    def dequeue(self) -> object:
        if not self.deque:
            return None
        return self.deque.popleft()
    
    def modifyFirstK(self, k: int, func: Callable[[object], object], 
                     defaultValue: object) -> None:
        modifiedElements = deque()
        while k:
            currentElement = defaultValue
            if self.deque:
                currentElement = self.deque.popleft()
            modifiedElements.append(func(currentElement))
            k -= 1
        self.deque = modifiedElements + self.deque


################################ TESTING #################################
testInput = ["Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53", 
             "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19", 
             "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1", 
             "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83", 
             "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36", 
             "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"]
print("Part 1 test input:", part_one(testInput))
print("Part 2 test input:", part_two(testInput))

with open("input.txt", 'r') as file:
    fileInput = file.read().split('\n')
    print("Part 1 file input:", part_one(fileInput))
    print("Part 2 file input:", part_two(fileInput))