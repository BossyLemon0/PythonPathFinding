import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path finding algo")

WHITE = (255, 255, 255)
BLACK = (0,0,0)
ORANGE = (255, 156, 57)
TURQOISE = (74, 255, 250)
ICEDBLUE = (169, 255, 247)
LIGHTGREEN = (148, 251, 171)
CAMBRIDGEBLUE = (130, 171, 161)
ULTRAVIOLET = (82, 81, 116)
DARKPURPLE = (66, 17, 60)
PAYNESGREY = (82, 91, 118)


class Square:
    def __init__(self, row, col, width, totalRows):
        self.row = row
        self.col = col 
        self.width = width
        self.x = row * width
        self.y = col * width
        self.totalRows = totalRows
        self.neigbors = []
        self.color  = WHITE

    def getPos(self):
        return self.row, self.col
    
    def isLookedAt(self):
        return self.color == ICEDBLUE
    
    def nextToSearch(self):
        return self.color == LIGHTGREEN
        
    def isBarrier(self):
        return self.color == CAMBRIDGEBLUE
    
    def isStart(self):
        return self.color == ORANGE
    
    def isEnd(self):
        return self.color == DARKPURPLE
    
    def reset(self):
        self.color = WHITE
    
    def makeIsLookedAt(self):
        self.color = ICEDBLUE
    
    def makeIsNextToSearch(self):
        self.color = LIGHTGREEN
        
    def makeIsBarrier(self):
        self.color = CAMBRIDGEBLUE
    
    def makeIsStart(self):
        self.color = ORANGE
    
    def makeIsEnd(self):
        self.color = DARKPURPLE

    def makePath (self):
        self.color = ORANGE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def updateNeigbors(self, grid):
        #CHECK IF NEIGHBOR
        self.neigbors = []
        if self.row < self.totalRows - 1 and not grid[self.row + 1][self.col].isBarrier(): #down
            self.neigbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].isBarrier(): #up
            self.neigbors.append(grid[self.row - 1][self.col])

        if self.col < self.totalRows - 1 and not grid[self.row][self.col + 1].isBarrier(): #right
            self.neigbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col  - 1].isBarrier(): #left
            self.neigbors.append(grid[self.row][self.col - 1])
    
    def __lt__(self, other):
        return False


#heuristic function/ manhattan distance formula
def h(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

#current starts from end node
def reconstructPath(cameFrom, current, draw):
    while current in cameFrom:
        current = cameFrom[current]
        current.makePath()
        draw()


def algorithm(draw, grid, start, end):
    count = 0
#priotyQueue uses an effecient algorithm(maybe heap sort) to get the smallest value everytime
    openSet = PriorityQueue()
#put start node into openset
    openSet.put((0, count, start)) 
#keeps track of where we came from, what nodes came from what
    cameFrom = {} 
#keeps track of current shortest distance
    gScore = {square: float("inf") for row in grid for square in row}
    gScore[start] = 0
#keeps track of predicted distance
    fScore = {square: float("inf") for row in grid for square in row}
#the hierstic is the guess
    fScore[start] = h(start.getPos(), end.getPos())

#help to see if something is in the openSet
    openSetHash = {start}

    while not openSet.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

#get, which kind of removes the node of the current smallest node/ fscore from the open set
#then remove it from the hash to match the openset
            current = openSet.get()[2] 
            openSetHash.remove(current)

#if you curruent == end then youre at the end, else consider more nodes
            if current == end:
                reconstructPath(cameFrom, end, draw)
                end.makeIsEnd()
                return True

            for neighbor in current.neigbors:
#calc Gscore and compare if it's the smallest value and replace gscore and fscore with the info of smallest gscore
                tempGScore = gScore[current] + 1
            
                if tempGScore < gScore[neighbor]:
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tempGScore
                    fScore[neighbor] = tempGScore + h(neighbor.getPos(), end.getPos())
#then add it to the open set and the has set
                    if neighbor not in openSetHash:
                        count += 1
                        openSet.put((fScore[neighbor], count, neighbor))
                        openSetHash.add(neighbor)
                        neighbor.makeIsNextToSearch()
                    
            draw()
            if current != start:
                current.makeIsLookedAt()
    return False

def makeGrid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            square = Square(i, j, gap, rows)
            grid[i].append(square)

    return grid

def drawGrid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, PAYNESGREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, PAYNESGREY, (i * gap, 0), (i * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for square in row:
            square.draw(win)

    drawGrid(win, rows, width)
    pygame.display.update()

def getClickedPos(pos, rows, width):
    gap = width // rows
    y,x = pos
    row = y // gap
    col = x // gap
    
    return row, col

def main(win, width):
    ROWS = 50
    grid = makeGrid(ROWS, width)
    
    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = getClickedPos(pos, ROWS, width)
                square = grid[row][col]

                if not start and square != end:
                    start = square
                    start.makeIsStart()

                elif not end and square != start:
                    end = square
                    square.makeIsEnd()

                elif square != end and square != start:
                    square.makeIsBarrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = getClickedPos(pos, ROWS, width)
                square = grid[row][col]
                square.reset()
                if square == start:
                    start = None
                elif square == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for square in row:
                            square.updateNeigbors(grid)
                    
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

    pygame.quit()

main(WIN, WIDTH)