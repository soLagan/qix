from pygame.constants import K_x, VIDEOEXPOSE, VIDEORESIZE
import pygame.display;
import time;
import pygame.color;
from pygame.locals import *
import pygame.event;
import sys
import math

from board import Board, Edge, Vertex
from boardObjects import Marker, Qix, Sparx

pygame.display.init()
fps = 30
fpsclock=pygame.time.Clock()

# Surface drawn on is 160 by 100 pixels, scaled to 1280 by 800 pixels
mysurface = pygame.display.set_mode((1280, 800), pygame.RESIZABLE)
resized = pygame.transform.scale(mysurface, (160, 100))

def main():
    pygame.display.update()

    # level = int(input("Enter the you the Level you wish to play [1-3]: "))
    # print("Entering Level {}...".format(level))

    print("Creating Board...")

    board = Board(80,94,1,1,False)
    board.gameStart()
    board.createEntities(1)

    print("Start!")

    # player = pygame.Rect(320,439,25,25)
    player = board.getMarker()
    playerRect = player.theRect
    player.updateLocation(playerRect.x, playerRect.y)

    running = True

    previousMoveVector = None
    startingIncurringEdge = None

    while running:

        fpsclock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            if event == VIDEORESIZE:
                mysurface = pygame.display.set_mode((event.w,event.h), pygame.RESIZABLE)


        keys = pygame.key.get_pressed()

        # TODO: This vector should be either: (1,0), (0,1), or (0,0)
        moveVector = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT], keys[pygame.K_DOWN] - keys[pygame.K_UP])
        
        touchingEdge = None # Start from no touchingEdge
        # If nothing is being pressed, ignore the code
        if not moveVector == (0,0):
            touchingEdge = currentEdge(player, board)
            
            if touchingEdge:
                # The player is touching an edge
                pass
            
            # Try moving in a direction
            player.updateLocation(player.x + moveVector[0], player.y + moveVector[1])

            touchingEdge = currentEdge(board.getMarker(), board)

            # If an edge was not found, revert the movement
            if not touchingEdge:
                player.updateLocation(player.x - moveVector[0], player.y - moveVector[1])
                # TODO: Consider error handling here; The player should always be on an edge

        if touchingEdge and not keys[pygame.K_SPACE]:
            board.getMarker().setIsPushing(False)

        # SPACE is pressed
        if keys[pygame.K_SPACE]:
            moveVector = limitVectorDirection(moveVector)
            # TODO: If this runs it skips the draw process after this if statement
            if moveVector == (0,0): continue
            
            # If the player is not currently incurring, initialise the environment
            if not board.getMarker().isPushing():
                board.getMarker().setIsPushing(True)

                playerPos = (player.x, player.y)
                board.edgesBuffer = Edge(playerPos, None)

                board.firstEdgeBuffer = board.edgesBuffer
                previousMoveVector = moveVector
                startingIncurringEdge = touchingEdge

            # Try moving
            # The player can move anywhere, BUT:
            #   - they cannot travel backwards along their path, AND
            #   - when they change vector direction they close one edge and start a new one
            edge = board.edgesBuffer

            # The direction changed
            if previousMoveVector != moveVector:
                # Finish this edge and start a new one
                playerPos = (player.x, player.y)
                edge.end = playerPos

                edge.next = Edge(edge.end, None)
                edge.next.previous = edge

                board.edgesBuffer = edge.next
                previousMoveVector = moveVector
            else:
                player.updateLocation(player.x + moveVector[0], player.y + moveVector[1])
                touchingEdge = currentEdge(player, board)
            
                # If an edge is being touched after the movement, the incursion is finished
                if touchingEdge:
                    # Now we need to decide: Insert into the touching edge or the edge from which it started?
                    # If same edge, figure out which one is first by comparing the 
                    if touchingEdge == startingIncurringEdge:
                        
                        if touchingEdge.start[1] > edge.start[1]:
                            # Change in upward direction
                            touchingEdge.addAfter(board.firstEdgeBuffer, True)
                        elif touchingEdge.start[1] < edge.start[1]:
                            # Change in downward direction
                            touchingEdge.addAfter(board.firstEdgeBuffer, False)
                            pass
                        pass
                    else:
                        # Otherwise it is an incursion to a different edge
                        pass

                    # Insert the buffer into the edge
                    board.getMarker().setIsPushing(False)

        board.getMarker().updateLocation(playerRect.x, playerRect.y)
        board.draw()

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

def currentEdge(player:Marker, board:Board):
    """
    Finds an edge that corresponds to the players current position.
        Returns: Edge if an edge was found. Otherwise: None
    """

    edge = board.firstEdge
    if posInRange(edge.start, edge.end, (player.x, player.y)):
        return edge
    
    # Move to the next element    
    edge = edge.next
    while edge != board.firstEdge:
        if posInRange(edge.start, edge.end, (player.x, player.y)):
            return edge
        edge = edge.next
    
    return None
        
def posInRange(start, end, position):
    
    return inRange(start[0], end[0], position[0]) and inRange(start[1], end[1], position[1])

def inRange(minVal, maxVal, target):
    return min(minVal, maxVal) <= target and target <= max(minVal, maxVal)

main()