from boardObjects import marker, qix, sparx
import random # for createEntities, assign enemies random but valid starting coordinates

class board():
    def __init__(self):
        self.mainBoard = []     # Contains all possible coordinates entites can exist on
        self.captured = []      # Contains coordinates of 'captured' space
        self.uncaptured = []    # Contains coordinates of 'uncaptured' space
        self.edges = []         # Contains coordinates of all traversal space
        self.edgesBuffer = []   # Contains edges on Current push
        self.entities = []      # Contains all boardObjects in play


    def gameStart(self):
        
        # Construct mainBoard & starting edges of traversal
        self.mainBoard = [ (x,y) for x in range(640) for y in range(480) if 120 < x < 520 and 40 < y < 440 ]
        self.edges = [ (lmao) for lmao in self.mainBoard if (lmao[0] == 121 or lmao[0] == 519) or lmao[1] == 41 or lmao[1] == 439 ]

        self.captured = self.edges
        self.uncaptured = [losing for losing in self.mainBoard if losing not in self.edges] # This process takes a while

        return

    def getEdges(self):
        return self.edges

    def getUncaptured(self):
        return self.uncaptured


    def updateEdges(self):
        for i in self.edgesBuffer:
            self.edges.append(i)
        self.edgesBuffer = []
        return

    def updateBuffer(self, coor):
        self.edgesBuffer.append(coor)
        return

    def validateMove(self):
        return

    def getMarker(self):
        return self.entities[0]

    def createEntities(self, level): # level determines number of enemy entities

        # Player wants to start at the middle bottom edge
        player = marker(320, 439, 1, 5, False)  
        self.entities.append(player)

        return

    def validateMove(self, keyPress, incr):
        return

    def updateLocations(self):
        return