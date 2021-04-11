from pygame.constants import K_x, VIDEOEXPOSE, VIDEORESIZE
import pygame.display;
import time;
import pygame.color;
from pygame.locals import *
import pygame.event;
import sys
import math

from board import Board, Edge
from boardObjects import Marker

fps = 30
fpsclock=pygame.time.Clock()

# To be removed, waiting on UI elements to be implemented first
# pygame.display.init()
# mysurface = pygame.display.set_mode((1280, 800), pygame.RESIZABLE)
# resized = pygame.transform.scale(mysurface, (160, 100))
# pygame.display.update()

level = 4
# level = int(input("Enter the you the Level you wish to play [1-4]: "))
# print("Entering Level {}...".format(level))

def main():
    print("Creating Board...")

    board = Board()
    board.gameStart(level)  # Calls createEntities

    print("Start!")

    player = board.getMarker()  # BoardObjects can only be accessed through the board

    running = True
    while running:

        fpsclock.tick(30)

        keys = pygame.key.get_pressed()
        moveVector = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT], keys[pygame.K_DOWN] - keys[pygame.K_UP])
        moveVector = limitVectorDirection(moveVector)
        touchingEdge = None # Start from no touchingEdge
        
        # If nothing is being pressed, ignore the code
        if not moveVector == (0,0) and not keys[pygame.K_SPACE]:
            
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

        if keys[pygame.K_SPACE]:
            # If the player is not currently incurring, initialise the environment
            if not board.getMarker().isPushing():
                board.getMarker().setIsPushing(True)

                playerPos = (player.x, player.y)
                board.edgesBuffer = Edge(playerPos, None)

                board.firstEdgeBuffer = board.edgesBuffer
                previousMoveVector = moveVector
                startingIncurringEdge = currentEdge(player, board)

            # Try moving
            # The player can move anywhere, BUT:
            #   - they cannot travel backwards along their path, AND
            #   - when they change vector direction they close one edge and start a new one
            edge = board.edgesBuffer

            # The direction changed
            if not currentEdge(player, board) and moveVector != (0,0) and previousMoveVector != moveVector:
                # Finish this edge and start a new one
                playerPos = (player.x, player.y)

                if playerPos != edge.start: 
                    edge.end = playerPos

                    edge.next = Edge(edge.end, None)
                    edge.next.previous = edge

                    board.edgesBuffer = edge.next
                    previousMoveVector = moveVector

            elif moveVector != (0,0):
                player.updateLocation(player.x + moveVector[0], player.y + moveVector[1])
                touchingEdge = currentEdge(player, board)
                
                # If an edge is being touched after the movement, the incursion is finished
                if touchingEdge and board.firstEdgeBuffer != board.edgesBuffer:
                    # Close the current edge
                    playerPos = (player.x, player.y)
                    edge.end = playerPos
                    
                    # If same edge, figure out which one is first by comparing the 
                    if touchingEdge == startingIncurringEdge:
                        

                        downwardEdge = touchingEdge.start[1] < touchingEdge.end[1]
                        upwardEdge = touchingEdge.start[1] > touchingEdge.end[1]
                        rightwardEdge = touchingEdge.start[0] < touchingEdge.end[0]
                        leftwardEdge = touchingEdge.start[0] > touchingEdge.end[0]

                        if downwardEdge and board.firstEdgeBuffer.start[1] < edge.start[1] \
                            or upwardEdge and board.firstEdgeBuffer.start[1] > edge.start[1] \
                            or rightwardEdge and board.firstEdgeBuffer.start[0] < edge.start[0]\
                            or leftwardEdge and board.firstEdgeBuffer.start[0] > edge.start[0]:
                            
                            touchingEdge.addAfter(board.firstEdgeBuffer)
                        else:
                            # If the direction of the incursion was made in opposite of the direction of the edge
                            # Reverse the list and insert it
                            printList(board.firstEdgeBuffer)
                            board.firstEdgeBuffer = reverseLinkedList(board.firstEdgeBuffer)
                            printList(board.firstEdgeBuffer)
                            touchingEdge.addAfter(board.firstEdgeBuffer)
                        
                    else:
                        # BUG 1: Fails when only one edge exists in the incursion.
                        #   Replicate by: Moving upwards from starting position.
                        # BUG 2: Incursion from right edge to top edge fails.

                        # Otherwise it is an incursion to a different edge
                        rightwards = board.firstEdgeBuffer.start[0] < edge.end[0]
                        leftwards = not rightwards # If not traveling right, the action must be going left

                        if rightwards:
                            startingIncurringEdge.end = board.firstEdgeBuffer.start
                            startingIncurringEdge.next = board.firstEdgeBuffer
                            touchingEdge.start = edge.end
                            edge.next = touchingEdge
                        else:
                            oldFirstEdge = board.firstEdgeBuffer
                            board.firstEdgeBuffer = reverseLinkedList(board.firstEdgeBuffer)

                            startingIncurringEdge.start = oldFirstEdge.end
                            touchingEdge.end = board.firstEdgeBuffer.start
                            touchingEdge.next = board.firstEdgeBuffer
                            oldFirstEdge.next = startingIncurringEdge

                    # Insert the buffer into the edge
                    board.getMarker().setIsPushing(False)
                    board.firstEdgeBuffer = None
                    board.edgesBuffer = None

        board.draw() # draw all objects

        for event in pygame.event.get(): # Check for quit event (closing window)
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event == VIDEORESIZE: # Check for resize
                mysurface = pygame.display.set_mode((event.w,event.h), pygame.RESIZABLE)

def reverseLinkedList(inputList):
    prev = None
    curr = inputList
    nextRef = None

    while curr != None:
      nextRef = curr.next
      curr.next = prev
      oldEnd = curr.end
      curr.end = curr.start
      curr.start = oldEnd
      prev = curr
      curr = nextRef
    
    return prev

def printList(inputList):
    edge = inputList
    print(edge)
    edge = edge.next
    while edge != None and edge != inputList:
        print(edge)
        edge = edge.next


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