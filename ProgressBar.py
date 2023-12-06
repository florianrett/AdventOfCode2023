import time
from sys import stdout

class ProgressBar:

    CurrentProgress = 0
    CurrentIteration: int
    TotalIterations: int

    CurrentPrefix = ""

    Puzzle1start: float
    Puzzle2start: float
    Puzzle1end: float
    Puzzle2end: float

    def __init__(self) -> None:
        self.CurrentProgress = 0
        self.CurrentIteration = 0
        self.TotalIterations = 0
        self.Puzzle1start = 0
        self.Puzzle1end = 0
        self.Puzzle2end = 0
        self.Puzzle2end = 0

        pass

    def StartPuzzle1(self, NumIterations: int):
        self.TotalIterations = NumIterations
        self.ResetProgress()

        self.Puzzle1start = time.time()
        self.CurrentPrefix = "Calculating Puzzle 1"

        pass

    def StartPuzzle2(self, NumIterations: int):
        self.Puzzle1end = time.time()
        self.FlushProgressBar()

        self.TotalIterations = NumIterations
        self.ResetProgress()

        self.Puzzle2start = time.time()
        self.CurrentPrefix = "Calculating Puzzle 2"

        pass

    def FinishPuzzle2(self):
        self.Puzzle2end = time.time()
        self.FlushProgressBar()

        pass

    def GetTimePuzzle1(self) -> float:
        return self.Puzzle1end - self.Puzzle1start

    def GetTimePuzzle2(self) -> float:
        return self.Puzzle2end - self.Puzzle2start

    def ResetProgress(self):
        self.CurrentIteration = 0
        self.CurrentProgress = 0

        pass

    def SetProgress(self, CompletedIterations: int):
        self.CurrentIteration = CompletedIterations
        self.UpdateProgress()

        pass

    def IncrementProgress(self):
        self.CurrentIteration += 1
        self.UpdateProgress()

        pass

    def UpdateProgress(self):
        Progress = self.CurrentIteration / self.TotalIterations
        if Progress - self.CurrentProgress >= 0.01:
            self.CurrentProgress = Progress
            self.PrintProgressBar()

        pass

    def FlushProgressBar(self):
        # remove current written line with ansi escape char: https://stackoverflow.com/questions/5290994/remove-and-replace-printed-items
        stdout.write('\033[K')
        pass

    def PrintProgressBar(self):

        self.PrintProgressBarInternal(self.CurrentIteration, self.TotalIterations, prefix = self.CurrentPrefix)

        pass


    # Print iterations progress from https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters/13685020
    def PrintProgressBarInternal(self, iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        if iteration != total:
            print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)

        # Print New Line on Complete
        # if iteration == total:
        #     print()