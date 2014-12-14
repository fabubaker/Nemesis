import pygame
from random import choice

# Colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
YELLOW   = ( 255, 255,   0)

# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player controls. """
 
    # Set speed vector
    change_x = 0
    change_y = 0
    
    walls = None
    bombs = None
    bullets = None

    #health
    health = 6
 
    # Constructor function
    def __init__(self, x, y):
        # Call the parent's constructor
        super(Player,self).__init__()

        #Loads all images for animation.
        self.images = [None]*12
        self.images[0] = pygame.image.load("sprites/hero/MoveB1.png").convert_alpha()        
        self.images[1] = pygame.image.load("sprites/hero/MoveB2.png").convert_alpha()     
        self.images[2] = pygame.image.load("sprites/hero/MoveF1.png").convert_alpha() 
        self.images[3] = pygame.image.load("sprites/hero/MoveF2.png").convert_alpha()         
        self.images[4] = pygame.image.load("sprites/hero/MoveL1.png").convert_alpha() 
        self.images[5] = pygame.image.load("sprites/hero/MoveL2.png").convert_alpha()    
        self.images[6] = pygame.image.load("sprites/hero/MoveR1.png").convert_alpha()    
        self.images[7] = pygame.image.load("sprites/hero/MoveR2.png").convert_alpha()    
        self.images[8] = pygame.image.load("sprites/hero/StandB.png").convert_alpha()
        self.images[9] = pygame.image.load("sprites/hero/StandF.png").convert_alpha()
        self.images[10] = pygame.image.load("sprites/hero/StandL.png").convert_alpha() 
        self.images[11] = pygame.image.load("sprites/hero/StandR.png").convert_alpha()

        #Load a list for move animation
        self.right_states = [self.images[11],self.images[6],self.images[7]]
        self.left_states = [self.images[10],self.images[4],self.images[5]]
        self.up_states = [self.images[9],self.images[2],self.images[3]]
        self.down_states = [self.images[8], self.images[0], self.images[1]]
        
        self.index = 0

        # Set picture of the player.    
        self.image = self.right_states[self.index]
        
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
 
        #variable to know whether key press is down or up.
        self.move = False

        #dx and dy for animation
        self.dx = 0
        self.dy = 0

        #Variable that holds player direction.
        self.direction = "E"

    def changespeed(self, x, y):
        """ Change the speed of the player. """
        self.change_x += x
        self.change_y += y

        self.dx = x
        self.dy = y
        
    def update(self):
        """ Update the player position. """
        #Character is moving. Animate movement.
        if self.move == True:
            #Move right.
            if self.dx > 0:
                self.animateMotion(self.right_states)
            #Move left.
            elif self.dx < 0:
                self.animateMotion(self.left_states)
            #Move down.
            elif self.dy > 0:
                self.animateMotion(self.down_states)
            #Move up.
            elif self.dy < 0:
                self.animateMotion(self.up_states)
        #Character stopped moving.
        else:
            #Stop right.
            if self.dx < 0:
                self.animateMotion([self.right_states[0]])
            #Stop left.
            elif self.dx > 0:
                self.animateMotion([self.left_states[0]])
            #Stop down.
            elif self.dy < 0:
                self.animateMotion([self.down_states[0]])
            #Stop up.
            elif self.dy > 0:
                self.animateMotion([self.up_states[0]])

        bombs_list = []
        
        for bomb in self.bombs.sprites():
            bomb.smaller_rect = bomb.rect.copy()
            bomb.smaller_rect.size = (20,20)
            bomb.smaller_rect.centerx = bomb.rect.centerx
            bomb.smaller_rect.centery = bomb.rect.centery
            bombs_list.append(bomb.smaller_rect)
            

        
        # Move left/right
        self.rect.x += self.change_x

        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)

        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of the item we hit
            
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        index = self.rect.collidelistall(bombs_list)
    
        if len(index) > 0:
            if self.change_x > 0:
                self.rect.right = bombs_list[index[0]].left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = bombs_list[index[0]].right
    
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

        index = self.rect.collidelistall(bombs_list)
    
        #
        if len(index) > 0:
            if self.change_y > 0:
                self.rect.bottom = bombs_list[index[0]].top
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.top = bombs_list[index[0]].bottom
        
        #Prevents player from going back a stage.
        if self.rect.x < 0:
            self.rect.x = 0

    #Function that animates the player character.
    def animateMotion(self, animateList):
        self.index +=1
        if self.index >= len(animateList):
            self.index = 0
        self.image = animateList[self.index]

class Virus(pygame.sprite.Sprite):
    #All objects to check for collision.
    all_collide_list = None

    '''Enemy virus that shoots lasers'''
    def __init__(self,x,y,width,height):
        #Inherit properties from parent class
        super(Virus,self).__init__()

        #Load picture.
        self.image = pygame.image.load("sprites/enemies/Virus.png").convert_alpha()

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        #Choose random motion for the enemy.
        self.dx = choice([-7,7])
        self.dy = choice([-7,7])
    
    def update(self):

        """ Update the enemy position. """
        
        # Move left/right
        self.rect.x += self.dx

        #Check for boundary collision.
        if self.rect.x > 790 or self.rect.x < 5:
            self.dx = -self.dx
            self.rect.x += self.dx

        if self.rect.y > 680 or self.rect.y < 5:
            self.dy = -self.dy
            self.rect.y += self.dy


        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.all_collide_list, False)
        count = 0
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of the item we hit
            if count < 1:
                if self.dx > 0:
                    
                    self.rect.right = block.rect.left
                else:
                    # Otherwise if we are moving left, do the opposite.
                    self.rect.left = block.rect.right
                
                self.dx = -self.dx
                self.rect.x += self.dx
                count += 1
            
        # Move up/down
        self.rect.y += self.dy
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.all_collide_list, False)
        count = 0
        for block in block_hit_list:
            if count < 1:
                if self.dy > 0:
                    self.rect.bottom = block.rect.top
                else:
                    self.rect.top = block.rect.bottom

                self.dy = -self.dy
                self.rect.y += self.dy
                count += 1

class Bug(pygame.sprite.Sprite):
    
    #All objects to check for collision.
    all_collide_list = None

    '''Enemy virus that shoots lasers'''
    def __init__(self,x,y,width,height):
        #Inherit properties from parent class
        super(Bug,self).__init__()

        #Load picture.
        self.image = pygame.image.load("sprites/enemies/Bug.png").convert_alpha()

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.dx = choice([-7,7])
        self.dy = choice([-7,7])
        
        

    def update(self):
    

        """ Update the enemy position. """
        
        # Move left/right
        self.rect.x += self.dx

        #Check for boundary collision.
        if self.rect.x > 790 or self.rect.x < 5:
            self.dx = -self.dx
            self.rect.x += self.dx

        if self.rect.y > 680 or self.rect.y < 5:
            self.dy = -self.dy
            self.rect.y += self.dy


        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.all_collide_list, False)
        count = 0
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of the item we hit
            if count < 1:
                if self.dx > 0:
                    
                    self.rect.right = block.rect.left
                else:
                    # Otherwise if we are moving left, do the opposite.
                    self.rect.left = block.rect.right
                
                self.dx = -self.dx
                self.rect.x += self.dx
                count += 1
            
        # Move up/down
        self.rect.y += self.dy
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.all_collide_list, False)
        count = 0
        for block in block_hit_list:
            if count < 1:
                if self.dy > 0:
                    self.rect.bottom = block.rect.top
                else:
                    self.rect.top = block.rect.bottom

                self.dy = -self.dy
                self.rect.y += self.dy
                count += 1

class Bullet(pygame.sprite.Sprite):
    '''Bullets that shoots from Virus'''
    def __init__(self,x,y):
        # Call the parent's constructor
        super(Bullet,self).__init__()

        self.image = pygame.Surface([5,10])
        self.image.fill(YELLOW)
        
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.direction = None

    def update(self):
        '''shoot the bullet and update its position'''
        
        if self.direction == "N":
            self.rect.y -= 10
        if self.direction == "S":
            self.rect.y += 10
        if self.direction == "E":
            self.rect.x += 10
        if self.direction == "W":
            self.rect.x -= 10

class Wall(pygame.sprite.Sprite):
    """ Wall the player can run into. """
    def __init__(self, x, y, width, height):
        """ Constructor for the wall that the player can run into. """
        # Call the parent's constructor
        super(Wall,self).__init__()
 
        # Make a black wall.
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

#Class for generating tiles across the map.
class Tile(pygame.sprite.Sprite):
    """ Wall the player can run into. """
    def __init__(self, x, y, width, height):
        """ Constructor for the wall that the player can run into. """
        # Call the parent's constructor
        super(Tile,self).__init__()
 
         # Set picture of the player.
        self.image = pygame.image.load("TilewoB.png").convert_alpha()
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
 
class RecursionBomb(pygame.sprite.Sprite):
    '''Recursion bombs that the player can throw'''
    def __init__(self):
        #Call parent constructor
        super(RecursionBomb,self).__init__()

        # Set the picture of the RBOMB.
        self.image = pygame.image.load("sprites/items/RecursionBomb.png").convert_alpha()

        #Set the location of the bomb.
        self.rect = self.image.get_rect()
     
        #Which way are you moving, Mr.Bomb?
        self.direction = None

        #Stay put, Mr. Bomb.
        self.move = False

        #Are you moving, Mr.Bomb?
        self.isMoving = False

        #Should you bounce, Mr.Bomb?
        self.bounce = False

    def shoot(self,direction):
        #Move bomb according to direction of player.
        if self.move == True:
            #The bomb is moving; keep rolling in the same direction.
            if self.isMoving == True:
                if self.direction == "N":
                    self.rect.y -= 10
                if self.direction == "S":
                    self.rect.y += 10
                if self.direction == "E":
                    self.rect.x += 10
                if self.direction == "W":
                    self.rect.x -= 10
            #The bomb isn't moving, make it move, nigga!
            elif self.isMoving == False:
                self.direction = direction
                self.isMoving = True
                if self.direction == "N":
                    self.rect.y -= 10
                if self.direction == "S":
                    self.rect.y += 10
                if self.direction == "E":
                    self.rect.x += 10
                if self.direction == "W":
                    self.rect.x -= 10
            
#Class that is used to draw hearts on screen.
class Heart(pygame.sprite.Sprite):

    def __init__(self,x,y):

        super(Heart,self).__init__()

        self.image = pygame.image.load("sprites/items/health.png")

        self.dx=x
        self.x =x
        self.y =y

        #Health that the player should have.
        self.number = 6

    #Draw the hearts on screen.
    def draw(self, screen):

        for number in range(0,self.number):
            self.x += 20
            screen.blit(self.image, (self.x+number*35,self.y))
        self.x = self.dx
            
#Class used for explosions and its animations.
class Explosion(pygame.sprite.Sprite):

    def __init__(self,x,y):

        super(Explosion,self).__init__()

        #Loads all images for animation.
        self.images = [None]*4
        self.images[0] = pygame.image.load("sprites/explosion_animation/Explosion1.png").convert_alpha()        
        self.images[1] = pygame.image.load("sprites/explosion_animation/Explosion2.png").convert_alpha()     
        self.images[2] = pygame.image.load("sprites/explosion_animation/Explosion3.png").convert_alpha() 

        self.states = [self.images[0], self.images[1], self.images[2]]

        self.index = 0

        self.image = self.images[0]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    #Animates the explosion.
    def update(self,all_exp_list):
        if self.index >= 3:
            self.index = 0
            all_exp_list.remove(self)
        self.image = self.states[self.index]
        self.index +=1

#Class used for teleport animations.
class Teleport(pygame.sprite.Sprite):

    def __init__(self,x,y):

        super(Teleport,self).__init__()

        #Loads all images for animation.
        self.images = [None]*4
        self.images[0] = pygame.image.load("sprites/teleport_animation/TP1.png").convert_alpha()        
        self.images[1] = pygame.image.load("sprites/teleport_animation/TP2.png").convert_alpha()     
        self.images[2] = pygame.image.load("sprites/teleport_animation/TP1.png").convert_alpha()        
        self.images[3] = pygame.image.load("sprites/teleport_animation/TP2.png").convert_alpha()     

        self.states = [self.images[0], self.images[1], self.images[2],self.images[3]]

        self.index = 0

        self.image = self.images[0]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    #Update the teleport animations with each frame.
    def update(self,all_tp_list):
        if self.index >= 4:
            self.index = 0
            all_tp_list.remove(self)
        self.image = self.states[self.index]
        self.index +=1

#Class used to contain forloops.
class ForLoop(pygame.sprite.Sprite):
    def __init__(self):

        super(ForLoop,self).__init__()

        self.image = pygame.image.load("sprites/items/ForLoop.png")

        self.rect = self.image.get_rect()
        
        self.direction = None
        
        self.isMoving = False
    
    def update(self,direction):

        #If the loop is already moving, keep 
        #updating it in that direction.
        #Else, retrieve direction from the player sprite
        #and update accordingly.

        if self.isMoving == False:
            self.direction = direction
            self.isMoving = True

        if self.direction == "N":
            self.rect.y -= 20
        if self.direction == "S":
            self.rect.y += 20
        if self.direction == "E":
            self.rect.x += 20
        if self.direction == "W":
            self.rect.x -= 20


#Class that is used to contain forloop pivot. 
#Mainly used just as a sprite for collision detection.
class ForLoopPivot(pygame.sprite.Sprite):
    def __init__(self,x,y):

        super(ForLoopPivot,self).__init__()

        self.image = pygame.image.load("sprites/items/ForLoopPivot.png")

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.width = 40
        self.rect.height = 40

#Function that handles resetting the game.
def playagain(screen):
    while True:
        '''Load all elements of the death screen'''

        font = pygame.font.Font("PressStart2P.ttf", 20)
        
        resume = font.render("Bill Gates is dead! Try again?", True, (239,0,0), (0,0,0))
        resumeRect = resume.get_rect()
        resumeRect.center = (400,360)
        
        yes = font.render('Yes!', True, (239,0,0), (0,0,0))
        yesRect = yes.get_rect()
        yesRect.center = (300,380)

        no = font.render("No.", True, (239,0,0), (0,0,0))
        noRect = no.get_rect()
        noRect.center = (550,380)

        mouse_pos = pygame.mouse.get_pos()

        #Wait for player input.
        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            return    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #If the player wants to replay the game;
            #Execute the main.py file.
            if yesRect.collidepoint(mouse_pos):
                exec file('main.py')
            #Else, close the program.
            if noRect.collidepoint(mouse_pos):
                return

        if yesRect.collidepoint(mouse_pos):
            yes = font.render('Yes!', True, (15,255,0), (0,0,0))
        if noRect.collidepoint(mouse_pos):
            no = font.render("No.", True, (15,255,0), (0,0,0))

        screen.blit(yes, yesRect)
        screen.blit(no, noRect)
        screen.blit(resume, resumeRect)
        pygame.display.flip()
    
    
#Function that handles resetting the game.
def win(screen):
    while True:
        '''Load all elements of the WIN screen'''

        font = pygame.font.Font("PressStart2P.ttf", 20)
        
        resume = font.render("You won! Play again?", True, (239,0,0), (0,0,0))
        resumeRect = resume.get_rect()
        resumeRect.center = (400,360)
        
        yes = font.render('Yes!', True, (239,0,0), (0,0,0))
        yesRect = yes.get_rect()
        yesRect.center = (300,380)

        no = font.render("No.", True, (239,0,0), (0,0,0))
        noRect = no.get_rect()
        noRect.center = (550,380)

        mouse_pos = pygame.mouse.get_pos()

        #Wait for player input.
        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            return    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #If player wants to play the game again;
            #execute the main.py file.
            if yesRect.collidepoint(mouse_pos):
                exec file('main.py')
            #Else, kill the program.
            if noRect.collidepoint(mouse_pos):
                return

        if yesRect.collidepoint(mouse_pos):
            yes = font.render('Yes!', True, (15,255,0), (0,0,0))
        if noRect.collidepoint(mouse_pos):
            no = font.render("No.", True, (15,255,0), (0,0,0))

        screen.blit(yes, yesRect)
        screen.blit(no, noRect)
        screen.blit(resume, resumeRect)
        pygame.display.flip()
