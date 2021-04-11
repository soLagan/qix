import pygame

class Object():
    def __init__(self, xPos, yPos, speed):
        self.x = xPos
        self.y = yPos
        self.speed = speed
        self.theRect = pygame.Rect(self.x, self.y, 1, 1)
        self.colour = None

    def updateLocation(self, x, y):
        self.x = x
        self.y = y
        self.theRect.update(self.x, self.y, 1, 1)
    
    def getLocation(self):
        return (self.x, self.y)

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour , self.theRect)
        return

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

    def updateLocation(self, x, y):
        super().updateLocation(x, y)

        # Update the position of the rect
        self.theRect.x = x
        self.theRect.y = y

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
    def __init__(self, xPos, yPos, speed):
        super().__init__(xPos, yPos, speed)
        self.theRect = pygame.Rect(self.x, self.y, 1, 1)
        self.colour = pygame.Color(51,51,255) # Blue
        self.tail = []  # For movement

class Qix(Object):
    def __init__(self, xPos, yPos, speed, orientation, directionOfTravel):
        super().__init__(xPos, yPos, speed)
        self.orientation = orientation
        self.directionOfTravel = directionOfTravel
        self.theRect = pygame.Rect(self.x, self.y, 1, 1)
        self.colour = pygame.Color(204,204,255) # Black

    