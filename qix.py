from pygame.constants import K_x
import pygame.display;
import time;
import pygame.color;
import pygame.locals;
import pygame.event;
import sys
from board import board
from boardObjects import marker, qix, sparx

pygame.display.init()
fps = 30
fpsclock=pygame.time.Clock()
mysurface = pygame.display.set_mode(size=(640, 480), flags=0, depth=0, display=0, vsync=0)
pygame.display.update()

incr = 1

print("Creating Board")

fuckingBoard = board()
fuckingBoard.gameStart()
fuckingBoard.createEntities(1)

print("Start!")

player = pygame.Rect(320,439,8,8)

running = True
while running:
    fpsclock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

    keys = pygame.key.get_pressed()

    if (player.x + (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]), player.y + (keys[pygame.K_DOWN] - keys[pygame.K_UP])) in fuckingBoard.getEdges():

        player.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
        player.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) 
        fuckingBoard.getMarker().updateState(False)
    if (player.x + (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]), player.y + (keys[pygame.K_DOWN] - keys[pygame.K_UP])) in fuckingBoard.getUncaptured():

        player.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
        player.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP])
        fuckingBoard.updateEdge((player.x,player.y))
        fuckingBoard.getMarker().updateState(True)

    fuckingBoard.getMarker().updateLocation(player.x, player.y)
    #print(fuckingBoard.getMarker().getLocation(), fuckingBoard.getMarker().getState())

    mysurface.fill(0)
    for coor in fuckingBoard.getEdges():
        pygame.draw.rect(mysurface, pygame.Color(255,255,255),pygame.Rect(coor[0],coor[1],1,1))
    pygame.draw.rect(mysurface, pygame.Color(0,255,255),player)
    pygame.display.flip()
