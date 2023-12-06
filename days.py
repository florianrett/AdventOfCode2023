import HelperFunctions as hf
import HelperClasses as hc
from ProgressBar import ProgressBar
from HelperClasses import Number
import typing
import collections
import copy
import numpy as np
import time
import ast
import math
from itertools import combinations, permutations
import operator
import re

def day1(input, Pbar: ProgressBar):
    
    elves = []

    current = 0
    for line in input:
        if line == "":
            elves.append(current)
            current = 0
        else:
            current += int(line)

    a = np.array(elves)
    largestInd = np.argpartition(a, -3)
    largest = a[largestInd[-3:]]

    return max(elves), sum(largest)

def day2(input, Pbar: ProgressBar):

    TotalScore = 0
    TotalScoreB = 0

    for line in input:
        left = line.split(' ')[0]
        right = line.split(' ')[1]

        if left == 'A':
            other = 0
        elif left == 'B':
            other = 1
        else:
            other = 2
        if right == 'X':
            self = 0
        elif right == 'Y':
            self = 1
        else:
            self = 2
        
        TotalScore += hf.PlayRockPaperScissors(self, other)

        if right == 'X':
            self = (other + 2) % 3
        elif right =='Y':
            self = other
        else:
            self = (other + 1) % 3
        
        TotalScoreB += hf.PlayRockPaperScissors(self, other)

    return TotalScore, TotalScoreB

def day3(input, Pbar: ProgressBar):

    TotalPrio = 0
    for line in input:
        num = int(len(line) / 2)
        items1 = set(line[:num])
        items2 = set(line[num:])
        
        matchedType = items1.intersection(items2).pop()
        if matchedType.isupper():
            TotalPrio += ord(matchedType) - 38
        else:
            TotalPrio += ord(matchedType) - 96

    TotalPrio2 = 0
    for i in range(len(input))[::3]:
        items1 = set(input[i])
        items2 = set(input[i+1])
        items3 = set(input[i+2])
        badge = items1.intersection(items2).intersection(items3).pop()
        
        if badge.isupper():
            TotalPrio2 += ord(badge) - 38
        else:
            TotalPrio2 += ord(badge) - 96

    return TotalPrio, TotalPrio2

def day4(input, Pbar: ProgressBar):

    FullOverlaps = 0
    PartialOverlaps = 0
    for pair in input:
        elf1 = pair.split(',')[0]
        elf2 = pair.split(',')[1]
        bounds1 = (int(elf1.split('-')[0]), int(elf1.split('-')[1]))
        bounds2 = (int(elf2.split('-')[0]), int(elf2.split('-')[1]))

        set1 = set(range(bounds1[0], bounds1[1]+1))
        set2 = set(range(bounds2[0], bounds2[1]+1))
        join = set1.union(set2)
        intersection = set1.intersection(set2)
        
        if len(join) == len(set1) or len(join) == len(set2):
            FullOverlaps += 1

        if len(intersection) > 0:
            PartialOverlaps += 1

    return FullOverlaps, PartialOverlaps

def day5(input, Pbar: ProgressBar):

    stacks = {}
    stacks2 = {}
    lineNr = 0
    while not input[lineNr].startswith(" 1"):
        # build initial stacks
        line = input[lineNr]
        stackIdx = 1
        for i in range(1, len(line), 4):
            if line[i] != ' ':
                if stackIdx not in stacks:
                    stacks[stackIdx] = []
                    stacks2[stackIdx] = []
                stacks[stackIdx].insert(0, line[i])
                stacks2[stackIdx].insert(0, line[i])
            stackIdx += 1

        lineNr += 1
    lineNr += 2
    
    while lineNr < len(input):
        move = input[lineNr].split(' ')
        num = int(move[1])
        fromS = int(move[3])
        toS = int(move[5])

        # puzzle 1 moving
        for i in range(num):
            stacks[toS].append(stacks[fromS].pop())

        # puzzle 2 moving
        lowestMovedIdx = len(stacks2[fromS]) - num        
        for i in range(num):
            stacks2[toS].append(stacks2[fromS].pop(lowestMovedIdx))
        lineNr += 1
        
    topCrates = ""
    topCrates2 = ""
    idx = 1
    while idx in stacks:
        topCrates += stacks[idx][-1]
        topCrates2 += stacks2[idx][-1]
        idx += 1

    return topCrates, topCrates2

def day6(input, Pbar: ProgressBar):
    signal = input[0]
    for i in range(3, len(signal)):
        marker = set(signal[i-3:i+1])
        if len(marker) == 4:
            startMarkerPos = i + 1 
            break

    startMessage = -1
    for j in range(13, len(signal)):
        marker = set(signal[j-13:j+1])
        if len(marker) == 14:
            startMessage = j + 1
            break

    return startMarkerPos, startMessage

def day7(input, Pbar: ProgressBar):
    currentDir = ""
    subdirs = {}
    files = {}

    for line in input:
        if line[0] == '$':
            cmd = line.split(' ')
            
            if cmd[1] == "cd":
                if cmd[2] == '/':
                    currentDir = "/"
                elif cmd[2] == "..":
                    parentEnd = currentDir.rfind('/', 0, -1)
                    currentDir = currentDir[:parentEnd + 1]
                else:
                    currentDir += cmd[2] + "/"
            elif cmd[1] == "ls":
                subdirs[currentDir] = []
                files[currentDir] = []
        else:
            # ls list
            item = line.split(' ')
            if item[0] == "dir":
                subdirs[currentDir].append(currentDir+item[1]+"/")
            else:
                files[currentDir].append((item[0], item[1]))

    sizes = {}
    hf.RecCalculateDirSizes("/", sizes, subdirs, files)
    
    totalSizeSmallDirs = 0
    for dir, size in sizes.items():
        if size <= 100000:
            totalSizeSmallDirs += size

    # part 2
    neededSpace = 30000000
    neededSpace -= 70000000 - sizes["/"]
    
    smallestDirSize = sizes["/"]
    for size in sizes.values():
        if size >= neededSpace and size < smallestDirSize:
            smallestDirSize = size


    return totalSizeSmallDirs, smallestDirSize

def day8(input, Pbar: ProgressBar):
    h = len(input)
    w = len(input[0])

    top = []
    right = []
    bottom = []
    left = []
    
    # calc visibilities
    for column in range(w):
        # from top
        top.append([])
        blockedHeight = -1
        for row in range(h):
            height = int(str(input[row])[column])
            if height > blockedHeight:
                top[column].append(True)
                blockedHeight = height
            else:
                top[column].append(False)
        # from bottom
        bottom.append([])
        blockedHeight = -1
        for row in reversed(range(h)):
            height = int(str(input[row])[column])
            if height > blockedHeight:
                bottom[column].append(True)
                blockedHeight = height
            else:
                bottom[column].append(False)
    for row in range(h):
        # from left
        left.append([])
        blockedHeight = -1
        for column in range(w):
            height = int(str(input[row])[column])
            if height > blockedHeight:
                left[row].append(True)
                blockedHeight = height
            else:
                left[row].append(False)
        # from right
        right.append([])
        blockedHeight = -1
        for column in reversed(range(w)):
            height = int(str(input[row])[column])
            if height > blockedHeight:
                right[row].append(True)
                blockedHeight = height
            else:
                right[row].append(False)

    numVisibleTrees = 0
    for y in range(h):
        revY  = h - y - 1
        for x in range(w):
            revX = w - x - 1
            if top[x][y] or bottom[x][revY] or left[y][x] or right[y][revX]:
                # print("Tree at", x, y, "is visible")
                numVisibleTrees += 1

    highestScenicScore = 0

    for y in range(h):
        for x in range(w):
            height = input[y][x]
            sLeft = 0
            sRight = 0
            sTop = 0
            sBottom = 0
            
            i = x - 1
            while i >= 0:
                sLeft += 1
                if input[y][i] >= height:
                    break
                i -= 1
            i = x + 1
            while i < w:
                sRight += 1
                if input[y][i] >= height:
                    break
                i += 1
            i = y - 1
            while i >= 0:
                sTop += 1
                if input[i][x] >= height:
                    break
                i -= 1
            i = y + 1
            while i < h:
                sBottom += 1
                if input[i][x] >= height:
                    break
                i += 1
            
            score = sLeft * sRight * sTop * sBottom
            if score > highestScenicScore:
                highestScenicScore = score

    return numVisibleTrees, highestScenicScore

def day9(input, Pbar: ProgressBar):

    currentHead = (0, 0)
    currentTail = (0, 0)
    tails = []
    for i in range(9):
        tails.append((0, 0))
    visited = set()
    visited2 = set()
    for line in input:
        dir = line[0]
        num = int(line[2:])

        for i in range(num):
            result = hf.MoveRope(currentHead, currentTail, dir)
            currentHead = result[0]
            currentTail = result[1]
            visited.add(currentTail)

            # part 2 longer rope
            tails[0] = result[1]
            for i in range(8):
                result = hf.MoveRope(tails[i], tails[i+1], '')
                tails[i+1] = result[1]
            visited2.add(tails[8])

    return len(visited), len(visited2)

def day10(input, Pbar: ProgressBar):
    cycle = 0
    regX = 1
    signalStrengths = []
    pixels = []
    for line in input:
        cycle += 1

        if cycle == 20 or cycle / 20 % 2 == 1:
            signalStrengths.append(regX * cycle)
            # print(cycle, regX)
        pixels.append('#' if abs(regX - (cycle - 1)  % 40) <= 1 else '.')
        # print(cycle, regX, pixels[-1])
        
        cmd = line.split(' ')
        if cmd[0] == "noop":
            pass
        elif cmd[0] == "addx":
            cycle += 1
            value = int(cmd[1])
            if cycle == 20 or cycle / 20 % 2 == 1:
                signalStrengths.append(regX * cycle)
                # print(cycle, regX)
            pixels.append('#' if abs(regX - (cycle - 1) % 40) <= 1 else '.')
            # print(cycle, regX, pixels[-1])
            regX += value
        
    for y in range(6):
        drawnLine = ""
        for x in range(40):
            drawnLine += pixels[y * 40 + x]
        print(drawnLine)

    total = sum(signalStrengths)
    return total, -1

def day11(input, Pbar: ProgressBar):

    Monkeys = []
    Monkeys2 = []
    for i in range(0, len(input), 7):
        items = [np.int64(x) for x in input[i+1].split(": ")[1].split(", ")]
        operation = input[i+2].split("= ")[1]
        test = input[i+3].split(' ')[-1]
        test = int(test)
        testTrue = input[i+4].split(' ')[-1]
        testTrue = int(testTrue)
        testFalse = input[i+5].split(' ')[-1]
        testFalse = int(testFalse)

        Monkeys.append(hc.Monkey(items.copy(), operation, test, testTrue, testFalse))
        Monkeys2.append(hc.Monkey(items.copy(), operation, test, testTrue, testFalse, False))
    
    for i in range(20):
        for m in Monkeys:
            throws = m.TakeTurn()
            for t in throws:
                Monkeys[t[1]].items.append(t[0])
        
        # print("After turn", i)
        # for j in range(len(Monkeys)):
        #     print("Monkey", j, ":", Monkeys[j].items)

    inspected = []
    for m in Monkeys:
        inspected.append(m.timesInspected)
    inspected.sort()
    inspected.reverse()
    MonkeyBusiness = inspected[0] * inspected[1]

    testProduct = np.prod([m.test for m in Monkeys2])
    for i in range(10000):
        for m in Monkeys2:
            throws = m.TakeTurn()
            for t in throws:
                Monkeys2[t[1]].items.append(t[0] % testProduct)
        
        # if i % 1000 == 0:
        #     print("After turn", i)
        #     for j in range(len(Monkeys2)):
        #         print("Monkey", j, " inspected", Monkeys2[j].timesInspected)
    
    inspected.clear()
    for m in Monkeys2:
        inspected.append(m.timesInspected)
    inspected.sort()
    inspected.reverse()
    MonkeyBusiness2 = inspected[0] * inspected[1]
    
    return MonkeyBusiness, MonkeyBusiness2

def day12(input, Pbar: ProgressBar):

    current = ()
    target = ()
    numX = len(input[0])
    numY = len(input)
    map = {}
    for x in range(numX):
        for y in range(numY):
            height = input[y][x]
            if height == 'S':
                height = 'a'
                current = (x, y)
            elif height == 'E':
                height = 'z'
                target = (x, y)
            map[(x, y)] = ord(height)

    # helper lambdas
    validX = lambda x : x >= 0 and x < numX
    validY = lambda y : y >= 0 and y < numY

    # depth first search
    visited = set()
    steps = {}
    steps[current] = 0
    candidates = []
    
    while current != target:
        visited.add(current)
        currentSteps = steps[current]
        # print(current, currentSteps)
        for offset in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor = (current[0] + offset[0], current[1] + offset[1])
            if validX(neighbor[0]) and validY(neighbor[1]):
                # print("neighbor:", neighbor, "dist:", map[neighbor] - map[current])
                if map[neighbor] - map[current] <= 1:
                    if neighbor in visited:
                        continue
                    if neighbor not in steps:
                        steps[neighbor] = currentSteps + 1
                        candidates.append(neighbor)
                    elif steps[neighbor] <= currentSteps + 1:
                        # 
                        pass
                    else:
                        print("This should never be reached!")
        # print("candidates: ", candidates)
        current = candidates.pop(0)
    shortestPath = steps[target]

    # part 2 depth first search
    current = target
    visited.clear()
    steps.clear()
    steps[current] = 0
    candidates = []
    candidates.append(target)
    shortestHikingPath = numX * numY
    
    while len(candidates) > 0:        
        current = candidates.pop(0)
        visited.add(current)
        currentSteps = steps[current]
        # print(current)
        if map[current] == ord('a'):
            if currentSteps < shortestHikingPath:
                shortestHikingPath = currentSteps
        # print(current, currentSteps)
        for offset in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor = (current[0] + offset[0], current[1] + offset[1])
            if validX(neighbor[0]) and validY(neighbor[1]):
                # print("neighbor:", neighbor, "dist:", map[neighbor] - map[current])
                if map[neighbor] - map[current] >= -1:
                    # print(neighbor)
                    if neighbor in visited:
                        continue
                    if neighbor not in steps:
                        steps[neighbor] = currentSteps + 1
                        candidates.append(neighbor)                        
                    elif steps[neighbor] <= currentSteps + 1:
                        # 
                        pass
                    else:
                        print("This should never be reached!")
        # print("candidates: ", candidates)

    return shortestPath, shortestHikingPath

def day13(input, Pbar: ProgressBar):

    pairInd = 0
    sum = 0
    packets = []
    for i in range(0, len(input), 3):
        pairInd += 1
        packet1 = ast.literal_eval(input[i])
        packet2 = ast.literal_eval(input[i+1])
        packets.append(packet1.copy())
        packets.append(packet2.copy())

        if hf.ComparePackets(packet1, packet2) == 1:
            sum += pairInd

    # part 2, sort packages
    sortedPackages = []
    for p in packets:
        bInserted = False
        for i in range(len(sortedPackages)):
            if hf.ComparePackets(p, sortedPackages[i]) == 1:
                sortedPackages.insert(i, p)
                bInserted = True
                break
        if not bInserted:
            sortedPackages.append(p)
    
    bFirstPacketInserted = False
    DecoderKey = 1
    for i in range(len(sortedPackages)):
        if not bFirstPacketInserted:
            if hf.ComparePackets([[2]], sortedPackages[i]) == 1:
                sortedPackages.insert(i, p)
                bFirstPacketInserted = True
                DecoderKey = i + 1
        else:
            if hf.ComparePackets([[6]], sortedPackages[i]) == 1:
                sortedPackages.insert(i, p)
                DecoderKey *= (i + 1)
                break

    return sum, DecoderKey

def day14(input, Pbar: ProgressBar):
    tiles = {}
    lowestRock = 0
    for line in input:
        path = line.split(" -> ")
        points = [(int(x.split(',')[0]), int(x.split(',')[1])) for x in path]
        
        for i in range(len(points) - 1):
            p = points[i]
            next = points[i+1]
            if p[0] == next[0]:
                x = p[0]
                dir = 1 if p[1] < next[1] else -1
                for i in range(p[1], next[1] + dir, dir):
                    tiles[(x, i)] = '#'
                    if i > lowestRock:
                        lowestRock = i
            elif p[1] == next[1]:
                y = p[1]
                if y > lowestRock:
                    lowestRock = y
                dir = 1 if p[0] < next[0] else -1
                for i in range(p[0], next[0] + dir, dir):
                    tiles[(i, y)] = '#'

    sandAtRest = 0
    solution1 = 0
    bFilled = False
    bActuallyFilled = False
    while not bActuallyFilled:
        pos = (500, 0)
        while True:
            if not bFilled and pos[1] >= lowestRock:
                bFilled = True
                solution1 = sandAtRest
                break
            elif (500, 0) in tiles:
                bActuallyFilled = True
                break
            if pos[1] == lowestRock + 1:
                sandAtRest += 1
                tiles[pos] = 'o'
                break
            next = (pos[0], pos[1] + 1)
            if next not in tiles:
                pos = next
                continue
            next = (pos[0] - 1, pos[1] + 1)
            if next not in tiles:
                pos = next
                continue
            next = (pos[0] + 1, pos[1] + 1)
            if next not in tiles:
                pos = next
                continue
            # sand came to rest
            sandAtRest += 1
            # print("sand at rest at", pos)
            tiles[pos] = 'o'
            break

    return solution1, sandAtRest

def day15(input, Pbar: ProgressBar):
    testY = 10
    maxCoord = 20
    if len(input) > 20:
        testY = 2000000
        maxCoord = 4000000


    sensors = [] # map of sensors to distance to closest beacon
    beacons = set()
    for line in input:
        Sx = int(line.split(',')[0].split('=')[1])
        Sy = int(line.split(':')[0].split('=')[2])
        Bx = int(line.split("x=")[2].split(',')[0])
        By = int(line.split('=')[-1])

        dist = abs(Bx - Sx) + abs(By - Sy)
        sensors.append([(Sx, Sy), dist])
        beacons.add((Bx, By))
    
    # puzzle 1
    numOccupied = hf.CheckLine(testY, sensors, -10000000, 1000000000)
    # remove all beacons in the tested line
    for b in beacons:
        if b[1] == testY:
            numOccupied -= 1

    # part 2
    frequency = -1
    for y in range(maxCoord + 1):
        if hf.CheckLine(y, sensors, 0, maxCoord) != maxCoord + 1:
            # found correct line
            for x in range(maxCoord + 1):
                bInRange = False
                for sensor in sensors:
                    if hf.IsInSensorRange((x, y), sensor[0], sensor[1]):
                        bInRange = True
                        break
                if not bInRange:
                    frequency = 4000000 * x + y
                    break
            break

    return numOccupied, frequency

def day16(input, Pbar: ProgressBar):
    allValves = []
    valveFlowRates = {}
    valveTunnels = {}
    for line in input:
        name = line.split(' ')[1]
        flow = int(line.split('=')[1].split(';')[0])
        if "tunnels lead to valves" in line:
            tunnels = line.split("valves ")[1].split(", ")
        else:
            tunnels = [line.split("valve ")[1]]
        
        # print(name, flow, tunnels)
        allValves.append(name)
        valveFlowRates[name] = flow
        valveTunnels[name]  = tunnels
    
    valves = [v for v in allValves if valveFlowRates[v] != 0]
    valves.append("AA") # add start valve to have valid start paths for graph traversal
    distances = {} # distances between all valves with posittive flow rates
    for i in range(len(valves)):
        for j in range(i + 1, len(valves)):
            v1 = valves[i]
            v2 = valves[j]
            # BFS until other valve is reached
            steps = 0
            visited = set()
            candidates = set()
            current = [v1]
            while True:
                if v2 in current:
                    break
                steps += 1
                visited.update(current)
                for c in current:
                    candidates.update(valveTunnels[c])
                current = candidates.copy()
                candidates.clear()
            distances[(v1, v2)] = steps
            distances[(v2, v1)] = steps

    valves.remove("AA")
    valves.sort(key= lambda x : valveFlowRates[x])
    valves.reverse()
    # print(valves)
    # print(distances)
    pressureReleased = hf.RecCalcPressure(valves, valveFlowRates, distances, "AA", 30)

    # part 2
    pressureReleased2 = -1
    valveSet = set(valves)
    
    # me and elefant both do half the valves. to avoid mirros I always open the valve wiht the highest flow rate
    highestFlowValve = valves.pop(0)
    MySets = list(combinations(valves, int(len(valves)  / 2)))
    MySets = [set(x).union([highestFlowValve]) for x in MySets]
    
    counter = 0
    num = len(MySets)
    for MySet in MySets:
        counter += 1
        print(counter, num)
        OtherSet = valveSet.difference(MySet)
        pressure1 = 0
        for perm in permutations(MySet):
            pressure1 = max(pressure1, hf.CalcPressureFixedPath(list(perm), valveFlowRates, distances, 26, "AA"))
        pressure2 = 0
        for perm2 in permutations(OtherSet):
            pressure2 = max(pressure2, hf.CalcPressureFixedPath(list(perm2), valveFlowRates, distances, 26, "AA"))
        
        pressureReleased2 = max(pressureReleased2, pressure1 + pressure2)

    return pressureReleased, pressureReleased2

def day17(input, Pbar: ProgressBar):

    jets = [1 if x == '>' else -1 for x in input[0]]
    rockTypes = [
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
        [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
        [(0, 0), (0, 1), (0, 2), (0, 3)],
        [(0, 0), (1, 0), (0, 1), (1, 1)]
    ]
    
    highestRock = 0
    rocks = set()
    rocks.update([(x, 0) for x in range(7)])
    jetIndex = 0
    typeIndex = 0

    knownStates = {}

    for i in range(2022):
        rock = rockTypes[typeIndex]
        typeIndex = (typeIndex + 1) % len(rockTypes)
        rockPos = (2, highestRock + 4)
        bAtRest = False
        while not bAtRest:
            # jet movement
            move = jets[jetIndex]
            jetIndex = (jetIndex + 1) % len(jets)
            newRockPos = (rockPos[0] + move, rockPos[1])
            if hf.IsRockPositionValid(newRockPos, rock, rocks):
                rockPos = newRockPos
            # else:
            #     print("blocked:", newRockPos)

            # fall movement
            newRockPos = (rockPos[0], rockPos[1] - 1)
            if hf.IsRockPositionValid(newRockPos, rock, rocks):
                rockPos = newRockPos
            else:
                bAtRest = True
                rocks.update([(rockPos[0] + x[0], rockPos[1] + x[1]) for x in rock])
                for o in rock:
                    rocks.add((rockPos[0] + o[0], rockPos[1] + o[1]))
                    highestRock = max(highestRock, rockPos[1] + o[1])
                # print("Rock", i, "came at rest at", rockPos)
    result1 = highestRock

    # part 2
    highestRock = 0
    rocks = set()
    rocks.update([(x, 0) for x in range(7)])
    jetIndex = 0
    typeIndex = 0
    
    numIterations = 1000000000000
    for i in range(numIterations):
        rock = rockTypes[typeIndex]
        typeIndex = (typeIndex + 1) % len(rockTypes)
        rockPos = (2, highestRock + 4)
        bAtRest = False
        while not bAtRest:
            # jet movement
            move = jets[jetIndex]
            jetIndex = (jetIndex + 1) % len(jets)
            newRockPos = (rockPos[0] + move, rockPos[1])
            if hf.IsRockPositionValid(newRockPos, rock, rocks):
                rockPos = newRockPos
            # else:
            #     print("blocked:", newRockPos)

            # fall movement
            newRockPos = (rockPos[0], rockPos[1] - 1)
            if hf.IsRockPositionValid(newRockPos, rock, rocks):
                rockPos = newRockPos
            else:
                bAtRest = True
                rocks.update([(rockPos[0] + x[0], rockPos[1] + x[1]) for x in rock])
                for o in rock:
                    rocks.add((rockPos[0] + o[0], rockPos[1] + o[1]))
                    highestRock = max(highestRock, rockPos[1] + o[1])
                # print("Rock", i, "came at rest at", rockPos)

        heightList = []
        bValidState = True
        for x in range(7):
            bColumnValid = False
            for y in range(4):
                if (x, y) in rocks:
                    bColumnValid = True
                    heightList.append(True)
                else:
                    heightList.append(False)
            if not bColumnValid:
                bValidState = False
                break

        if bValidState:
            heights = (heightList[0], heightList[1], heightList[2], heightList[3], heightList[4], heightList[5], heightList[6],
            heightList[7], heightList[8], heightList[9], heightList[10], heightList[11], heightList[12], heightList[13],
            heightList[14], heightList[15], heightList[16], heightList[17], heightList[18], heightList[19], heightList[20],            
            heightList[21], heightList[22], heightList[23], heightList[24], heightList[25], heightList[26], heightList[27])
            currentState = (jetIndex, typeIndex, heights)
            if currentState in knownStates:
                steps = i - knownStates[currentState][0]
                growth = highestRock - knownStates[currentState][1]
                print("known state found after", i, "rocks. Growth:", growth, "in", steps)
                # extrapolate if this can perfectly reach target iterations
                remainingIterations = numIterations - i - 1
                if remainingIterations % steps == 0:
                    extrapolationSteps = math.floor(remainingIterations / steps)
                    i += extrapolationSteps * steps
                    highestRock += growth * extrapolationSteps
                    break                  
            else:
                knownStates[currentState] = (i, highestRock)

    result2 = highestRock

    return result1, result2

def day18(input, Pbar: ProgressBar):

    drops = set()
    maxExtent = 0
    for line in input:
        coords = [int(x) for x in line.split(',')]
        drops.add((coords[0], coords[1], coords[2]))
        maxExtent = max(maxExtent, max(coords))
        
    adjacent = set(permutations([1, 0, 0]))
    adjacent.update(set(permutations([-1, 0, 0])))
    emptyNeighbors = set()
    numSidesExposed = 0
    for d in drops:
        for a in adjacent:
            neighbor = (d[0] + a[0], d[1] + a[1], d[2] + a[2])
            if neighbor not in drops:
                numSidesExposed += 1
                emptyNeighbors.add(neighbor)
        pass

    # part 2
    exteriorSides = numSidesExposed
    outerCubes = set()
    for n in emptyNeighbors:
        bIsOuter = False
        for a in adjacent:
            bFoundDrop = False
            for i in range(1, maxExtent): # find drop within n cubes
                neighbor = (n[0] + i * a[0], n[1] + i * a[1], n[2] + i * a[2])
                if neighbor in drops:
                    bFoundDrop = True
                    break
            if not bFoundDrop:
                bIsOuter = True
                break
        if bIsOuter:
            outerCubes.add(n)

    innerCubeCandidates = emptyNeighbors.difference(outerCubes)
    bKeepSearching = True
    while bKeepSearching:
        bKeepSearching = False
        newOuterCubes = set()
        for o in outerCubes:
            for a in adjacent:
                n = (o[0] + a[0], o[1] + a[1], o[2] + a[2])
                if n in innerCubeCandidates:
                    innerCubeCandidates.remove(n)
                    newOuterCubes.add(n)
                    bKeepSearching = True
        outerCubes.update(newOuterCubes)

    for c in innerCubeCandidates:
        for a in adjacent:
            neighbor = (c[0] + a[0], c[1] + a[1], c[2] + a[2])
            if neighbor in drops:
                exteriorSides -= 1
            
    return numSidesExposed, exteriorSides

def day19(input, Pbar: ProgressBar):

    Pbar.StartPuzzle1(len(input))
    Blueprints = []
    for bp in input:
        s = bp.split(' ')
        ore = int(s[6])
        clay = int(s[12])
        obsidianOre = int(s[18])
        obsidianClay = int(s[21])
        geodeOre = int(s[27])
        geodeObsidian = int(s[30])

        Blueprints.append((ore, clay, obsidianOre, obsidianClay, geodeOre, geodeObsidian))
        
    QualityLevels = []

    for i in range(len(Blueprints)):
        Pbar.SetProgress(i)
        Factory = hc.RobotFactory(Blueprints[i], 24)
        NumGeodes = Factory.FindOptimum()
        
        QualityLevel = (i + 1) * NumGeodes
        QualityLevels.append(QualityLevel)

    Pbar.StartPuzzle2(3)

    GeodeNumbers2 = []
    for i in range(3):
        Pbar.SetProgress(i)
        Factory = hc.RobotFactory(Blueprints[i], 32)
        NumGeodes = Factory.FindOptimum()
        GeodeNumbers2.append(NumGeodes)
    
    Pbar.FinishPuzzle2()

    Solution2 = np.prod(GeodeNumbers2)

    return sum(QualityLevels), Solution2

def day20(input, Pbar: ProgressBar):
    numbers = [Number(x) for x in input]
    num = len(numbers)

    Pbar.StartPuzzle1(1)
    mixedNumbers = hf.MixNumbers(numbers, Pbar, 1)
    mixedInts = [x.Value for x in mixedNumbers]
    
    ind0 = mixedInts.index(0)
    coords = []
    coords.append(mixedInts[(ind0 + 1000) % num])
    coords.append(mixedInts[(ind0 + 2000) % num])
    coords.append(mixedInts[(ind0 + 3000) % num])

    # part 2
    Pbar.StartPuzzle2(10)
    key = 811589153
    numbers2 = [Number(x.Value * key) for x in numbers]
    mixed2 = [x.Value for x in hf.MixNumbers(numbers2, Pbar, 10)]
    ind0 = mixed2.index(0)
    coords2 = []
    coords2.append(mixed2[(ind0 + 1000) % num])
    coords2.append(mixed2[(ind0 + 2000) % num])
    coords2.append(mixed2[(ind0 + 3000) % num])

    Pbar.FinishPuzzle2()

    return sum(coords), sum(coords2)

def day21(input, Pbar: ProgressBar):

    monkeys = {x.split(": ")[0]: x.split(": ")[1].split(' ') for x in input}

    unsolvedMonkeys = set(monkeys.keys())
    
    solvedMonkeys = {x: int(monkeys[x][0]) for x in unsolvedMonkeys if monkeys[x][0].isdigit()}
    for x in solvedMonkeys:
        unsolvedMonkeys.remove(x)

    Pbar.StartPuzzle1(len(unsolvedMonkeys))

    ops = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.floordiv}
    while unsolvedMonkeys:
        for m in unsolvedMonkeys:
            expr = monkeys[m]
            if expr[0] in solvedMonkeys and expr[2] in solvedMonkeys:
                op = ops[expr[1]]
                result = op(solvedMonkeys[expr[0]], solvedMonkeys[expr[2]])
                # print(f"{m} yells number {result}")
                solvedMonkeys[m] = result
                unsolvedMonkeys.remove(m)
                break
    solution1 = solvedMonkeys["root"]
    
    # part 2
    Pbar.StartPuzzle2(0)

    unsolvedMonkeys = set(monkeys.keys())
    solvedMonkeys = {x: int(monkeys[x][0]) for x in unsolvedMonkeys if monkeys[x][0].isdigit() and x != "humn"}
    for x in solvedMonkeys:
        unsolvedMonkeys.remove(x)

    # solve as far as possible
    while unsolvedMonkeys:
        bCouldSolve = False
        for m in unsolvedMonkeys:
            expr = monkeys[m]            
            if expr[0] in solvedMonkeys and expr[2] in solvedMonkeys:
                op = ops[expr[1]]
                result = op(solvedMonkeys[expr[0]], solvedMonkeys[expr[2]])
                # print(f"{m} yells number {result}")
                solvedMonkeys[m] = result
                unsolvedMonkeys.remove(m)
                bCouldSolve = True
                break
        if not bCouldSolve:
            break

    revOps = {"+": operator.sub, "-": operator.add, "*": operator.floordiv, "/": operator.mul}
    # solve recursively assuming there is always one number known
    current = "root"
    targetValue = -1
    left = monkeys[current][0]
    right = monkeys[current][2]
    if left in solvedMonkeys:
        targetValue = solvedMonkeys[left]
        current = right
    else:
        targetValue = solvedMonkeys[right]
        current = left
    
    while current != "humn":
        left = monkeys[current][0]
        right = monkeys[current][2]
        if left in solvedMonkeys:
            # x = l - r --> r = l - x
            # x = l + r --> r = x - l
            # x = l * r --> r = x / l
            # x = l / r --> r = l / x
            opStr = monkeys[current][1]
            if opStr == "-":
                targetValue = solvedMonkeys[left] - targetValue
            elif opStr == "+":
                targetValue = targetValue - solvedMonkeys[left]
            elif opStr == "*":
                targetValue = targetValue // solvedMonkeys[left]
            elif opStr == "/":
                targetValue = solvedMonkeys[left] // targetValue
            else:
                print(f"unknown operator {opStr}!")                
            current = right
            pass
        elif right in solvedMonkeys:
            # x = l - r --> l = x + r
            # x = l + r --> l = x - r
            # x = l * r --> l = x / r
            # x = l / r --> l = x * r
            op = revOps[monkeys[current][1]]
            targetValue = op(targetValue, solvedMonkeys[right])
            current = left
            pass
        else:
            print(f"{current}: Neither partial monkey is solved: {left}, {right}")
            break

        pass


    Pbar.FinishPuzzle2()

    return solution1, targetValue

def day22(input, Pbar: ProgressBar):

    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)] # e, s, w, n

    map  = {}
    for i in range(len(input) - 1):
        line = input[i]
        for x in range(len(line)):
            if line[x] == ' ':
                continue
            else:
                map[(x, i)] = line[x]
    
    instructions = re.split(r"(R|L)", input[-1])

    pos = (0, 0)
    facing = 0 # start facing east
    while pos not in map or map[pos] == '#':
        pos = (pos[0] + 1, 0)
    
    Pbar.StartPuzzle1(len(instructions))

    for ins in instructions:

        if ins == 'L':
            facing -= 1
            facing %= 4
        elif ins == 'R':
            facing += 1
            facing %= 4
        else:
            dir = dirs[facing]
            for i in range(int(ins)):
                next = (pos[0] + dir[0], pos[1] + dir[1])
                if next in map:
                    if map[next] == '#':
                        # ran into wall
                        break
                    else:
                        pos = next       
                else:
                    # wrap around
                    opDir = (dir[0] * -1, dir[1] * -1)
                    next = pos
                    while next in map:
                        wrap = next
                        next = (wrap[0] + opDir[0], wrap[1] + opDir[1])
                    if map[wrap] == '#':
                        break
                    else:
                        pos = wrap

        Pbar.IncrementProgress()

    row1 = pos[1] + 1
    column1 = pos[0] + 1
    password1 = 1000 * row1 + 4 * column1 + facing


    Pbar.StartPuzzle2(len(instructions))

    bIsUsingTestInput = len(input[0]) == 12
    pos = (0, 0)
    facing = 0 # start facing east
    while pos not in map or map[pos] == '#':
        pos = (pos[0] + 1, 0)

    for ins in instructions:
        if ins == 'L':
            facing -= 1
            facing %= 4
        elif ins == 'R':
            facing += 1
            facing %= 4
        else:
            for i in range(int(ins)):
                dir = dirs[facing]
                next = (pos[0] + dir[0], pos[1] + dir[1])
                # print(f"nextPos: {next}")
                if next in map:
                    if map[next] == '#':
                        # ran into wall
                        break
                    else:
                        pos = next
                else:
                    # cube wrapping. Actual mapping needs to be customized for specific input layout
                    if bIsUsingTestInput:
                        wrap = hf.CubeWrapTestinput(next, facing)
                    else:
                        wrap = hf.CubeWrapMyInput(next, facing)

                    if wrap[0] not in map:
                        print(dir, facing, dirs[facing])
                        print(pos, facing, next, wrap)
                    next = wrap[0]
                    # print(f"wrap from {pos} to {next} (dir: {dir}")
                    if map[next] == '#':
                        # print("wall wrap")
                        break
                    else:
                        pos = next
                        facing = wrap[1]
        # print(ins, pos, facing)
        Pbar.IncrementProgress()
    
    row = pos[1] + 1
    column = pos[0] + 1
    password2 = 1000 * row + 4 * column + facing
        
    Pbar.FinishPuzzle2()

    return password1, password2

def day23(input, Pbar: ProgressBar):

    elves = set()
    for y in range(len(input)):
        for x in range(len(input[y])):
            if input[y][x] == '#':
                elves.add((x, y * -1))

    Pbar.StartPuzzle1(10)

    positions = elves.copy()
    for i in range(10):
        Pbar.SetProgress(i)
        positions = hf.UpdateElfPositions(positions, i % 4)

    minX, maxX, minY, maxY = 0, 0, 0, 0
    for p in positions:
        minX = min(minX, p[0])
        maxX = max(maxX, p[0])
        minY = min(minY, p[1])
        maxY = max(maxY, p[1])

    emptyTiles = 0
    for y in range(maxY, minY - 1, -1):
        line = ""
        for x in range(minX, maxX + 1):
            if (x, y) in positions:
                # line += "#"
                pass
            else:
                # line += "."
                emptyTiles += 1
        # print(line)

    Pbar.StartPuzzle2(1000)

    positions = elves.copy()
    numRounds = 0
    while True:
        Pbar.SetProgress(numRounds)
        newPositions = hf.UpdateElfPositions(positions, numRounds % 4)
        numRounds += 1
        if len(newPositions.difference(positions)) == 0:
            break
        positions = newPositions

    Pbar.FinishPuzzle2()

    return emptyTiles, numRounds

def day24(input, Pbar: ProgressBar):

    blizzardsLeft, blizzardsRight, blizzardsUp, blizzardsDown = set(), set(), set(), set()
    wallLeft, wallRight, wallTop, wallBottom = 0, len(input[0]) - 1, 0, len(input) - 1
    
    for y in range(1, len(input) - 1):
        line = input[y]
        for x in range(1, len(line) - 1):
            if line[x] == '<':
                blizzardsLeft.add((x, y))
            elif line[x] == '>':
                blizzardsRight.add((x, y))
            elif line[x] == '^':
                blizzardsUp.add((x, y))
            elif line[x] == 'v':
                blizzardsDown.add((x, y))
            
        
    Pbar.StartPuzzle1(1000)

    startPos = (1, 0)
    targetPos = (wallRight - 1, wallBottom)
    left = blizzardsLeft.copy()
    right = blizzardsRight.copy()
    up = blizzardsUp.copy()
    down = blizzardsDown.copy()

    numMoves = 0
    moves = [(0, 0), (-1, 0), (1, 0), (0, 1), (0, -1)] # possible moves: wait, left, right, up, down
    possiblePositions = set()
    possiblePositions.add(startPos)
    while True:
        Pbar.SetProgress(numMoves)
        numMoves += 1
        # move blizzards
        left = set([(x[0] - 1, x[1]) if x[0] - 1 > wallLeft else (wallRight - 1, x[1]) for x in left])
        right = set([(x[0] + 1, x[1]) if x[0] + 1 < wallRight else (wallLeft + 1, x[1]) for x in right])
        up = set([(x[0], x[1] - 1) if x[1] - 1 > wallTop else (x[0], wallBottom - 1) for x in up])
        down = set([(x[0], x[1] + 1) if x[1] + 1 < wallBottom else (x[0], wallTop + 1) for x in down])
        
        # print(numMoves - 1, possiblePositions)
        newPositions = set()
        for p in [(x[0] + m[0], x[1] + m[1]) for x in possiblePositions for m in moves]:
            if p[0] <= wallLeft or p[0] >= wallRight or (p[1] >= wallBottom and p != targetPos) or (p[1] <= wallTop and p != startPos):
                continue
            elif p in left or p in right or p in up or p in down:
                continue
            else:
                newPositions.add(p)

        possiblePositions = newPositions
        if targetPos in possiblePositions:
            break
    solution1 = numMoves

    Pbar.StartPuzzle2(1000)

    possiblePositions.clear()
    possiblePositions.add(targetPos)
    while True:
        Pbar.SetProgress(numMoves)
        numMoves += 1
        # move blizzards
        left = set([(x[0] - 1, x[1]) if x[0] - 1 > wallLeft else (wallRight - 1, x[1]) for x in left])
        right = set([(x[0] + 1, x[1]) if x[0] + 1 < wallRight else (wallLeft + 1, x[1]) for x in right])
        up = set([(x[0], x[1] - 1) if x[1] - 1 > wallTop else (x[0], wallBottom - 1) for x in up])
        down = set([(x[0], x[1] + 1) if x[1] + 1 < wallBottom else (x[0], wallTop + 1) for x in down])
        
        newPositions = set()
        for p in [(x[0] + m[0], x[1] + m[1]) for x in possiblePositions for m in moves]:
            if p[0] <= wallLeft or p[0] >= wallRight or (p[1] >= wallBottom and p != targetPos) or (p[1] <= wallTop and p != startPos):
                continue
            elif p in left or p in right or p in up or p in down:
                continue
            else:
                newPositions.add(p)

        possiblePositions = newPositions
        if startPos in possiblePositions:
            break
    possiblePositions.clear()
    possiblePositions.add(startPos)
    while True:
        Pbar.SetProgress(numMoves)
        numMoves += 1
        # move blizzards
        left = set([(x[0] - 1, x[1]) if x[0] - 1 > wallLeft else (wallRight - 1, x[1]) for x in left])
        right = set([(x[0] + 1, x[1]) if x[0] + 1 < wallRight else (wallLeft + 1, x[1]) for x in right])
        up = set([(x[0], x[1] - 1) if x[1] - 1 > wallTop else (x[0], wallBottom - 1) for x in up])
        down = set([(x[0], x[1] + 1) if x[1] + 1 < wallBottom else (x[0], wallTop + 1) for x in down])
        
        newPositions = set()
        for p in [(x[0] + m[0], x[1] + m[1]) for x in possiblePositions for m in moves]:
            if p[0] <= wallLeft or p[0] >= wallRight or (p[1] >= wallBottom and p != targetPos) or (p[1] <= wallTop and p != startPos):
                continue
            elif p in left or p in right or p in up or p in down:
                continue
            else:
                newPositions.add(p)

        possiblePositions = newPositions
        if targetPos in possiblePositions:
            break
        
    Pbar.FinishPuzzle2()

    return solution1, numMoves

def day25(input, Pbar: ProgressBar):

    SNAFUtoDecimal = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
    DecimalToSNAFU = {v: k for k, v in SNAFUtoDecimal.items()}

    Pbar.StartPuzzle1(len(input))
    
    totals = {} # dict of power indices to list of individual values
    for line in input:
        Pbar.IncrementProgress()

        for i in range(len(line)):
            if i not in totals:
                totals[i] = []

            totals[i].append(SNAFUtoDecimal[line[-1 * (i  + 1)]])
    
    indices = list(totals.keys())
    indices.sort()

    result = ""
    overflow = 0
    for i in indices:
        total = sum(totals[i]) + overflow
        overflow = (total + 2) // 5
        digit = total - overflow * 5

        result = DecimalToSNAFU[digit] + result
    
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return result, "Merry Christmas!"