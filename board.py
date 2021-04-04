from boardObjects import Marker, Qix, Sparx
import random # for createEntities, assign enemies random but valid starting coordinates
import copy

class Vertex():
    def __init__(self):
        self.x = 0
        self.y = 0

class Edge():
    def __init__(self):
        self.start = None
        self.end = None
        self.next = None
        self.previous = None

    def addAfter(self, new):
        pass
        # Turn an incursion into a polygon and use it to take out points from uncaptured space

class Board():
    def __init__(self):
        self.mainBoard = []     # Contains all possible coordinates entites can exist on
        self.captured = []      # Contains coordinates of 'captured' space
        self.uncaptured = []    # Contains coordinates of 'uncaptured' space
        self.edges = []         # Contains coordinates of all traversal space
        self.edgesBuffer = []   # Contains edges on Current push
        self.entities = []      # Contains all boardObjects in play
        self.capturedBuffer = []

    def gameStart(self):
        
        # Construct mainBoard & starting edges of traversal
        self.mainBoard = [ (x,y) for x in range(160) for y in range(100) if 40 < x < 120 and 10 < y < 90 ]
        self.edges = [ (lmao) for lmao in self.mainBoard if (lmao[0] == 41 or lmao[0] == 119) or lmao[1] == 11 or lmao[1] == 89 ]

        self.uncaptured = [losing for losing in self.mainBoard if losing not in self.edges] # This process takes a while

        return

    def updateEdges(self):
        avgX = 0
        avgY = 0
        for i in self.edgesBuffer:
            self.edges.append(i)
            avgX+= i[0]
            avgY+= i[1]
        avgX /= len(self.edgesBuffer)
        avgY /= len(self.edgesBuffer)

        self.fillCapture(int(avgX), int(avgY))

        for i in self.capturedBuffer:
            self.captured.append(i)
        self.capturedBuffer = []
        self.edgesBuffer = []
        percentage = ((len(self.captured) + len(self.edges)) / len(self.mainBoard))*100
        print("{:.2f}% of board captured.".format(percentage))
        return

    def fillCapture(self, x,y):
        self.capturedBuffer.append((x,y))

        # This takes forever, so I changed the dimensions of the board to 40 by 40 and just scaled it up
        for coor in self.capturedBuffer:
            if (coor[0]+1,coor[1])  in self.uncaptured and (coor[0]+1,coor[1]) not in self.capturedBuffer:
                self.capturedBuffer.append((coor[0]+1,coor[1]))
                self.uncaptured.remove((coor[0]+1,coor[1]))
            if (coor[0]-1,coor[1])  in self.uncaptured and (coor[0]-1,coor[1]) not in self.capturedBuffer:
                self.capturedBuffer.append((coor[0]-1,coor[1]))
                self.uncaptured.remove((coor[0]-1,coor[1]))
            if (coor[0],coor[1]+1)  in self.uncaptured and (coor[0],coor[1]+1) not in self.capturedBuffer:
                self.capturedBuffer.append((coor[0],coor[1]+1))
                self.uncaptured.remove((coor[0],coor[1]+1))
            if (coor[0],coor[1]-1)  in self.uncaptured and (coor[0],coor[1]-1) not in self.capturedBuffer:
                self.capturedBuffer.append((coor[0],coor[1]-1))
                self.uncaptured.remove((coor[0],coor[1]-1))
        return

    def validateMove(self):
        return

    def getMarker(self):
        return self.entities[0]

    def createEntities(self, level): # level determines number of enemy entities

        # Player wants to start at the middle bottom edge
        player = Marker(320, 439, 1, 5, False)  
        self.entities.append(player)

        return

    def validateMove(self, keyPress, incr):
        return

    def updateLocations(self):
        return