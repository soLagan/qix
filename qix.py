from pygame.constants import K_x
import pygame.display;
import time;
import pygame.color;
import pygame.locals;
import pygame.event;
import sys

from board import Board
from boardObjects import Marker, Qix, Sparx

pygame.display.init()
fps = 30
fpsclock=pygame.time.Clock()
mysurface = pygame.display.set_mode(size=(640, 480), flags=0, depth=0, display=0, vsync=0)
pygame.display.update()

print("Creating Board...")

board = Board(1,1,1,1,False)
board.gameStart()
board.createEntities(1)

print("Start!")

# player = pygame.Rect(320,439,25,25)
player = board.theMarker.theRect
board.getMarker().updateLocation(player.x, player.y)

running = True
while running:

    fpsclock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

    keys = pygame.key.get_pressed()
    moveVector = (player.x + (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]), player.y + (keys[pygame.K_DOWN] - keys[pygame.K_UP]))
    
    # Check if it can move on an edge
    if moveVector in board.edges:
        player.x = moveVector[0]
        player.y = moveVector[1]

        board.getMarker().setIsPushing(False)
        # Add all pixels that appear in that buffer and add it to captured space

    if not board.getMarker().isPushing() and board.edgesBuffer:
        board.updateEdges()

    if moveVector in board.uncaptured:
        player.x = moveVector[0]
        player.y = moveVector[1]

        board.edgesBuffer.append((player.x,player.y))
        board.uncaptured.remove((player.x,player.y))

        board.getMarker().setIsPushing(True)

    board.getMarker().updateLocation(player.x, player.y)

    # Fill the background with black
    mysurface.fill(0)
    
    for coor in board.edges:
        pygame.draw.rect(mysurface, pygame.Color(255,255,255),pygame.Rect(coor[0],coor[1],1,1))
    for coor in board.edgesBuffer:
        pygame.draw.rect(mysurface, pygame.Color(255,0,0),pygame.Rect(coor[0],coor[1],1,1))
    
    # print("I AM HERE")
    # pygame.draw.rect(mysurface, pygame.Color(0,255,255) , player)
    for entity in board.entities:
        # print(entity.theRect)
        pygame.draw.rect(mysurface, pygame.Color(0,255,255) , entity.theRect)
    pygame.display.flip()
