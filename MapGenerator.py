from GameObjects import *

'''Class used to generate each stage'''

class Stage(object):

    def __init__(self,file):

        
        self.maptext = open(file)
        
        self.wall_list = pygame.sprite.Group()
        self.tile_list = pygame.sprite.Group()
        self.tiles_walls_list = pygame.sprite.Group()
        self.virus_list = pygame.sprite.Group()
        self.bug_list = pygame.sprite.Group()
        self.pivot_list = pygame.sprite.Group()

    '''Function that generates a map given a text file'''

    def generateMap(self):

        row_counter = 0         #Used to detect y-axis.
        col_counter = 0         #Used to detect x-axis.
        for line in self.maptext:
            col_counter = 0
            for char in line:
                #Remove this line if \n is mapped to a tile. 
                #Else \n is replaced by a blank tile/ BG.
                if char == "#":
                    #This snippet intelligently places tiles on the screen using 
                    #x and y coordinates as well as the dimensions of the tile. 
                    wall = Wall(50*col_counter, 50*row_counter,50, 50)
                    self.wall_list.add(wall) 
                    self.tiles_walls_list.add(wall)
                if char == "=":
                    tile = Tile(50*col_counter, 50*row_counter,50, 50)
                    self.tile_list.add(tile)
                    self.tiles_walls_list.add(tile)
                if char == "X":
                    tile = Tile(50*col_counter, 50*row_counter,50, 50)
                    self.tile_list.add(tile)
                    self.tiles_walls_list.add(tile)
                    virus = Virus(50*col_counter, 50*row_counter,50, 50)
                    self.virus_list.add(virus)
                if char == "Y":
                    tile = Tile(50*col_counter, 50*row_counter,50, 50)
                    self.tile_list.add(tile)
                    self.tiles_walls_list.add(tile)
                    bug = Bug(50*col_counter, 50*row_counter,50, 50)
                    self.bug_list.add(bug)
                if char == "P":
                    tile = Tile(50*col_counter, 50*row_counter,50, 50)
                    self.tile_list.add(tile)
                    self.tiles_walls_list.add(tile)
                    pivot = ForLoopPivot(50*col_counter, 50*row_counter)
                    self.pivot_list.add(pivot)
                col_counter+=1
            row_counter += 1

    '''Function that overwrite global map variables with local map variables.'''

    def drawMap(self):

        return self.wall_list, self.tile_list, self.tiles_walls_list, self.virus_list, self.bug_list,  self.pivot_list

    '''Feed all enemies in the stage their collision objects'''

    def feedCollideObjs(self, collide_list):
        
        #Iterate through all the enemies and
        #feed them their collision objects.
        for obj in self.virus_list:
            obj.all_collide_list = collide_list
            obj.all_collide_list.remove(obj)
        for obj in self.bug_list:
            obj.all_collide_list = collide_list
            obj.all_collide_list.remove(obj)