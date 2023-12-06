import collections
import copy
import typing
from HelperClasses import Number
from ProgressBar import ProgressBar

# Rock = 0, Paper = 1, Scissors = 2
def PlayRockPaperScissors(PlayerA, PlayerB):
    Score = PlayerA + 1
    if PlayerA == PlayerB:
        # draw
        return Score + 3

    if PlayerA == (PlayerB + 1) % 3:
        # win
        return Score + 6
    else:
        # lose
        return Score

# recursive calc dir sizes
def RecCalculateDirSizes(dir, sizes = {}, subdirs = {}, files = {}):
    dirSize = 0
    for subdir in subdirs[dir]:
        RecCalculateDirSizes(subdir, sizes, subdirs, files)
        dirSize += sizes[subdir]
    
    for file in files[dir]:
        dirSize += int(file[0])

    sizes[dir] = dirSize

# move rope head and tail one step
def MoveRope(head, tail, dir):
    # update head
    newHead = head
    if dir == 'R':
        newHead = (head[0] + 1, head[1])
    elif dir == 'L':
        newHead = (head[0] - 1, head[1])
    elif dir == 'U':
        newHead = (head[0], head[1] + 1)
    elif dir == 'D':
        newHead = (head[0], head[1] - 1)
    
    # update tail
    dX = newHead[0] - tail[0]
    dY = newHead[1] - tail[1]
    moveX = 0
    moveY = 0
    if dX == 0 and abs(dY) > 1:
        moveY = 1 if dY > 0 else -1
    elif dY == 0 and abs(dX) > 1:
        moveX = 1 if dX > 0 else -1
    elif abs(dX) + abs(dY) > 2:
        moveX = 1 if dX > 0 else -1
        moveY = 1 if dY > 0 else -1
    newTail = (tail[0] + moveX, tail[1] + moveY)

    return newHead, newTail

# day 13 compare packets recursively
def ComparePackets(packet1, packet2) -> int:
    # print("comparing", packet1, "vs", packet2)
    bLeftIsInt = isinstance(packet1, int)
    bRightIsInt = isinstance(packet2, int)

    if bLeftIsInt and bRightIsInt:
        if packet1 < packet2:
            return 1
        elif packet1 == packet2:
            return 0
        else:
            return -1
    
    if not bLeftIsInt and not bRightIsInt:
        # both are lists
        for i in range(len(packet1)):
            if i >= len(packet2):
                # right ran out of items
                return -1
            comp = ComparePackets(packet1[i], packet2[i])
            if comp == 0:
                continue
            else:
                return comp
        if len(packet1) == len(packet2):
            return 0
        return 1
        
    
    # mismatched types
    if bLeftIsInt:
        return ComparePackets([packet1], packet2)
    if bRightIsInt:
        return ComparePackets(packet1, [packet2])

    print("This should never be reached")
    return -1

# day 15 is in sensor range
def IsInSensorRange(point, sensorPos, dist) -> bool:
    return abs(point[0] - sensorPos[0]) + abs(point[1] - sensorPos[1]) <= dist

def CheckLine(y, sensors, minX, maxX) -> int:    
    blocks = []
    for sensor in sensors:
        pos = sensor[0]
        dist = sensor[1]
        width = dist - abs(pos[1] - y)
        if width >= 0:
            # print("sensor", pos, "blocking from", pos[0] - width, "to", pos[0] + width)
            blocks.append((pos[0] - width, pos[0] + width))
    blocks.sort(key=lambda x: x[0])
    
    numOccupied = 0
    lastBlockUpper = minX - 1
    for b in blocks:
        start = max(b[0], lastBlockUpper + 1)
        end = min(b[1], maxX)
        if end < start:
            continue
        uniqueWidth = end - start + 1
        numOccupied += uniqueWidth
        lastBlockUpper = b[1]
        
    return numOccupied

# day 16
def RecCalcPressure(valves, flowRates, distances, current, minutesLeft) -> int:
    CurrentPressure = flowRates[current] * minutesLeft
    MaxTotalPressure = 0

    for v in valves:
        time = distances[(current, v)] + 1 # walk there and open it
        if time > minutesLeft:
            continue
        newValves = valves.copy()
        newValves.remove(v)

        MaxTotalPressure = max(MaxTotalPressure, RecCalcPressure(newValves, flowRates, distances, v, minutesLeft - time))

    return CurrentPressure + MaxTotalPressure

def RecCalcPressure2(valves, flowRates, distances, minutesLeft, current1, current2, remainingWay1, remainingWay2, depth) -> int:

    # if depth <= 2:
    #     print(minutesLeft, current1, current2, remainingWay1, remainingWay2)
    print(valves, minutesLeft, current1, current2, remainingWay1, remainingWay2)

    MaxTotalPressure = 0
    ChildPath = ""
    
    if remainingWay1 == 0:
        CurrentPressure = flowRates[current1] * minutesLeft
        Path = "1("  + str(27 - minutesLeft) + "):" + current1 + "; "

        sortedValves = valves.copy()
        # sortedValves.sort(key=lambda x : (minutesLeft - distances[(current1, x)] - 1) * flowRates[x])
        # sortedValves.reverse()
        for v in sortedValves:
            dist = distances[(current1, v)] + 1 # distance + one minute for opening
            time = min(remainingWay2, dist)
            if time >= minutesLeft: # neither agent can reach his next destination in time
                continue
            newValves = sortedValves.copy()
            newValves.remove(v)

            # print("A:", time, dist, remainingWay2 - time)
            result = RecCalcPressure2(newValves, flowRates, distances, minutesLeft - time, v, current2, dist - time, remainingWay2 - time, depth + 1)
            if result[0] > MaxTotalPressure:
                # print("Found more efficient path for agent 1 at minute", 27 - minutesLeft, ":", v)
                MaxTotalPressure = result[0]
                ChildPath = result[1]
            break
                    
    elif remainingWay2 == 0:
        CurrentPressure = flowRates[current2] * minutesLeft
        Path = "2("  + str(27 - minutesLeft) + "):" + current2 + "; "

        sortedValves = valves.copy()
        # sortedValves.sort(key=lambda x : (minutesLeft - distances[(current2, x)] - 1) * flowRates[x])
        # sortedValves.reverse()
        for v in sortedValves:
            dist = distances[(current2, v)] + 1
            time = min(remainingWay1, dist)
            if time >= minutesLeft:
                continue
            newValves = sortedValves.copy()
            newValves.remove(v)

            # print("B:", time, remainingWay1 - time, dist)
            result = RecCalcPressure2(newValves, flowRates, distances, minutesLeft - time, current1, v, remainingWay1 - time, dist - time, depth + 1)
            if result[0] > MaxTotalPressure:
                # print("Found more efficient path for agent 2 at minute", 27 - minutesLeft, ":", v)
                MaxTotalPressure = result[0]
                ChildPath = result[1]
            break
    else:
        print("No agent arrived at his destination!")

    print(Path+ChildPath, MaxTotalPressure, valves)
    return CurrentPressure + MaxTotalPressure, Path + ChildPath

def CalcPressureFixedPath(valves, flowRates, distances, minutesLeft, current) -> int:

    TotalPressure = flowRates[current] * minutesLeft
    TotalPressure = 0

    while len(valves) > 0:
        next = valves.pop(0)
        dist = distances[(current, next)] + 1
        if dist >= minutesLeft:
            break
        minutesLeft -= dist
        TotalPressure += flowRates[next] * minutesLeft
        current = next

    return TotalPressure

# day 17
def IsRockPositionValid(RockPos, rock, rocks) -> bool:
    for offset in rock:
        pos = (RockPos[0] + offset[0], RockPos[1] + offset[1])
        if pos[0] < 0 or pos[0] >= 7 or pos in rocks:
            return False
    return True

# day 20
def MixNumbers(Numbers: list, Pbar: ProgressBar, MixCount: int = 1) -> typing.List[Number]:
    Num = len(Numbers)

    MixedNumbers = Numbers.copy()

    for i in range(MixCount):
        Pbar.SetProgress(i)
        x: Number
        for x in Numbers:
            index = MixedNumbers.index(x)
            MixedNumbers.pop(index)
            # print("insert", x, "at", i + x.Value)
            MixedNumbers.insert((index + x.Value) % (Num - 1), x)
            # print(MixedNumbers)

    return MixedNumbers

# day 21
def RecSolveRiddle(Pbar: ProgressBar, UnsolvedMonkeys: typing.Set[str], SolvedMonkeys):
    pass

# day 22
def CubeWrapTestinput(pos, facing):

    if facing == 0: # going east
        if pos[1] < 4: # side 1 to side 6 (right)
            return (15, 11 - pos[1]), 2
        if pos[1] < 8:  # side 4 to side 6 (top)
            return (19 - pos[1], 8), 1
        if pos[1] >= 8:  # side 6 to side 1 (right)
            return (11, 11 - pos[1]), 2
    
    if facing == 1: # going south
        if pos[0] < 4: # side 2 to side 5 (bot)
            return (11 - pos[0], 11), 3
        if pos[0] < 8: # side 3 to side 5 (left)
            return (8, 15 - pos[0]), 1
        if pos[0] < 12: # side 5 to side 2 (bot)
            return (11 -  pos[0], 7), 3
        if pos[0] >= 12: # side 6 to side 2 (left)
            return (0, 15 - pos[0]), 1

    if facing == 2: # going west
        if pos[1] < 4: # side 1 to side 3 (top)
            return (11 - pos[1], 4), 1
        if pos[1] < 8: # side 2 to side 6 (bot)
            return (15 - pos[1], 11), 1
        if pos[1] >= 8: # side 5 to side 3 (bot)
            return (15 - pos[1], 7), 3

    if facing == 3: # going north
        if pos[0] < 4: # side 2 to side 1 (top)
            return (11 - pos[0], 0), 1
        if pos[0] < 8: # side 3 to side 1 (left)
            return (8, 11 - pos[0]), 0
        if pos[0] < 12: # side 1 to side 2 (top)
            return (11 - pos[0], 4), 1
        if pos[0] >= 12: # side 6 to side 4 (right)
            return (11, 19 - pos[0]), 2

    print("encountered unhandled state for {pos} and {facing}!")
    pass

def CubeWrapMyInput(pos, facing):

    if facing == 0: # going east
        if pos[1] < 50: # side 2 to side 5 (right)
            return (99, 149 - pos[1]), 2
        if pos[1] < 100: # side 3 to side 2 (bot)
            return (50 + pos[1], 49), 3
        if pos[1] < 150: # side 5 to side 2 (right)
            return (149, 149 - pos[1]), 2
        if pos[1] >= 150: # side 6 to side 5 (bot)
            return (pos[1] - 100, 149), 3

    if facing == 1: # going south
        if pos[0] < 50: # side 6 to side 2 (top)
            return (100 + pos[0], 0), 1
        if pos[0] < 100: # side 5 to side 6 (right)
            return (49, 100 + pos[0]), 2
        if pos[0] >= 100: # side 2 to side 3 (right)
            return (99, pos[0] - 50), 2
    
    if facing == 2: # going west
        if pos[1] < 50: # side 1 to side 4 (left)
            return (0, 149 - pos[1]), 0
        if pos[1] < 100: # side 3 to side 4 (top)
            return (pos[1] - 50, 100), 1
        if pos[1] < 150: # side 4 to side 1 (left)
            return (50, 149 - pos[1]), 0
        if pos[1] >= 150: # side 6 to side 1 (top)
            return (pos[1] - 100, 0), 1

    if facing == 3: # going north
        if pos[0] < 50: # side 4 to side 3 (left)
            return (50, pos[0] + 50), 0
        if pos[0] < 100: # side 1 to side 6 (left)
            return (0, pos[0] + 100), 0
        if pos[0] >= 100: # side 2 to side 6 (bot)
            return (pos[0] - 100, 199), 3

    print("encountered unhandled state for {pos} and {facing}!")
    pass

# day 23
dirs = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)] # N, NE, E, SE, S, SW, W, NW
# list of possible moves containing 3-tuples: (list[dir indices], moveX, moveY)
moves = [([0, 1, 7], 0, 1), ([3, 4, 5], 0, -1), ([5, 6, 7], -1, 0), ([1, 2, 3], 1, 0)] # N, S, W, E
def UpdateElfPositions(elves: typing.Set[tuple], startMoveIndex: int) -> typing.Set[tuple]:
    newPositions = {}

    for e in elves:
        adj = [(e[0] + d[0], e[1] + d[1]) in elves for d in dirs]
        
        if collections.Counter(adj)[False] == 8:
            # no other elves
            newPositions[e] = e
            continue
        
        bFoundMove = False
        for i in range(startMoveIndex, startMoveIndex + 4):
            move = moves[i % 4]
            if all([not adj[x] for x in move[0]]):
                newPositions[e] = (e[0] + move[1], e[1] + move[2])
                bFoundMove = True
                break

        if not bFoundMove:
            newPositions[e] = e

    c = collections.Counter(newPositions.values())

    outPositions = set()
    for k, v in newPositions.items():
        if c[v] == 1:
            outPositions.add(v)
        else:
            outPositions.add(k)
            
    return outPositions
