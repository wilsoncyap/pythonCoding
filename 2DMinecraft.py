import pygame, sys
from pygame.locals import *
import random
from cloud import Cloud

#constants representing colors
BLACK = (0,0,0)
BROWN = (153,76,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)

#number of clouds in the game
numcloud = 20
fpsClock = pygame.time.Clock()

#constants representing the different resources
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

#a list of resources
resources = [DIRT, GRASS, WATER, COAL, WOOD, FIRE, SAND, GLASS, ROCK, STONE, BRICK, DIAMOND]

#a dictionary linking resources to texture
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

#map each resource to the EVENT key used to place/craft it
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
#the player image
PLAYER = pygame.image.load('player.png')
#the position of the player [x,y]
playerPos = [0,0]

#game dimensions
TILESIZE = 20
MAPWIDTH = 50
MAPHEIGHT = 30

tilemap = [[DIRT for w in range(MAPWIDTH)] for h in range(MAPHEIGHT)]
clouds = []
for i in range(numcloud):
    clouds.append(Cloud(random.randint(-200, -50), random.randint(0, MAPHEIGHT*TILESIZE), random.randint(1, 3)))

#set up the display
pygame.init()
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE,MAPHEIGHT*TILESIZE + 50))

#add a font for our inventory
INVFONT = pygame.font.Font('FreeSansBold.ttf', 18)

#loop through each row
for rw in range(MAPHEIGHT):
    #loop through each column in that row
    for cl in range(MAPWIDTH):
        #pick a random number between 0 and 100
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
        #set the position in the tilemap to randonmly chosen tile
        tilemap[rw][cl] = tile

while True:
    DISPLAYSURF.fill(BLACK)
    #get all the user events
    for event in pygame.event.get():
        #if the user wants to quit
        if event.type == QUIT:
            #end the game and close the window
            pygame.quit()
            sys.exit()
        #if a key is pressed
        elif event.type == KEYDOWN:
            #if the right arrow is pressed
            if event.key == K_RIGHT and playerPos[0] < MAPWIDTH:
                #change the player's x position positive
                playerPos[0] += 1
            #if the left arrow key is pressed
            if event.key == K_LEFT and playerPos[0] > 0:
                #change the player's x position negative
                playerPos[0] -= 1
            #if the down key is pressed
            if event.key == K_DOWN and playerPos[1] < MAPHEIGHT:
                #change player's y position positive
                playerPos[1] += 1
            #if the up arrow is pressed
            if event.key == K_UP and playerPos[1] > 0:
                #change the player's y position negative
                playerPos[1] -= 1
            if event.key == K_SPACE:
                #what resource is the player standing on?
                currentTile = tilemap[playerPos[1]][playerPos[0]]
                #player now has 1 more of this resource
                inventory[currentTile] += 1
                #the player is now standing on dirt
                tilemap[playerPos[1]][playerPos[0]] = DIRT

            for key in controls:
                #if this key was pressed
                if event.key == controls[key]:
                    #CRAFT if the mouse is also pressed
                    if pygame.mouse.get_pressed()[0]:
                        #if the item can be crafted
                        if key in craft:
                            #keeps track of whether we have the resources
                            #to craft this item
                            canBeMade = True
                            #for each item needed to craft...
                            for i in craft[key]:
                                #... if we don't have enough...
                                if craft[key][i] > inventory[i]:
                                    #... we can't craft it!
                                    canBeMade = False
                                    break
                            #if we can craft it (we have all needed resources)
                            if canBeMade == True:
                                #take each item from the inventory
                                for i in craft[key]:
                                    inventory[i] -= craft[key][i]
                                    #add the crafted item to the inventory
                                    inventory[key] += 1
                    #PLACE if the mouse wasn't pressed
                    else:

                        #get the tile the player is standing on
                        currentTile = tilemap[playerPos[1]][playerPos[0]]
                        #if we have the item to place
                        if inventory[key] > 0:
                            #take it from the inventory
                            inventory[key] -= 1
                            #swap it with the tile we are standing on
                            inventory[currentTile] += 1
                            #place the item
                            tilemap[playerPos[1]][playerPos[0]] = key
    #loop through each row
    for row in range(MAPHEIGHT):
        #loop through each column in the row
        for column in range(MAPWIDTH):
            #draw the resource at that position in the tilemap, using the correct image
            DISPLAYSURF.blit(textures[tilemap[row][column]], (column*TILESIZE,row*TILESIZE))
    #display the player at the correct position
    DISPLAYSURF.blit(PLAYER,(playerPos[0]*TILESIZE,playerPos[1]*TILESIZE))

    #loop through each cloud
    for c in range(numcloud):
        #display the cloud
        DISPLAYSURF.blit(textures[CLOUD].convert_alpha(), (clouds[c].cloudx,clouds[c].cloudy))
        #move the cloud to the left slightly
        clouds[c].cloudx += clouds[c].cloudspd
        #if cloud has moved past the map
        if clouds[c].cloudx > MAPWIDTH*TILESIZE:
            #pick a new position to place the cloud
            clouds[c].cloudy = random.randint(0,MAPHEIGHT*TILESIZE)
            clouds[c].cloudx = -200

    #display the inventory, stating 10 pixels in
    placePosition = 10
    for item in resources:
        #add the image
        DISPLAYSURF.blit(textures[item],(placePosition, MAPHEIGHT*TILESIZE+20))
        placePosition += 30
        #add the text showing the amount in the inventory
        textObj = INVFONT.render(str(inventory[item]), True, WHITE, BLACK)
        DISPLAYSURF.blit(textObj,(placePosition,MAPHEIGHT*TILESIZE+20))
        placePosition += 50
    #update the display
    pygame.display.update()
    fpsClock.tick(24)