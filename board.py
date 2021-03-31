from boardObjects import marker, qix, sparx

class board():
    def __init__(self, mainBoard, captured, uncaptured, edges, entities):
        self.mainBoard = []
        self.captured = []
        self.uncaptured = []
        self.edges = []
        self.entities = []

    def createEntities(self, level): # level determines number of enemy entities
        return

    def validateMove(self, keyPress, incr):
        return

    def updateLocations(self):
        return