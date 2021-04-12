from pygame.constants import K_x, VIDEOEXPOSE, VIDEORESIZE
import pygame.display;
import time;
import pygame.color;
from pygame.locals import *
import pygame.event;
import sys
import math
import copy
import random

from board import Board

fps = 30
fpsclock=pygame.time.Clock()

# To be removed, waiting on UI elements to be implemented first

# pygame.display.update()

def main():
    pygame.display.init()
    mysurface = pygame.display.set_mode((1280, 800), pygame.RESIZABLE)
    resized = pygame.transform.scale(mysurface, (160, 100))
    pygame.display.update()
    level = 4

    # level = int(input("Enter the you the Level you wish to play [1-4]: "))
    # print("Entering Level {}...".format(level))

    print("Creating Board...")

    board = Board()
    board.gameStart(level)  # Calls createEntities

    print("Start!")

    player = board.getMarker()  # BoardObjects can only be accessed through the board

    running = True
    while running:

        fpsclock.tick(30)

        keys = pygame.key.get_pressed()
        moveVector = (player.x + (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]), player.y + (keys[pygame.K_DOWN] - keys[pygame.K_UP]))
        
        # Check if it can move on a valid edge
        if moveVector in board.playableEdge:
            player.x = moveVector[0]
            player.y = moveVector[1]
            player.setIsPushing(False)
            # Add all pixels that appear in that buffer and add it to captured space

        if not board.getMarker().isPushing() and board.edgesBuffer:
            board.updateEdges()
            board.updatePlayable()

        # Press Spacebar in order start an incursion
        if moveVector in board.uncaptured and (keys[K_SPACE] or player.isPushing()):
            player.x = moveVector[0]
            player.y = moveVector[1]

            board.edgesBuffer.append((player.x,player.y))
            board.uncaptured.remove((player.x,player.y))

            player.setIsPushing(True)


        # Enemy Movement

        # Sparx 1
        if level >= 2:

            sparx = board.getSparx1()
            sparx.generateMoves()
            moveList = []

            for move in sparx.possibleMoves:

                if move in sparx.tail:
                    continue
                
                prevX = copy.deepcopy(sparx.x)
                prevY = copy.deepcopy(sparx.y)

                sparx.updateLocation(move[0], move[1])

                touchingEdge = currentEdge(sparx,board)

                if not touchingEdge:
                    sparx.updateLocation(prevX, prevY)
                else:
                    moveList.append(move)

            move = random.choice(moveList)  
            sparx.updateTail((move[0], move[1]))

            sparx.resetMoves()


        # Sparx 2
        if level >= 3:

            sparx = board.getSparx2()
            sparx.generateMoves()
            moveList = []

            for move in sparx.possibleMoves:

                if move in sparx.tail:
                    continue
                
                prevX = copy.deepcopy(sparx.x)
                prevY = copy.deepcopy(sparx.y)

                sparx.updateLocation(move[0], move[1])

                touchingEdge = currentEdge(sparx,board)

                if not touchingEdge:
                    sparx.updateLocation(prevX, prevY)
                else:
                    moveList.append(move)

            move = random.choice(moveList)  
            sparx.updateTail((move[0], move[1]))

            sparx.resetMoves()



        # Qix
        if level == 4:
            qix = board.getQix()
            qix.generateMoves()
            moveList = []

            for moveVector in qix.possibleMoves:
                prevX = copy.deepcopy(sparx.x)
                prevY = copy.deepcopy(sparx.y)

                qix.updateLocation(moveVector[0], moveVector[1])
                touchingEdge = currentEdge(qix, board)

                if touchingEdge:
                    qix.updateLocation(prevX, prevY)
                else:
                    moveList.append(moveVector)

            moveVector = random.choice(moveList)
            qix.updateLocation(moveVector[0]-3, moveVector[1]-3)

            qix.resetMoves()


        player.updateLocation(player.x, player.y)

        board.draw()
        board.collide()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event == VIDEORESIZE:
                mysurface = pygame.display.set_mode((event.w,event.h), pygame.RESIZABLE)


def limitVectorDirection(vector):
    """
    Converts a vector to (+-1,0), (0,+-1), or (0,0).
        Assumption: The input vector consists of two numerical elements.
        Returns: A tuple in the form: (val, val)
    """
    if abs(vector[0]) == 1:
        return (math.copysign(1, vector[0]), 0)
    elif abs(vector[1]) == 1:
        return (0, math.copysign(1, vector[1]))
    
    return (0,0)

def currentEdge(object, board:Board):
    """
    Finds an edge that corresponds to the players current position.
        Returns: Edge if an edge was found. Otherwise: None
    """

    edge = board.firstEdge
    if posInRange(edge.start, edge.end, (object.x, object.y)):
        return edge
    
    # Move to the next element    
    edge = edge.next
    while edge != board.firstEdge:
        if posInRange(edge.start, edge.end, (object.x, object.y)):
            return edge
        edge = edge.next
    
    return None
        
def posInRange(start, end, position):
    
    return inRange(start[0], end[0], position[0]) and inRange(start[1], end[1], position[1])

def inRange(minVal, maxVal, target):
    return min(minVal, maxVal) <= target and target <= max(minVal, maxVal)


main() 