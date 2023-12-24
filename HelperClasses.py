import operator
from collections import Counter
import copy
from math import floor
from math import ceil
import numpy as np
import re

class CamelCardHand:

    def __init__(self, input:str, UseJokers:bool) -> None:
        self.HandString:str
        self.Cards:list[int] = []
        self.Bid:int = 0
        self.Type:int = 0 # 1:HighCard, 2:OnePair, 3:TwoPair, 4:Triple, 5:FullHouse, 6:FourOfAKind, 7:FiveOfAKind

        self.Bid = int(input.split(' ')[1])
        self.HandString = input.split(' ')[0]
        NumJokers = 0 
        for Card in self.HandString:
            CardValue = 0
            if Card.isnumeric():
                CardValue = (int(Card))
            elif Card == 'T':
                CardValue = 10
            elif Card == 'J':
                if UseJokers:
                    CardValue = 1
                    NumJokers += 1
                else:
                    CardValue = 11
            elif Card == 'Q':
                CardValue = 12
            elif Card == 'K':
                CardValue = 13
            elif Card == 'A':
                CardValue = 14

            self.Cards.append(CardValue)

        # Calculate type
        actualCards:list[int] = []
        if UseJokers:
            for c in self.Cards:
                if c != 1:
                    actualCards.append(c)
        else:
            actualCards = copy.copy(self.Cards)

        sets = Counter(actualCards).most_common(2)
        if len(sets) > 0:
            primarySetSize = sets[0][1]
        else:
            primarySetSize = 0
        if len(sets) > 1:
            secondarySetSize = sets[1][1]

        if UseJokers:
            primarySetSize += NumJokers

        if primarySetSize == 5:
            self.Type = 7
        elif primarySetSize == 4:
            self.Type = 6
        elif primarySetSize == 3:
            if secondarySetSize == 2:
                self.Type = 5
            else:
                self.Type = 4
        elif primarySetSize == 2:
            if secondarySetSize == 2:
                self.Type = 3
            else:
                self.Type = 2
        else:
            self.Type = 1        

        pass

    def IsHigher(self, other:'CamelCardHand'):
        if self.Type > other.Type:
            return True
        if self.Type < other.Type:
            return False
        
        for i in range(5):
            if self.Cards[i] > other.Cards[i]:
                return True
            if self.Cards[i] < other.Cards[i]:
                return False
        
        return False

class NodeSolver:
    Network:dict[str,tuple:str] = {}
    
    def __init__(self, StartNode:str, ) -> None:
        self.InitialNode = StartNode
        self.CurrentNode:str = StartNode
        pass

    def Step(self, bGoRight:bool) -> None:
        self.CurrentNode = self.Network[self.CurrentNode][bGoRight]
        pass

    def IsSolved(self) -> bool:
        return self.CurrentNode == 'ZZZ'
    
    def IsSolved2(self) -> bool:
        return self.CurrentNode[-1] == 'Z'
    
class Module:

    def __init__(self, input:str) -> None:
        split = input.split(" -> ")
        if input == "output" or input == "rx":
            self.type = -1
            self.name = input
            self.destinations = []
            return

        self.destinations = re.findall('[a-z]+', split[1])

        if split[0] == "broadcaster":
            self.type = 0
            self.name = split[0]
        elif split[0][0] == "%":
            self.type = 1
            self.name = split[0][1:]
            self.state = False
        elif split[0][0] == "&":
            self.type  = 2
            self.name = split[0][1:]
            self.memory = {}
        pass

    def InitConnection(self, InputModule:str) -> None:
        if self.type == 2:
            self.memory[InputModule] = False
        if self.type == -1:
            self.source = InputModule # this is only used to generalize puzzle 2

    def Pulse(self, bHigh:bool, source:str) -> list[tuple]:
        out = [] # format: tuple(source module name, destination module name, pulse value (high=True, low=False))
        
        if self.type == 0:
            out = [(self.name, x, bHigh) for x in self.destinations]
        elif self.type == 1:
            if not bHigh:
                self.state = not self.state
                out = [(self.name, x, self.state) for x in self.destinations]
        elif self.type == 2:
            self.memory[source] = bHigh
            out = [(self.name, x, not all(self.memory.values())) for x in self.destinations]
            # print(self.memory, out)
        
        return out
    
    def IsInDefaultState(self) -> bool:
        if self.type == -1:
            return True
        elif self.type == 0:
            return True
        elif self.type == 1:
            return self.state == False
        elif self.type == 2:
            return not any(self.memory.values())
        
    def Reset(self) -> None:
        if self.type == 1:
            self.state = False
        elif self.type == 2:
            for k in self.memory:
                self.memory[k] = False