class Object():
    def __init__(self, xPos, yPos, speed):
        self.xPos = xPos
        self.yPos = yPos
        self.speed = speed

    def updateLocation(self, x, y):
        self.xPos = x
        self.yPos = y
        return
    
    def getLocation(self):
        return (self.xPos, self.yPos)

    def move(self, board, keyPress, incr):
        return

    def collide(self): # if collision happens?
        return

class Marker(Object):
    def __init__(self, xPos, yPos, speed, health, pushState):
        self.health = health
        self.pushState = pushState
        super().__init__(xPos, yPos, speed)

    def getState(self):
        return self.pushState

    def updateState(self, state):
        # Call `fillCapture`
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


class Qix(Object):
    def __init__(self, xPos, yPos, speed, orientation, directionOfTravel):
        self.orientation = orientation
        self.directionOfTravel = directionOfTravel
        super().__init__(xPos, yPos, speed)

    