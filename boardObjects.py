import pygame

class Object():
    def __init__(self, xPos, yPos, speed):
        self.x = xPos
        self.y = yPos
        self.speed = speed
        self.theRect = pygame.Rect(self.x, self.y, 1, 1)
        self.colour = None
        self.possibleMoves = []

    def updateLocation(self, x, y):
        self.x = x
        self.y = y
        self.theRect.update(self.x, self.y, 1, 1)
        return
    
    def getLocation(self):
        return (self.x, self.y)

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour , self.theRect)
        return

    def generateMoveVectors(self):
        self.possibleMoves.append((self.x+1, self.y))
        self.possibleMoves.append((self.x, self.y+1))
        self.possibleMoves.append((self.x-1, self.y))
        self.possibleMoves.append((self.x, self.y-1))
        return

    def resetMoveVectors(self):
        self.possibleMoves = []

    # def move(self, board, keyPress, incr):
    #     return

    # def collide(self): # if collision happens?
    #     return


class Marker(Object):
    def __init__(self, xPos, yPos, speed, health, pushState):
        super().__init__(xPos, yPos, speed)
        self.health = health
        self.pushState = pushState
        self.theRect = pygame.Rect(self.x, self.y, 1, 1)
        self.colour = pygame.Color(0,204,0) # Green

    def isPushing(self):
        return self.pushState

    def setIsPushing(self, state):
        self.pushState = state
        return

    def getHealth(self):
        return self.health

    def updateHealth(self):
        self.health -= 1
        return


class Sparx(Object):
    def __init__(self, xPos, yPos, speed, tail1, tail2):
        super().__init__(xPos, yPos, speed)
        self.theRect = pygame.Rect(self.x, self.y, 1, 1)
        self.colour = pygame.Color(51,51,255) # Blue
        self.tail = []  # For movement
        self.tail.append((xPos,yPos))
        self.tail.append(tail1)
        self.possibleMoves = []

    def updateTail(self, moveVector):
        self.tail.insert(0, moveVector)
        self.tail.pop()


class Qix(Object):
    def __init__(self, xPos, yPos, speed, orientation, directionOfTravel):
        super().__init__(xPos, yPos, speed)
        self.orientation = orientation
        self.directionOfTravel = directionOfTravel
        self.theRect = pygame.Rect(self.x, self.y, 1, 1)
        self.colour = pygame.Color(204,204,255) # Black

    