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
mysurface = pygame.display.set_mode((1280, 800), pygame.RESIZABLE)
resized = pygame.transform.scale(mysurface, (320, 200))
pygame.display.update()

print("Creating Board...")

board = Board()
board.gameStart()
board.createEntities(1)

print("Start!")

player = pygame.Rect(160,149,3,3)

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
    
    # Check if it can move on an edge
    if moveVector in board.edges:
        player.x = moveVector[0]
        player.y = moveVector[1]

        board.getMarker().updateState(False)
        # Add all pixels that appear in that buffer and add it to captured space

    if not board.getMarker().getState() and board.edgesBuffer:
        board.updateEdges()

    if moveVector in board.uncaptured:
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
    for coor in board.edgesBuffer:
        pygame.draw.rect(resized, pygame.Color(255,0,0),pygame.Rect(coor[0],coor[1],1,1))
    for coor in board.captured:
        pygame.draw.rect(resized, pygame.Color(0,255,0),pygame.Rect(coor[0],coor[1],1,1))
    
    # print("I AM HERE")
    pygame.draw.rect(resized, pygame.Color(0,255,255) , player)
    mysurface.blit(pygame.transform.scale(resized, mysurface.get_rect().size), (0,0))
    pygame.display.flip()
