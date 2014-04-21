########################################################################
class Tile(object):
    """A single tile, or cell"""

    #----------------------------------------------------------------------
    def __init__(self, coords, ID, color=(200, 0, 0)):
        """take all the coords that is inside the cell, and the ID,
         the top left coord """
        
        #all the points in the grid
        self.coords = coords
        #range of coords in the grid
        self.range_x = min(coords)[0], max(coords)[0]
        self.range_y = min(coords)[1], max(coords)[1]
        
        #the color of the tile
        # values is a randomly generated list of integers between 0 and 255
        self.color = color
        
        self.colorOriginal = (225,235,205)
        
        #creates a PyGamerect of the tile,
        # as well as certain important coords in it.
        self.set_rect()
        
        #id, how the AI will refer to this time
        self.ID = ID
        
        #the font that is used to show the ID on the screen
        #self.font = pygame.font.SysFont('Times', 10)

        self.unwalkable = False

        
        
        #finds all neighboring tiles
        #self.findNear()
        
        self.G = ''
        self.F = ''
        self.H = ''
        self.parent = ''
        
        #creates a surface with the height and width found in self.rect()
        #self.surface = pygame.surface.Surface((self.rect.w, abs(self.rect.h)))        
        #draw the cell for the first time
        self.draw()        
        
                
    #----------------------------------------------------------------------
    def set_rect(self):
        """returns the Pygame rect"""
        
        #smallest coord is the top left
        self.topLeft = min(self.coords)
        #biggest is the bottom right
        self.btmRight = max(self.coords)
        
        #some math to find the other corners
        self.topRight = self.btmRight[0], self.topLeft[1]
        self.btLeft = self.topLeft[0], self.btmRight[1]
        
        #as well as to find the width and height
        self.w = self.topRight[0] - self.topLeft[0]
        self.h = self.topRight[1] - self.btmRight[1]
        
        #finally, creating the rect
        #self.rect = pygame.Rect(self.topLeft, (self.w, self.h))
        
        
        
        
    #----------------------------------------------------------------------
    def draw(self):
        """returns a surf with a number in the middle of self"""
        
        ##creates a surface with the height and width found in self.rect()
        ##self.surface = pygame.surface.Surface((self.rect.w, abs(self.rect.h)))
        ##fills it in with a color, chosen on construction
        #self.surface.fill(self.color)
        #if self.unwalkable:
            #self.surface.fill((0, 0, 0))
        ##color key is the invisible color used when blitting
        ## I like this one, because it's quick to type.
        #self.surface.set_colorkey((123, 123, 123))
        
        ###draws the ID on a surface
        ##number = self.font.render('{}'.format(self.ID), 0, (0, 0, 0))
        ###blits (draws) the ID onto the top left corner of the tile
        ##self.surface.blit(number, (0, 0))
        
        #return self.surface
        pass
    
    #----------------------------------------------------------------------
    def changeColor(self, color='default'):
        """sets the color of the tilee"""
        
        if color == 'default':
            self.color = self.colorOriginal
            
        else:
            self.color = color
            
        print self.color
        
    #----------------------------------------------------------------------
    def findNear(self):
        """finds all the adjacent tiles"""
        print 'find near'
        self.nearby = []
        
        x, y = self.ID


        try:
            self.nRight = tiles[y][x + 1]
            self.nearby.append(self.nRight)
        except IndexError:
            self.nRight = 'None'
    #elif tile.ID == (x + 1, y + 1):
        try:
            self.nBtmRight = tiles[y+1][x + 1]
            self.nearby.append(self.nBtmRight)
        except IndexError:
            self.nBtmRight = 'None'
    #elif tile.ID == (x, y + 1):
        try:
            self.nBtm = tiles[y+1][x]
            self.nearby.append(self.nBtm)
        except IndexError:
            self.nBtm = 'None'
    #elif tile.ID == (x - 1, y + 1):
        try:
            self.nBtmLeft = tiles[y + 1][x - 1]
            self.nearby.append(self.nBtmLeft)
        except IndexError:
            self.nBtmLeft = 'None'
    #elif tile.ID == (x - 1, y):
        try:
            self.nLeft = tiles[y][x - 1]
            self.nearby.append(self.nLeft)
        except IndexError:
            self.nLeft = 'None'
    #elif tile.ID == (x - 1, y - 1):
        try:
            self.nTopLeft = tiles[y - 1][x - 1]
            self.nearby.append(self.nTopLeft)
        except IndexError:
            self.nTopLeft = 'None'
    #elif tile.ID == (x , y - 1):
        try:
            self.nTop = tiles[y-1][x]
            self.nearby.append(self.nTop)
        except IndexError:
            self.nTop = 'None'
    #elif tile.ID == (x + 1, y - 1):
        try:
            self.nTopRight = tiles[y- 1][x + 1]
            self.nearby.append(self.nTopRight)
        except:
            self.nTopRight = 'None'    
        #print "len nearby", len(self.nearby)


#----------------------------------------------------------------------
def createGrid():
    return
    """makes a list of grids topleft corners, and fills em in"""
    
    print 'starting grid'
    
    
    ##explicitly calling the size of the game
    width = 800
    height = 600
    cellsize = 25  #size of each cell
    #width = constants.WIDTH
    #height = constants.HEIGHT
    #cellsize = constants.CELLSIZE
    
    
    
    key_cords = []  #key cords are the topleft corner of the cell
    cells = {}  #dict of all the cells > coords
    global tiles, all_tiles
    tiles = []  #using this later, instead of returning. Will need to change
    all_tiles = []
    #Have to find the topleft corner of all the tiles in the game
    
    #for every row in the length of the height plus one, 
    # with an interval of cellsize
    for y in xrange(0, height+1, cellsize):
        #same thing for columns
        y_list = []
        for x in xrange(0, width+1, cellsize):
            #append the coord to key_cords
            
        

            #find all coordinates inside by adding a number between 0 and cellsize
            # eg +0,+1,+2...+cellsize
            cell = []
            for y2 in range(cellsize):
                for x2 in range(cellsize):
                    cell.append((x + x2, y + y2))
            #put the cell in a dict OR:        
            cells[(x, y)] = cell
            #or create a tile inst
            tile = Tile(cell, (x/cellsize, y/cellsize), (255, 255, 200))
            #if len(tiles) % 100 == 0:
                #tile.u`nwalkable = True 
            #tiles.append(tile)
            y_list.append(tile)
            all_tiles.append(tile)
        tiles.append(y_list)
   
    
    print 'Done building grid'
    
    print 'Finding neighbors'
    for tile in all_tiles:
        tile.findNear()    
    print 'Found all neighbors'    
    
    return tiles


createGrid()

print 'done all'