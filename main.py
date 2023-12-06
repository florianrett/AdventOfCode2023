import requests
import days
from ProgressBar import ProgressBar

day = 25
bUseTestInput = False

if bUseTestInput:
    print("Loading test input from file")
    f = open("testinput.txt", "r")
    input = f.read().splitlines()
    f.close()
else:    
    url = 'https://adventofcode.com/2022/day/' + str(day) + '/input'
    print("Loading input from AoC: " + url)

    f = open("sessioncookie.txt", "r")
    aocsession = {'session' : f.read().splitlines()[0]}
    f.close()    
    
    response = requests.get(url, cookies = aocsession)
    if response.status_code == 200:
        input = response.text.split('\n')
        input.pop()
    else:
        print("Web request failed! Check if session cookie is valid")
        print(response.status_code)
        print(response.text)

Bar = ProgressBar()
funcname = 'day' + str(day)
result = getattr(days, funcname)(input, Bar)

print(f"Puzzle 1 result: {result[0]} ({Bar.GetTimePuzzle1():.2} s)")
print(f"Puzzle 2 result: {result[1]} ({Bar.GetTimePuzzle2():.2} s)")
