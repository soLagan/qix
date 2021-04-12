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


# To be removed, waiting on UI elements to be implemented first

# pygame.display.update()

def main():

    fpsclock=pygame.time.Clock()

    level = 4

    # level = int(input("Enter the you the Level you wish to play [1-4]: "))
    # print("Entering Level {}...".format(level))

    print("Creating Board...")

    board = Board()
    board.gameStart(level)  # Calls createEntities

    print("Start!")

    # BoardObjects can only be accessed through the board
    player = board.getMarker()
    sparx1 = board.getSparx1()
    sparx2 = board.getSparx2()
    qix = board.getQix()

    sparxHolder = [sparx1,sparx2]

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

        player.updateLocation(player.x, player.y)


        # General Enemy Movement:
        # Qix and Sparx both use a random movement algorithm
        # 1. They will generate a movelist based on the adjacent points to their current position
        # 2. Filter through movelist checking if a move satisfies the specific criteria
        # 3. Choose a random move based on the moves that have been screened

        # For the Sparx's
        for sparx in sparxHolder:

            if sparx:
                sparx.generateMoves()
                moveList = []

                for move in sparx.possibleMoves:

                    if move in sparx.tail:  # Sparx tail to prevent backtracking
                        continue
                    
                    prevX = copy.deepcopy(sparx.x)
                    prevY = copy.deepcopy(sparx.y)

                    sparx.updateLocation(move[0], move[1])

                    touchingEdge = currentEdge(sparx,board)

                    if not touchingEdge:
                        sparx.updateLocation(prevX, prevY)
                    else:
                        moveList.append(move)

                if moveList:
                    move = random.choice(moveList)
                    sparx.updateTail((move[0], move[1]))
                    sparx.updateLocation(move[0], move[1]) 

                sparx.resetMoves()

        # Qix
        if qix:
            qix.generateMoves() # Generates moves based on the position of Rect.center
            moveList = []

            for move in qix.possibleMoves:
                prevX = copy.deepcopy(qix.x)
                prevY = copy.deepcopy(qix.y)

                qix.updateLocation(move[0], move[1])
                touchingEdge = currentEdge(qix, board)

                if touchingEdge:
                    qix.updateLocation(prevX, prevY)
                else:
                    moveList.append(move)

            if moveList:
                move = random.choice(moveList)
                # -1 to counteract the offset of using Rect.center for generating moves
                qix.updateLocation(move[0]-1, move[1]-1) 

            qix.resetMoves()

        board.draw()
        board.collide()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()


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