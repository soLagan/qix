from pygame.constants import K_x, VIDEOEXPOSE, VIDEORESIZE
import pygame.display;
import time;
import pygame.color;
from pygame.locals import *
import pygame.event;
import sys

from board import Board

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

print("Creating Board...")

board = Board()
board.gameStart(level)  # Calls createEntities

print("Start!")

player = board.getMarker()  # BoardObjects can only be accessed through the board

running = True
while running:

    fpsclock.tick(60)

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

    board.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event == VIDEORESIZE:
            mysurface = pygame.display.set_mode((event.w,event.h), pygame.RESIZABLE)

