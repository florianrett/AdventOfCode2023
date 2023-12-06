import operator
from collections import Counter
from math import floor
from math import ceil
from typing import Sequence
import numpy as np

# day 11
class Monkey:

    items = []
    operation = None
    op = None
    operand = 0 # maybe invalid
    test = 1
    TestTrueMonkey = -1
    TestFalseMonkey = -1
    bRelief = True

    timesInspected = 0

    def __init__(self, StartingItems = [], Operation = "", Test = 1, TestTrueMonkey = -1, TestFalseMonkey = -1, bRelief = True) -> None:
        self.items = StartingItems
        self.operation = Operation
        self.test = Test
        self.TestTrueMonkey = TestTrueMonkey
        self.TestFalseMonkey = TestFalseMonkey
        self.timesInspected = 0
        self.bRelief = bRelief

        # parse operation lambda
        parts = Operation.split(' ')
        self.op = operator.add if parts[1] == '+' else operator.mul

        if parts[2] == "old":
            self.operation = lambda old: self.op(old, old)
        else:
            self.operand = int(parts[2])
            self.operation = lambda old: self.op(old, self.operand)
        
        pass


    def TakeTurn(self) -> list:
        Throws = [] # list of tuples (WorryLevel, TargetMonkey)

        for item in self.items:
            # inspect item
            item = self.operation(item)
            if self.bRelief:
                item = np.int64(np.floor(item / 3))
            self.timesInspected += 1
            
            throw = ()
            if item % self.test == 0:
                throw = (item, self.TestTrueMonkey)
            else:
                throw = (item, self.TestFalseMonkey)
            Throws.append(throw)
            
        self.items.clear()
        return Throws

# day 19
class RobotFactory:

    # Minute = 1

    OreCost = 0
    ClayCost = 0
    ObsCostOre = 0
    ObsCostClay = 0
    GeoCostOre = 0
    GeoCostObs = 0

    OreRobotLimit = 0
    ClayRobotLimit = 0
    ObsRobotLimit = 0

    NumMinutes = 0

    AbsoluteMaximum = 0
    GeodeEstimates = []

    def __init__(self, Blueprint, NumMinutes) -> None:
        self.OreCost = Blueprint[0]
        self.ClayCost = Blueprint[1]
        self.ObsCostOre = Blueprint[2]
        self.ObsCostClay = Blueprint[3]
        self.GeoCostOre = Blueprint[4]
        self.GeoCostObs = Blueprint[5]

        self.OreRobotLimit = max(self.OreCost, self.ClayCost, self.ObsCostOre, self.GeoCostOre)
        self.ClayRobotLimit = self.ObsCostClay
        self.ObsRobotLimit = self.GeoCostObs

        self.NumMinutes = NumMinutes
        
        self.GeodeEstimates = [(t + 0) * t / 2 for t in range(NumMinutes + 1)]

        pass

    def FindOptimum(self) -> int:
        
        for i in range(4):
            self.RecFindNumGeodes(self.NumMinutes, i, 1, 0, 0, 0, 0, 0, 0, 0)
        
        return self.AbsoluteMaximum

    def RecFindNumGeodes(self, MinutesLeft, robotType, oreRobots, clayRobots, obsRobots, geoRobots, ore, clay, obs, geo):

        # stop search if any robot exceeded his limit or current state can't possibly exceed maximum
        if (robotType == 0 and oreRobots >= self.OreRobotLimit or
            robotType == 1 and clayRobots >= self.ClayRobotLimit or
            robotType == 2 and ( obsRobots >= self.ObsRobotLimit or clayRobots == 0) or 
            geo + MinutesLeft * geoRobots + self.GeodeEstimates[MinutesLeft] <= self.AbsoluteMaximum ):
            return
        
        while MinutesLeft:
            if robotType == 0 and ore >= self.OreCost:
                for type in range(4):
                    self.RecFindNumGeodes(MinutesLeft - 1, type, oreRobots + 1, clayRobots, obsRobots, geoRobots, ore + oreRobots - self.OreCost, clay + clayRobots, obs + obsRobots, geo + geoRobots)
                return
            elif robotType == 1 and ore >= self.ClayCost:
                for type in range(4):
                    self.RecFindNumGeodes(MinutesLeft - 1, type, oreRobots, clayRobots + 1, obsRobots, geoRobots, ore + oreRobots - self.ClayCost, clay + clayRobots, obs + obsRobots, geo + geoRobots)
                return
            elif robotType == 2 and ore >= self.ObsCostOre and clay >= self.ObsCostClay:
                for type in range(4):
                    self.RecFindNumGeodes(MinutesLeft - 1, type, oreRobots, clayRobots, obsRobots + 1, geoRobots, ore + oreRobots - self.ObsCostOre, clay + clayRobots - self.ObsCostClay, obs + obsRobots, geo + geoRobots)
                return
            elif robotType == 3 and ore >= self.GeoCostOre and obs >= self.GeoCostObs:
                for type in range(4):
                    self.RecFindNumGeodes(MinutesLeft - 1, type, oreRobots, clayRobots, obsRobots, geoRobots + 1, ore + oreRobots - self.GeoCostOre, clay + clayRobots, obs + obsRobots - self.GeoCostObs, geo + geoRobots)
                return
            
            # build nothing, inplace increase variables
            MinutesLeft, ore, clay, obs, geo = MinutesLeft - 1, ore + oreRobots, clay + clayRobots, obs + obsRobots, geo + geoRobots        
        self.AbsoluteMaximum = max(self.AbsoluteMaximum, geo)
        
        return

class Number:

    Value = 0

    def __init__(self, value: int) -> None:
        self.Value = int(value)
        pass

    def __str__(self) -> str:
        return str(self.Value)
        pass

    def __repr__(self) -> str:
        return str(self.Value)