'''

Nemesis v0.1.
Fadhil Abubaker.

Some code schemes have been obtained from : 
http://programarcadegames.com/index.php?chapter=introduction_to_sprites

Font obtained from:
http://www.fontspace.com/codeman38/press-start-2p"


'''

import pygame
from GameObjects import *
from MapGenerator import *
from random import choice

"""
Global constants
"""
 
# Map
mapfile1 = "maps/map1.txt"
mapfile2 = "maps/map2.txt"
mapfile3 = "maps/map3.txt"
mapfile4 = "maps/map4.txt"
mapfile5 = "maps/map5.txt"
mapfile6 = "maps/map6.txt"
mapfile7 = "maps/map7.txt"
mapfile8 = "maps/map8.txt"

#Text to display in help screen.
text = [ 
"It is the year 2106.",
"Microsoft has developed an advanced technology that can", 
"be used to travel inside computers.",
"The technology is named NEMESIS: Null Efficient Machine", 
"Emulation System Interface - Sigma,",
"and is equipped with a powerful A.I. called", 
"ABRXS: Advanced Biological Restructuring X System.",
"However, as with all Microsoft products, NEMESIS crashes", 
"and ABRXS goes evil.",
"A cryogenically frozen Bill Gates is awakened to save", 
"humanity from the clutches of ABRXS.",
"Bill Gates must travel inside the Microsoft", 
"mainframe and shut down ABRXS once and for all.",
"To aid his mission, he has with him",
"Recursion-Bombs and For-Loops to use",
"inside the mainframe to defeat various viruses and bugs", 
"and get to the evil A.I.",
"",
"",
"Use the Arrow Keys to move Bill Gates inside the",
"mainframe. Press 'a' to place a Recursion-Bomb, get near",
"the bomb and press 's' to shoot it. Press 'd' to release", 
"a for-loop, used to teleport Bill Gates to a pivot.",
"",
"The first stage is a practice stage. Good luck!"
]


# Colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
 
# Screen dimensions				
SCREEN_WIDTH  = 800     #Maptxt files must be 16 lines in width 
SCREEN_HEIGHT = 720 	#and 14 lines in height.
 
# Call this function so the Pygame library can initialize itself
pygame.init()
 
# Create an 800x720 sized screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

#Create a clock object to track FPS
clock = pygame.time.Clock()

# Set the title of the window
pygame.display.set_caption('Nemesis')
 
GameOver = True     #The game isn't running yet, so False.
mainMenu = True     #Main menu comes first, so True.
Help = False        #Help screen? Not yet. So False.

''' Display Main Menu'''
while mainMenu:

    '''Load menu elements'''

    Menutitle = pygame.sprite.Sprite()
    Menutitle.image = pygame.image.load("Menu/MenuTitle.png")
    Menutitle.rect = Menutitle.image.get_rect()
    Menutitle.rect.x = 100
    Menutitle.rect.y = 100
    
    ABRXS = pygame.sprite.Sprite()
    ABRXS.image = pygame.image.load("Menu/ABRXS.png")
    ABRXS.rect = ABRXS.image.get_rect()
    ABRXS.rect.x = 300
    ABRXS.rect.y = 250
    
    PlayButton = pygame.sprite.Sprite()
    PlayButton.image_list = [pygame.image.load("Menu/Play.png"), pygame.image.load("Menu/Play1.png")]
    PlayButton.image = PlayButton.image_list[0]
    PlayButton.rect=PlayButton.image_list[0].get_rect()
    PlayButton.rect.x = 20
    PlayButton.rect.y = 500
    
    HelpButton = pygame.sprite.Sprite()
    HelpButton.image_list = [pygame.image.load("Menu/Help.png"), pygame.image.load("Menu/Help1.png")]
    HelpButton.image = HelpButton.image_list[0]
    HelpButton.rect=HelpButton.image_list[0].get_rect()
    HelpButton.rect.x = 580
    HelpButton.rect.y = 500

    '''Display menu screen elements on screen'''

    screen.fill(BLACK)
    screen.blit(Menutitle.image,Menutitle.rect)
    screen.blit(ABRXS.image,ABRXS.rect)
    screen.blit(PlayButton.image,PlayButton.rect)
    screen.blit(HelpButton.image, HelpButton.rect)

    #Pull mouse position.
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainMenu = False    
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #Check for button presses on Play button.
            if PlayButton.rect.collidepoint(mouse_pos):
                mainMenu = False
                GameOver = False
            #Check for button presses on Help button.
            if HelpButton.rect.collidepoint(mouse_pos):
                mainMenu = False
                Help = True
    
    #Button animation upon mouse hover for Play button.
    if PlayButton.rect.collidepoint(mouse_pos):
        PlayButton.image = PlayButton.image_list[1]
        screen.blit(PlayButton.image,PlayButton.rect)
        
    #Button animation upon mouse hover for Help button.
    if HelpButton.rect.collidepoint(mouse_pos):
        HelpButton.image = HelpButton.image_list[1]
        screen.blit(HelpButton.image,HelpButton.rect)
    
    pygame.display.flip()
    clock.tick(20)

'''Trigger Help menu'''

while Help:
    screen.fill((0, 0, 0))
    font = pygame.font.Font("PressStart2P.ttf", 14)
    
    #Display the help text.
    for line in range(len(text)):
        textLine = font.render(text[line], True, (150, 150, 150), (0, 0, 0))
        textLineRect = textLine.get_rect()
        textLineRect.x = 10
        textLineRect.y = 20+20*line
        screen.blit(textLine, textLineRect)

    '''Load Help screen elements'''

    RBOMB = pygame.sprite.Sprite()
    RBOMB.image = pygame.image.load("sprites/items/RecursionBomb.png")
    RBOMB.rect = RBOMB.image.get_rect()
    RBOMB.rect.topleft = (10,550)
    bombtext = font.render("Recursion-Bomb", True, (150, 150, 150), (0, 0, 0))
    bombtextRect = bombtext.get_rect()
    bombtextRect.topleft = (65,570)
    
    FLOOP = pygame.sprite.Sprite()
    FLOOP.image = pygame.image.load("sprites/items/ForLoop.png")
    FLOOP.rect = FLOOP.image.get_rect()
    FLOOP.rect.topleft = (300,550)
    looptext = font.render("For-Loop", True, (150, 150, 150), (0, 0, 0))
    looptextRect = looptext.get_rect()
    looptextRect.topleft = (365,570)

    PIVOT = pygame.sprite.Sprite()
    PIVOT.image = pygame.image.load("sprites/items/ForLoopPivot.png")
    PIVOT.rect = PIVOT.image.get_rect()
    PIVOT.rect.topleft = (500,550)
    pivottext = font.render("Pivot", True, (150, 150, 150), (0, 0, 0))
    pivottextRect = pivottext.get_rect()
    pivottextRect.topleft = (570,570)

    PlayButton.image = PlayButton.image_list[0]
    PlayButton.rect.center = (400,670)

    '''Blit all the elements on screen'''

    screen.blit(bombtext, bombtextRect)
    screen.blit(RBOMB.image, RBOMB.rect)
    screen.blit(looptext, looptextRect)
    screen.blit(FLOOP.image, FLOOP.rect)
    screen.blit(pivottext, pivottextRect)
    screen.blit(PIVOT.image, PIVOT.rect)
    screen.blit(PlayButton.image,PlayButton.rect)

    #Pull mouse position.
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Help = False    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #Check if the play button has been pressed.
            if PlayButton.rect.collidepoint(mouse_pos):
                #Garbage Collection:
                del(RBOMB,FLOOP,PIVOT,bombtext,looptext,pivottext,textLine, textLineRect)
                #Help is over. Time for Fun.
                Help = False
                #Begin Game!
                GameOver = False
    
    #Toggle Play button upon mouse hover.
    if PlayButton.rect.collidepoint(mouse_pos):
        PlayButton.image = PlayButton.image_list[1]
        screen.blit(PlayButton.image,PlayButton.rect)
 
    pygame.display.update()
    clock.tick(20)

#Garbage collection:
del(Menutitle, PlayButton,HelpButton,ABRXS)

'''Pygame Sprite Groups'''

# List to hold tiles and walls.
tiles_walls_list = pygame.sprite.Group()
 
# Make the walls. (x_pos, y_pos, width, height)
wall_list = pygame.sprite.Group()
 
# List to hold tiles.
tile_list = pygame.sprite.Group()

# List to hold recursion bombs
bombs_list = pygame.sprite.Group()
#How many bombs on stage?
bomb_count = 0
#How many bounces off walls?
bomb_bounce_count = 0

#List to hold Enemy viruses
virus_list = pygame.sprite.Group()

#List to hold Enemy bugs
bug_list = pygame.sprite.Group()

#List to hold bullets
bullets_list = pygame.sprite.Group()

#List that holds all enemies.
all_enemies_list = pygame.sprite.Group()

#List that holds all explosions. Damn, that's one volatile list.
explosions_list = pygame.sprite.Group()

#List that holds all teleportations. Beam me up, Scotty!
teleportations_list = pygame.sprite.Group()

#List that holds all forLoops. 
forloop_list = pygame.sprite.Group()
#How many forloops on stage?
forloop_count = 0

#List thath holds all forloopPivots. 
pivot_list = pygame.sprite.Group()

#health bar
Health_bar = Heart(0,660)

'''Load Stages onto variables'''

#Set current stage to 1.
currentStage = 1

Stage1 = Stage(mapfile1)
Stage1.generateMap()    # We start with the first stage, so generate the required variables.

Stage2 = Stage(mapfile2)

Stage3 = Stage(mapfile3)

Stage4 = Stage(mapfile4)

Stage5 = Stage(mapfile5)

Stage6 = Stage(mapfile6)

Stage7 = Stage(mapfile7)

Stage8 = Stage(mapfile8)

#map dictionary
mapDict = {1:Stage1, 2:Stage2, 3:Stage3,4:Stage4,5:Stage5,6:Stage6,7:Stage7,8:Stage8}
 
#Begin game with Stage1.
wall_list,tile_list,tiles_walls_list, virus_list, bug_list, pivot_list = Stage1.drawMap()

#Group together all enemy sprites.
all_enemies_list.add(virus_list)
all_enemies_list.add(bug_list)

#Add bugs and viruses and walls to master list. This is for collision detection
#for enemy objects only.
all_collide_list = pygame.sprite.Group()
all_collide_list.add(virus_list)
all_collide_list.add(bug_list)
all_collide_list.add(wall_list)
all_collide_list.add(pivot_list)

#Update collision objects for all enemy sprites in current stage.
Stage1.feedCollideObjs(all_collide_list)

# Create the player object
player = Player(0, 250)
player.walls = wall_list       #Feed the player the objects to check for collision detection.
player.bombs = bombs_list      #Feed the player the bombs for shooting.
player.bullets = bullets_list  #Feed the player the bullets to check for collision detection.


'''Gameloop begins'''

while not GameOver:
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameOver = True
 
        # Check key presses for character movement.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.direction = "W"
                player.move = True
                player.changespeed(-9, 0)
            if event.key == pygame.K_RIGHT:
                player.direction = "E"
                player.move = True
                player.changespeed(9, 0)
            if event.key == pygame.K_UP:
                player.direction = "N"
                player.move = True
                player.changespeed(0, -9)
            if event.key == pygame.K_DOWN:
                player.direction = "S"
                player.move = True
                player.changespeed(0, 9)
            
            # Check for bomb placement upon pressing 'a'.
            if event.key == pygame.K_a:
                # Max of three bombs on stage : (0,1,2)
                if bomb_count <= 2:
                    
                    #Place bomb depending on player direction.
                    if player.direction == "N":
                        Bomb = RecursionBomb()
                        Bomb.rect.x = player.rect.x
                        Bomb.rect.y = player.rect.y-60
                    elif player.direction == "S":
                        Bomb = RecursionBomb()
                        Bomb.rect.x = player.rect.x
                        Bomb.rect.y = player.rect.y+50
                    elif player.direction == "E":
                        Bomb = RecursionBomb()
                        Bomb.rect.x = player.rect.x+50
                        Bomb.rect.y = player.rect.y
                    elif player.direction == "W":
                        Bomb = RecursionBomb()
                        Bomb.rect.x = player.rect.x-60
                        Bomb.rect.y = player.rect.y
                    
                    #Only place bomb if it does not collide with another bomb or an enemy.
                    bombOverlap_hit_list = pygame.sprite.spritecollide(Bomb, bombs_list, False)
                    bombOverlap_hit_list2 = pygame.sprite.spritecollide(Bomb,all_enemies_list,False)
                    if len(bombOverlap_hit_list) == 0 and len(bombOverlap_hit_list2) == 0:
                        bomb_count += 1
                        bombs_list.add(Bomb)
            		
            # Pressed 's'? Shoot bomb!
            if event.key == pygame.K_s:
                #Check if player is in range of bomb.
                bombshoot_hit_list = pygame.sprite.spritecollide(player, bombs_list, False)
                if len(bombshoot_hit_list) > 0:
                    #Prevent initiaitng bombs before blitting them.
                    for bombs in bombshoot_hit_list:
                        bombs.move = True

            #Pressed 'd'? Teleport!
            if event.key == pygame.K_d:
                if forloop_count < 1:
                    # Shoot loops in direction of player.
                    if player.direction == "N":
                        forloop = ForLoop()
                        forloop.image = pygame.transform.rotate(forloop.image,90)
                        forloop.rect.x = player.rect.x
                        forloop.rect.y = player.rect.y-60
                    elif player.direction == "S":
                        forloop = ForLoop()
                        forloop.image = pygame.transform.rotate(forloop.image,270)
                        forloop.rect.x = player.rect.x
                        forloop.rect.y = player.rect.y+50
                    elif player.direction == "E":
                        forloop = ForLoop()
                        forloop.rect.x = player.rect.x+50
                        forloop.rect.y = player.rect.y
                    elif player.direction == "W":
                        forloop = ForLoop()
                        forloop.image = pygame.transform.rotate(forloop.image,180)
                        forloop.rect.x = player.rect.x-60
                        forloop.rect.y = player.rect.y
                    forloop_list.add(forloop)
                

        # Check if a key has been released.
        elif event.type == pygame.KEYUP:
            # If key released is one of the arrow
            # keys, do a fancy walking animation.

            if event.key == pygame.K_LEFT:
                player.direction = "W"
                player.move = False
                player.changespeed(9, 0)
            if event.key == pygame.K_RIGHT:
                player.direction = "E"
                player.move = False
                player.changespeed(-9, 0)
            if event.key == pygame.K_UP:
                player.direction = "N"
                player.move = False
                player.changespeed(0, 9)
            if event.key == pygame.K_DOWN:
                player.direction = "S"
                player.move = False
                player.changespeed(0, -9)
 
    #Fire bullets randomly!
    for enemy in all_enemies_list:
        
        #Has a one in 30 chance of shooting.
        #If you ask me, this enemy is too trigger happy. ^_^
        shoot =  choice(range(0,31))
        if shoot == 0:
            bullet = Bullet(enemy.rect.x, enemy.rect.y)
            bullet.direction = choice(["N","S","E","W"])
            bullets_list.add(bullet)
            

    #Check for bomb collisions.
    for bombs in bombs_list:
        bombs.shoot(player.direction)

        # When ypu place a bomb, this bomb bounces off incoming enemies; 
        # doesn't actually destroy them.
        # Perform that collision.
        for enemy in all_enemies_list: 
            enemy.all_collide_list.add(bombs)
        
        # Destroy all enemies if a bomb is moving!
        if bombs.move == True:
	        #Check if bomb hits an enemy.
            enemy_hit_list = pygame.sprite.spritecollide(bombs, all_enemies_list, True)
            for enemy in enemy_hit_list:
                newExplosion = Explosion(enemy.rect.x,enemy.rect.y) 
                explosions_list.add(newExplosion)
                
	        # So long as the bomb hits an enemy, explode it and
            # remove it from the game.
            if enemy_hit_list != []:
	        	bombs_list.remove(bombs)
	        	bomb_count -= 1
	        		        	
    		#Check if bomb hits another bomb.
            temp_bombs_list = bombs_list.copy()
            temp_bombs_list.remove(bombs)
            bombshoot_hit_list = pygame.sprite.spritecollide(bombs, temp_bombs_list, True)
            
            # If the bomb hits another bomb, remove all bombs.
            if bombshoot_hit_list:
                bombs_list.remove(bombs)
                bomb_count -= 1
                #Perform an explosion animation.
                for element in bombshoot_hit_list:
                    newExplosion = Explosion(element.rect.x,element.rect.y) 
                    explosions_list.add(newExplosion)
                    bomb_count -= 1

        

        #Check if bomb is out of screen.
        if bombs.rect.y < 0 or bombs.rect.y > 700:
            #Remove bomb from screen
            bombs_list.remove(bombs)
            bomb_count -= 1
            
            
        #Check if bomb is out of screen.
        elif bombs.rect.x < 0 or bombs.rect.x > 800:
            #Remove bomb from screen
            bombs_list.remove(bombs)
            bomb_count -= 1
    
	#Check for player collision with enemies.
    enemy_hit_list = pygame.sprite.spritecollide(player, all_enemies_list, False)
    for enemy in enemy_hit_list:
        newExplosion = Explosion(player.rect.x,player.rect.y) 
        explosions_list.add(newExplosion)

        #Reduce health if the player has collided with an enemy.
        player.health -= 1
        Health_bar.number -= 1
        
        #Bounce the enemies off of the player.
        enemy.dx = -enemy.dx
        enemy.rect.x += enemy.dx
        enemy.dy = -enemy.dy
        enemy.rect.y += enemy.dy 

    #Check for player collision with bullets.
    bullets_hit_list = pygame.sprite.spritecollide(player, bullets_list, True)
    for bullet in bullets_hit_list:
        #Perform an explosion animation.
        newExplosion = Explosion(player.rect.x,player.rect.y) 
        explosions_list.add(newExplosion)
        #Reduce player health.
        player.health -= 1
        #Update health bar animation.
        Health_bar.number -= 1

    #Check for bombs collision with bullets.
    bullet_bomb_hit_list = pygame.sprite.groupcollide(bullets_list,bombs_list,True,True)
    for bullet in bullet_bomb_hit_list:
        newExplosion = Explosion(bullet.rect.x,bullet.rect.y) 
        explosions_list.add(newExplosion)
        bomb_count -= 1

    #Check if bullet went out of the wall.
    for bullet in bullets_list:
        if bullet.rect.x > 800 or bullet.rect.x < 0 or bullet.rect.y > 700 or bullet.rect.y < 0:
            bullets_list.remove(bullet)

    #Check for forloop collision with a forloop pivot.
    forloop_hit_list = pygame.sprite.groupcollide(forloop_list, pivot_list,True,False)
    for loop in forloop_hit_list:
        newTeleportation = Teleport(player.rect.x,player.rect.y)
        teleportations_list.add(newTeleportation)
        player.rect.x = forloop_hit_list[loop][0].rect.x
        player.rect.y = forloop_hit_list[loop][0].rect.y
        newTeleportation = Teleport(player.rect.x,player.rect.y)
        teleportations_list.add(newTeleportation)

    #Check if a forloop went out of screen.
    for loop in forloop_list:
        if loop.rect.x > 800 or loop.rect.x < 0 or loop.rect.y > 700 or loop.rect.y < 0:
            forloop_list.remove(loop)
            forloop_count -= 1            

    if player.rect.x > 780 and len(all_enemies_list) == 0:
    	#Clear all level sprites.
        wall_list.empty()
        tile_list.empty()
        tiles_walls_list.empty() 
        virus_list.empty()
        bug_list.empty()
        all_enemies_list.empty()
        all_collide_list.empty()
        bombs_list.empty()
        pivot_list.empty()

        #Reset bomb count.
        bomb_count = 0

        #Increment stage by 1.
        currentStage += 1

        #If final stage, display win screen. SO MUCH WIN!
        if currentStage == 9:
            win(screen)

        #Depending on the current stage picked,
        #generate all the variables for it.
        mapDict[currentStage].generateMap()
        
        #Update these variables.
        wall_list,tile_list,tiles_walls_list, virus_list, bug_list, pivot_list = mapDict[currentStage].drawMap()
        all_enemies_list.add(virus_list)
        all_enemies_list.add(bug_list)

        #Add bugs and viruses and walls to master list. This is for collision detection
        #for enemy objects only.
        all_collide_list = pygame.sprite.Group()
        all_collide_list.add(virus_list)
        all_collide_list.add(bug_list)
        all_collide_list.add(wall_list)
        all_collide_list.add(pivot_list)

        #Feed all the objects required for collision for the enemies.
        mapDict[currentStage].feedCollideObjs(all_collide_list)
        
        #Feed the player the objects to check for collision detection.
        player.walls = wall_list       
        player.bombs = bombs_list           

        #Respawn player in new level. 
        player.rect.x = 0
        player.rect.y = 250

    #If player goes out of the screen without killing all enemies,
    #BAD PLAYER! DON'T GO ANYWHERE!
    elif player.rect.x > 780:
        player.rect.x = 780

    #Player goes out vertically off the screen;
    #keep the character in the screen.
    if player.rect.y > 720:
        player.rect.y = 720

    if player.rect.y < 0:
        player.rect.y = 0
    
    #If player dies, display reset screen.
    if player.health <= 0:
        GameOver = True
        playagain(screen)

    screen.fill(BLACK)

    #Update player position on screen based on changed input values.
    player.update()

    ''' Update the position of all the game elements'''

    all_enemies_list.update()

    bullets_list.update()

    explosions_list.update(explosions_list)

    forloop_list.update(player.direction)

    teleportations_list.update(teleportations_list)

    '''Draw all the game elements on screen'''

    #Draw all tiles and walls on screen.
    tiles_walls_list.draw(screen)

    #Draw all those pesky lil bugs and draw all da viri, virii, viruses, virus?
    all_enemies_list.draw(screen)

    #Draw all da bullets.
    bullets_list.draw(screen)

    #Draw all da bombs.
    bombs_list.draw(screen)

    #Draw da health bar. Yum.
    Health_bar.draw(screen)

    #Draw da frooty loops.
    forloop_list.draw(screen)

    #Draw the frooty loop pivots.
    pivot_list.draw(screen)

    #Draw the player along with his new position.
    screen.blit(player.image, player.rect)
    
    #Draw all da EXPLOSIONS! BOOM BOOM KABOOM!
    explosions_list.draw(screen)

    #Draw the teleporations. FFFZOOOP.
    teleportations_list.draw(screen)

    #Flip the pygame display.
    pygame.display.flip()
 
    clock.tick(20)      #Standard tick is 20. Keep it.
 
pygame.quit()









