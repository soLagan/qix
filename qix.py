from pygame.constants import K_x, VIDEOEXPOSE, VIDEORESIZE
import pygame.display;
import time;
import pygame.color;
from pygame.locals import *
import pygame.event;
import sys

from board import Board
from boardObjects import Marker, Qix, Sparx

pygame.display.init()
fps = 30
fpsclock=pygame.time.Clock()

# Surface drawn on is 160 by 100 pixels, scaled to 1280 by 800 pixels
mysurface = pygame.display.set_mode((1280, 800), pygame.RESIZABLE)
resized = pygame.transform.scale(mysurface, (160, 100))

pygame.display.update()

# level = int(input("Enter the you the Level you wish to play [1-3]: "))
# print("Entering Level {}...".format(level))

print("Creating Board...")

board = Board()
board.gameStart()
board.createEntities(1)

print("Start!")

player = pygame.Rect(80,94,1,1)

running = True
while running:

    fpsclock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        if event == VIDEORESIZE:
            mysurface = pygame.display.set_mode((event.w,event.h), pygame.RESIZABLE)


    keys = pygame.key.get_pressed()
    moveVector = (player.x + (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]), player.y + (keys[pygame.K_DOWN] - keys[pygame.K_UP]))
    
    # Check if it can move on a valid edge
    if moveVector in board.playableEdge:
        player.x = moveVector[0]
        player.y = moveVector[1]

        board.getMarker().updateState(False)
    
    # Add all pixels that appear in that buffer and add it to captured space
    if not board.getMarker().getState() and board.edgesBuffer:
        board.updateEdges()     # Calls the fillCapture() method
        board.updatePlayable()
        board.printPercentage()
        

    # Press Spacebar in order start an incursion
    if moveVector in board.uncaptured and (keys[K_SPACE] or board.getMarker().getState()):
        player.x = moveVector[0]
        player.y = moveVector[1]

        board.edgesBuffer.append((player.x,player.y))
        board.uncaptured.remove((player.x,player.y))

        board.getMarker().updateState(True)

    board.getMarker().updateLocation(player.x, player.y)

    # Fill the background with black
    resized.fill(0)

    for coor in board.edges:
        pygame.draw.rect(resized, pygame.Color(255,255,255),pygame.Rect(coor[0],coor[1],1,1))
    for coor in board.playableEdge: # Omit drawing playable edges in later iterations
        pygame.draw.rect(resized, pygame.Color(255,0,255),pygame.Rect(coor[0],coor[1],1,1))
    for coor in board.uncaptured:
        pygame.draw.rect(resized, pygame.Color(23,0,0),pygame.Rect(coor[0],coor[1],1,1))
    for coor in board.edgesBuffer:
        pygame.draw.rect(resized, pygame.Color(255,0,0),pygame.Rect(coor[0],coor[1],1,1))
    for coor in board.captured:
        pygame.draw.rect(resized, pygame.Color(210,105,30),pygame.Rect(coor[0],coor[1],1,1))
    
    # print("I AM HERE")
    pygame.draw.rect(resized, pygame.Color(0,255,0) , player)
    mysurface.blit(pygame.transform.scale(resized, mysurface.get_rect().size), (0,0))   # Scale 160 by 100 board to 1280 by 800
    pygame.display.flip()
