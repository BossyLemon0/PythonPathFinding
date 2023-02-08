import pygame
import math

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


class Squares:
    def __init__(self, width, row, col, totalRows):
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
        return self.color == ULTRAVIOLET
    
    def isEnd(self):
        return self.color == DARKPURPLE
    
    def reset(self):
        return self.color == WHITE
    
    def makeIsLookedAt(self):
        self.color = ICEDBLUE
    
    def makeIsNextToSearch(self):
        self.color = LIGHTGREEN
        
    def makeIsBarrier(self):
        self.color = CAMBRIDGEBLUE
    
    def makeIsStart(self):
        self.color = ULTRAVIOLET
    
    def makeIsEnd(self):
        self.color = DARKPURPLE
    
    def makeReset(self):
        self.color = WHITE

    def makePath (self):
        self.olor = ORANGE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def updateNeigbors(self, grid):
        return False
    
    def __lt__(self, other):
        return False