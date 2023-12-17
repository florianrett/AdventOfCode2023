import operator
from collections import Counter
import copy
from math import floor
from math import ceil
import numpy as np

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
