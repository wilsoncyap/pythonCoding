import pygame, sys
from pygame.locals import *
import random
from cloud import Cloud

BLACK = (0,0,0)
BROWN = (153,76,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)

numcloud = 20
fpsClock = pygame.time.Clock()

DIRT = 0
GRASS = 1
WATER = 2
COAL = 3
CLOUD = 4
WOOD = 5
FIRE = 6
SAND = 7
GLASS = 8
ROCK = 9
STONE = 10
BRICK = 11
DIAMOND = 12
resources = [DIRT, GRASS, WATER, COAL, WOOD, FIRE, SAND, GLASS, ROCK, STONE, BRICK, DIAMOND]

textures = {
    DIRT : pygame.image.load('dirt.png'),
    GRASS : pygame.image.load('grass.png'),
    WATER : pygame.image.load('water.png'),
    COAL : pygame.image.load('coal.png'),
    CLOUD : pygame.image.load('cloud.png'),
    WOOD : pygame.image.load('wood.png'),
    FIRE : pygame.image.load('fire.png'),
    SAND : pygame.image.load('sand.png'),
    GLASS : pygame.image.load('glass.png'),
    ROCK : pygame.image.load('rock.png'),
    STONE : pygame.image.load('stone.png'),
    BRICK : pygame.image.load('brick.png'),
    DIAMOND : pygame.image.load('diamond.png')
    }

inventory = {
    DIRT : 0,
    GRASS : 0,
    WATER : 0,
    COAL : 0,
    WOOD : 0,
    FIRE : 0,
    SAND : 0,
    GLASS : 0,
    ROCK : 0,
    STONE : 0,
    BRICK : 0,
    DIAMOND : 0
}

controls = {
    DIRT : 49, #event 49 is the '1' key
    GRASS : 50, #event 50 is the '2' key, etc.
    WATER : 51, #3 key
    COAL : 52, #4 key
    WOOD : 53, #5 key
    FIRE : 54, #6 key
    SAND : 55, #7 key
    GLASS : 56, #8 key
    ROCK : 57, #9 key
    STONE: 48, #0 key
    BRICK: 45, #- key
    DIAMOND : 61 #= key
}

craft = {
    FIRE : {WOOD : 2, ROCK : 2},
    STONE : {ROCK : 2},
    GLASS : {FIRE : 1, SAND : 2},
    DIAMOND : {WOOD : 2, COAL : 3},
    BRICK : {ROCK : 2, FIRE : 1},
    SAND : {ROCK : 2}
}

PLAYER = pygame.image.load('player.png')
playerPos = [0,0]

TILESIZE = 20
MAPWIDTH = 50
MAPHEIGHT = 30

tilemap = [[DIRT for w in range(MAPWIDTH)] for h in range(MAPHEIGHT)]
clouds = []
for i in range(numcloud):
    clouds.append(Cloud(random.randint(-200, -50), random.randint(0, MAPHEIGHT*TILESIZE), random.randint(1, 3)))

print(tilemap)

pygame.init()
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE,MAPHEIGHT*TILESIZE + 50))

INVFONT = pygame.font.Font('FreeSansBold.ttf', 18)

for rw in range(MAPHEIGHT):
    for cl in range(MAPWIDTH):
        randomNumber = random.randint(0,100)
        if randomNumber == 0:
            tile = DIAMOND
        elif randomNumber >= 1 and randomNumber <= 5:
            tile = ROCK
        elif randomNumber >= 6 and randomNumber <= 15:
            tile = COAL
        elif randomNumber >= 16 and randomNumber <= 25:
            tile = SAND
        elif randomNumber >= 26 and randomNumber <= 40:
            tile = WOOD
        elif randomNumber >= 41 and randomNumber <= 55:
            tile = WATER
        elif randomNumber >= 56 and randomNumber <= 80:
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

            for key in controls:
                if event.key == controls[key]:
                    if pygame.mouse.get_pressed()[0]:
                        if key in craft:
                            canBeMade = True
                            for i in craft[key]:
                                if craft[key][i] > inventory[i]:
                                    canBeMade = False
                                    break
                            if canBeMade == True:
                                for i in craft[key]:
                                    inventory[i] -= craft[key][i]
                                    inventory[key] += 1
                    else:
                        currentTile = tilemap[playerPos[1]][playerPos[0]]
                        if inventory[key] > 0:
                            inventory[key] -= 1
                            inventory[currentTile] += 1
                            tilemap[playerPos[1]][playerPos[0]] = key

    for row in range(MAPHEIGHT):
        for column in range(MAPWIDTH):
            DISPLAYSURF.blit(textures[tilemap[row][column]], (column*TILESIZE,row*TILESIZE))
    DISPLAYSURF.blit(PLAYER,(playerPos[0]*TILESIZE,playerPos[1]*TILESIZE))

    for c in range(numcloud):
        DISPLAYSURF.blit(textures[CLOUD].convert_alpha(), (clouds[c].cloudx,clouds[c].cloudy))
        clouds[c].cloudx += clouds[c].cloudspd
        if clouds[c].cloudx > MAPWIDTH*TILESIZE:
            clouds[c].cloudy = random.randint(0,MAPHEIGHT*TILESIZE)
            clouds[c].cloudx = -200

    placePosition = 10
    for item in resources:
        DISPLAYSURF.blit(textures[item],(placePosition, MAPHEIGHT*TILESIZE+20))
        placePosition += 30
        textObj = INVFONT.render(str(inventory[item]), True, WHITE, BLACK)
        DISPLAYSURF.blit(textObj,(placePosition,MAPHEIGHT*TILESIZE+20))
        placePosition += 50
    pygame.display.update()
    fpsClock.tick(24)