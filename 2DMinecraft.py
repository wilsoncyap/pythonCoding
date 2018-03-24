import pygame, sys
from pygame.locals import *
import random

BLACK = (0,0,0)
BROWN = (153,76,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)

cloudx = -200
cloudy = 0

fpsClock = pygame.time.Clock()

DIRT = 0
GRASS = 1
WATER = 2
COAL = 3
CLOUD = 4
resources = [DIRT, GRASS, WATER, COAL]

textures = {
    DIRT : pygame.image.load('dirt.png'),
    GRASS : pygame.image.load('grass.png'),
    WATER : pygame.image.load('water.png'),
    COAL : pygame.image.load('coal.png'),
    CLOUD : pygame.image.load('cloud.png')
    }

inventory = {
    DIRT : 0,
    GRASS : 0,
    WATER : 0,
    COAL : 0
}

PLAYER = pygame.image.load('player.png')
playerPos = [0,0]

TILESIZE = 20
MAPWIDTH = 30
MAPHEIGHT = 20

tilemap = [[DIRT for w in range(MAPWIDTH)] for h in range(MAPHEIGHT)]
print(tilemap)

pygame.init()
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE,MAPHEIGHT*TILESIZE + 50))

INVFONT = pygame.font.Font('FreeSansBold.ttf', 18)

for rw in range(MAPHEIGHT):
    for cl in range(MAPWIDTH):
        randomNumber = random.randint(0,15)
        if randomNumber == 0:
            tile = COAL
        elif randomNumber == 1 or randomNumber == 2:
            tile = WATER
        elif randomNumber >= 3 and randomNumber <= 7:
            tile = GRASS
        else:
            tile = DIRT
        tilemap[rw][cl] = tile

while True:
    DISPLAYSURF.fill(BLACK)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT and playerPos[0] < MAPWIDTH:
                playerPos[0] += 1
            if event.key == K_LEFT and playerPos[0] > 0:
                playerPos[0] -= 1
            if event.key == K_DOWN and playerPos[1] < MAPHEIGHT:
                playerPos[1] += 1
            if event.key == K_UP and playerPos[1] > 0:
                playerPos[1] -= 1
            if event.key == K_SPACE:
                currentTile = tilemap[playerPos[1]][playerPos[0]]
                inventory[currentTile] += 1
                tilemap[playerPos[1]][playerPos[0]] = DIRT

            if event.key == K_1:
                currentTile = tilemap[playerPos[1]][playerPos[0]]
                if inventory[DIRT] > 0:
                    inventory[DIRT] -= 1
                    tilemap[playerPos[1]][playerPos[0]] = DIRT
                    inventory[currentTile] += 1
            if event.key == K_2:
                currentTile = tilemap[playerPos[1]][playerPos[0]]
                if inventory[GRASS] > 0:
                    inventory[GRASS] -= 1
                    tilemap[playerPos[1]][playerPos[0]] = GRASS
                    inventory[currentTile] += 1
            if event.key == K_3:
                currentTile = tilemap[playerPos[1]][playerPos[0]]
                if inventory[WATER] > 0:
                    inventory[WATER] -= 1
                    tilemap[playerPos[1]][playerPos[0]] = WATER
                    inventory[currentTile] += 1
            if event.key == K_4:
                currentTile = tilemap[playerPos[1]][playerPos[0]]
                if inventory[COAL] > 0:
                    inventory[COAL] -= 1
                    tilemap[playerPos[1]][playerPos[0]] = COAL
                    inventory[currentTile] += 1


    for row in range(MAPHEIGHT):
        for column in range(MAPWIDTH):
            DISPLAYSURF.blit(textures[tilemap[row][column]], (column*TILESIZE,row*TILESIZE))
    DISPLAYSURF.blit(PLAYER,(playerPos[0]*TILESIZE,playerPos[1]*TILESIZE))

    DISPLAYSURF.blit(textures[CLOUD].convert_alpha(), (cloudx,cloudy))
    cloudx+=1
    if cloudx > MAPWIDTH*TILESIZE:
        cloudy = random.randint(0,MAPHEIGHT*TILESIZE)
        cloudx = -200
    placePosition = 10
    for item in resources:
        DISPLAYSURF.blit(textures[item],(placePosition, MAPHEIGHT*TILESIZE+20))
        placePosition += 30
        textObj = INVFONT.render(str(inventory[item]), True, WHITE, BLACK)
        DISPLAYSURF.blit(textObj,(placePosition,MAPHEIGHT*TILESIZE+20))
        placePosition += 50
    pygame.display.update()
    fpsClock.tick(24)