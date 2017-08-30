
import sys
from collections import Counter

char_Z, Z_char = Counter(), Counter()
validActions = set(['', 'north', 'south', 'east', 'west', 'alpha', 'beta', 'gamma', 'delta'])

class StarFleet(object):
    def __init__(self):
        self.mines = set()
        self.nMines = 0
        self.shipX, self.shipY, self.shipZ = 0, 0, 0
        self.steps = []
        self.step = 1
        self.volleys = 0
        self.moves = 0
        
        # maintain an boolean array of location of mines at different depths
        # and the index of the mine at the highest depth in the cuboid
        self.arr = [0]*53
        self.minIndex = float('inf')

    def parseGrid(self, fieldLines):
        """
        parse grid to build the mines collection
        """
        r, c = len(fieldLines), len(fieldLines[0])
        if r%2 == 0 or c%2 == 0:
            raise ValueError("The mine grid does not have a well defined center")

        self.shipX, self.shipY = c/2, r/2
        for i in range(r):
            if len(fieldLines[i]) != c:
                raise ValueError("Lines in field file do not have same length")
            
            for j in range(c):
                if fieldLines[i][j].isalpha():
                    self.mines.add((j, i, char_Z[fieldLines[i][j]]))
                    self.minIndex = min(self.minIndex, -char_Z[fieldLines[i][j]])
                    self.arr[-char_Z[fieldLines[i][j]]] = 1
                    self.nMines += 1
                elif fieldLines[i][j] != ".":
                    raise ValueError("Invalid character in field file")
    
    def parseScript(self, scriptLines):
        """
        parse script lines to build the steps list
        """
        for line in scriptLines:
            line = " ".join(line.strip().split())
            commands = line.split()
            if len(commands) > 2:
                raise ValueError("Invalid command sequence in script file")
            step = []
            for command in commands:
                if command not in validActions:
                    raise ValueError("command {0} not recognized in script file".format(command))
                step.append(command)
            self.steps.append(step)
    
    def displayGrid(self):
        """
        displays the current state of the mine grid
        """
        x, y = 0, 0
        for mine in self.mines:
            x = max(x, abs(mine[0] - self.shipX))
            y = max(y, abs(mine[1] - self.shipY))
        
        grid = [['.' for i in range(2*x+1)] for j in range(2*y+1)]
        for mine in self.mines:
            grid[mine[1] - self.shipY + y][mine[0] - self.shipX + x] = Z_char.get(self.shipZ - mine[2], '*')
        
        for row in grid:
            print "".join(row)
    
    def updateMinIndex(self):
        while self.minIndex < 53 and self.arr[self.minIndex] != 1:
            self.minIndex += 1
    
    def fireAlpha(self):
        """
        alpha firing pattern
        """
        destroyedMines = set()
        for mine in self.mines:
            if mine[0] == self.shipX - 1:
                if mine[1] == self.shipY - 1 or mine[1] == self.shipY + 1:
                    destroyedMines.add(mine)
                    self.arr[-mine[2]] = 0
                    if -mine[2] == self.minIndex:
                        self.updateMinIndex()
            elif mine[0] == self.shipX + 1:
                if mine[1] == self.shipY - 1 or mine[1] == self.shipY + 1:
                    destroyedMines.add(mine)
                    self.arr[-mine[2]] = 0
                    if -mine[2] == self.minIndex:
                        self.updateMinIndex()

        self.mines -= destroyedMines
        self.volleys += 1
    
    def fireBeta(self):
        """
        beta firing pattern
        """
        destroyedMines = set()
        for mine in self.mines:
            if mine[0] == self.shipX:
                if mine[1] == self.shipY - 1 or mine[1] == self.shipY + 1:
                    destroyedMines.add(mine)
                    self.arr[-mine[2]] = 0
                    if -mine[2] == self.minIndex:
                        self.updateMinIndex()
            elif mine[1] == self.shipY:
                if mine[0] == self.shipX - 1 or mine[0] == self.shipX + 1:
                    destroyedMines.add(mine)
                    self.arr[-mine[2]] = 0
                    if -mine[2] == self.minIndex:
                        self.updateMinIndex()

        self.mines -= destroyedMines
        self.volleys += 1
    
    def fireGamma(self):
        """
        gamma firing pattern
        """
        destroyedMines = set()
        for mine in self.mines:
            if mine[1] == self.shipY:
                if mine[0] >= self.shipX - 1 and mine[0] <= self.shipX + 1:
                    destroyedMines.add(mine)
                    self.arr[-mine[2]] = 0
                    if -mine[2] == self.minIndex:
                        self.updateMinIndex()
        
        self.mines -= destroyedMines
        self.volleys += 1
    
    def fireDelta(self):
        """
        delta firing pattern
        """
        destroyedMines = set()
        for mine in self.mines:
            if mine[0] == self.shipX:
                if mine[1] >= self.shipY - 1 and mine[1] <= self.shipY + 1:
                    destroyedMines.add(mine)
                    self.arr[-mine[2]] = 0
                    if -mine[2] == self.minIndex:
                        self.updateMinIndex()
        
        self.mines -= destroyedMines
        self.volleys += 1
    
    def navigate(self):
        """
        executes a line of commands in the script file
        """
        for command in self.steps[self.step-1]:
            # fire volley commands
            if command == "alpha":
                self.fireAlpha()
            elif command == "beta":
                self.fireBeta()
            elif command == "gamma":
                self.fireGamma()
            elif command == "delta":
                self.fireDelta()
            # move commands
            else:
                self.moves += 1
                if command == "north":
                    self.shipY -= 1  
                elif command == "south":
                    self.shipY += 1
                elif command == "east":
                    self.shipX += 1
                elif command == "west":
                    self.shipX -= 1
        self.shipZ -= 1
    
    def passedMine(self):
        """
        returns True if a mine is above or at the same depth as the ship
        """
        if -self.minIndex >= self.shipZ:
            return True
        return False

    def score(self):
        """
        prints the score of the simulation run
        """
        if self.passedMine():
            print ("fail (0)")
        elif len(self.mines) > 0 and self.step > len(self.steps):
            print ("fail (0)")
        elif len(self.mines) == 0 and self.step <= len(self.steps):
            print ("pass (1)")
        else:
            score = self.nMines * 10 - min(self.volleys*5, self.nMines*5) - \
            min(self.moves*2, self.nMines*3)
            print "pass ({0})".format(score)

def main():
    if len(sys.argv) < 3:
        print ("Input files missing; expected Field file and Script file")
        sys.exit(1)

    fieldFile, scriptFile = sys.argv[1], sys.argv[2]
    try:
        fieldR = open(fieldFile, 'r')
        fieldLines = fieldR.read().splitlines()
        
        scriptR = open(scriptFile, 'r')
        scriptLines = scriptR.read().splitlines()
        
        fieldR.close()
        scriptR.close()
    except IOError:
        print("Wrong file path or file not found")
    
    # build the char to Z map
    for i in range(65, 91):
        char_Z[chr(i)] = (-1)*(i-38)
    for i in range(97, 123):
        char_Z[chr(i)] = (-1)*(i-96)
    
    # build the Z to char map
    for i in range(1, 27):
        Z_char[i] = chr(i+96)
    for i in range(27, 53):
        Z_char[i] = chr(i+38)
    
    # initialize StartFleet object
    sf = StarFleet()

    # parse fieldLines
    sf.parseGrid(fieldLines)
    
    # parse scriptLines
    sf.parseScript(scriptLines)
    
    # run the simulation
    while sf.step <= len(sf.steps) and len(sf.mines) > 0 and not sf.passedMine():
        print "Step ", sf.step
        print ("")
        sf.displayGrid()
        print ("")
        print " ".join(sf.steps[sf.step-1])
        sf.navigate()
        print ("")
        sf.displayGrid()
        print ("")
        sf.step += 1
    
    # print the score of the simulation run
    sf.score()

if __name__ == '__main__':
    main()
