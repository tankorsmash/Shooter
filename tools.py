'''random tools for the project'''

import math, pygame

import constants
#----------------------------------------------------------------------
def loadTextFile(filepath):
    """loads a textfile to a variable, returns a list of lines"""
    
    #open filepath, read data
    with open(filepath, 'r') as f:
        
        #create a list to hold lines
        data = []
        #fetch lines
        for line in f.readlines():
            line = line.rstrip()
            data.append(line)
            
        #return list of lines
        return data
    
    
########################################################################
class Vector(object):
    """class for doing vector math, imports math"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        pass
    
    
    #----------------------------------------------------------------------
    def normalize(self, vector):
        """divide each component by the length of the vector"""
        
        x = vector[0]
        y = vector[1]
        
        length = self.length(vector)
        
        nX = x / length
        nY = y / length
        
        return nX, nY            
                
    #----------------------------------------------------------------------
    def rotate(self, vector, degree):
        """rotates a vector by degrees"""
        
        x, y = vector
        
        theta = math.radians(degree)
        
        cs = math.cos(theta)
        sn = math.sin(theta)
        
        px = x * cs - y * sn
        py = x * sn + y * cs
        
        #return (round(px, 10), round(py, 10))
        px, py = self.normalize((px, py))
        
        return px, py
    
    #----------------------------------------------------------------------
    def length(self, vector):
        """length of a vector with pythagoras"""
        
        #x **2 + y **2
        a = (vector[0]**2 + vector[1]**2)
        
        length = math.sqrt(a)
        
        return length
    
    #----------------------------------------------------------------------
    def distance(self, p1, p2):
        """distance between two vectors:
           length of the differential vector length(p2-p1)"""
        
        diff = self.sub(p1, p2)
        
        len = self.length(diff)
        
        return len
        
        
        
    #----------------------------------------------------------------------
    def scale(self, v, scale):
        """scale the vector bigger or smaller"""
        
        x = v[0] * scale
        y = v[1] * scale
        
        return x, y
    
    #----------------------------------------------------------------------
    def add(self, V1, V2):
        """add two vectors"""
        #change pos
        x,y = V1
        x += V2[0]
        y += V2[1]
        return x, y
  
    #----------------------------------------------------------------------
    def sub(self, V1, V2):
        """subract v2 from v1"""
        
        x = V1[0] - V2[0]
        y = V1[1] - V2[1]
        
        return x, y
    
    def angle(self, o, p1, p2):
        '''the angle between two points around origin
        
        eq= len(op1)**2 + len(op2)**2 - len(p1p2)**2 over
             / 2*len(op1)*len(op2) '''

        ##norm both points
        #p1 = self.normalize(p1)
        #p2 = self.normalize(p2)
        
        
        #lengths of both points from origin
        a = self.distance(o, p1)
        b = self.distance(o, p2)
        c = self.distance(p1, p2)
        
        #print 'distance of a, b, c:', a, b, c       
        
        
        #main equation
        cosC = (a ** 2 + b ** 2 - c ** 2) / (2 * a * b)
        #print 'result of equation', cosC
        
        
        ##solve cos with var cosC
        #Ccos = math.cos(cosC)
        #print 'used equations result and cosd it', Ccos
        
        try:
            
            C = math.acos(cosC)
            
        except ValueError:
            C = 0
        #print 'angle between the two points in relation to origin in rads', C
        
        #value in degrees
        angle = math.degrees(C)
        #print 'C in degrees', degC
        return round(angle, 2)
        
        
    #----------------------------------------------------------------------
    def sineRule(self, a='coord', bVec='velocity', c='coord'):
        """uses the triangle rule returns rounded angle to two places
            also treats bVec as a velocity away from c(player)"""
        
        #distance of c to a
        lenCA = self.distance(c, a)
        
        #make c to b the same distance #maybe not needed though
        scaledCB = self.scale(bVec, lenCA)
        
        #joinedBC is not the same length as CA
        b = self.add(c, scaledCB)
        
        #to find the and of C corner
        angle = self.angle(a, b, c)
        
        return round(angle)
        
        
        
    #----------------------------------------------------------------------
    def rectPerimeter(self, rect, (dx, dy)):
        """returns a list two points of a slope on dx,dy
        relative to 0,0 as center on the perimeter of rect
        
        """
        dx = float(dx)
        dy = float(dy)
        
        
        Y = (rect.w / 2,
             rect.h / 2)
        
        xs = []
        for Y in Y:
            
            try:
                X = Y / (dy / dx)
            except ZeroDivisionError:
                X = Y
                
            xs.append(X)
    
        #return [Wpoint, Hpoint]
        twoPoints = (xs[0], Y), (xs[1], Y)
        
        twoPack = []
        #for both points
        for pair in twoPoints:
            pack = []
            #add center to pair
            pair = self.add(pair, rect.center)
            
            for coord in pair:                
                integer = int(round(coord))
                pack.append(integer)
                
            twoPack.append(pack)
            
        print 'first and second pack', twoPack[0], twoPack[1]    
        return twoPack
    
    #----------------------------------------------------------------------
    def intersect_perimeter(self, x, y, w, h):
        """finds the intersection in a rectangle"""
        
        #if check which side to put the point on
        if abs(y*w) > abs(x*h):
            return (int(0.5*h * x/abs(y)), int(0.5*h * sign(y)))
        else:
            return (int(0.5*w * sign(x)), int(0.5*w * y/abs(x)))        
    

    #----------------------------------------------------------------------
    def angleOfTwoPoints(self, corner, start, end):
        """calculates the angle between two points, start and end,
         from corner as origin"""
        
        ##find the length between object and other's postion
        #cornerToEnd = self.distance(corner, end)
        ##multiply that distance to the direction of the object
        #scaledCTE = self.scale(start, cornerToEnd)
        ##combined vector of postion and direction to properly 
        ## place the direction on the cartesian plane
        #addCTE = self.add(corner, scaledCTE)
        ##calc angle between pos, dir, other
        #angle =  self.angle(corner, addCTE, end)
        
        ##-------
        
        #combined vector of postion and direction to properly 
        # place the direction on the cartesian plane
        addCTE = self.add(corner, start)
        #calc angle between pos, dir, other
        angle =  self.angle(corner, addCTE, end)
        
        #print '### angle between direction and mouse ###', angle
 
        return round(angle)
        
    #----------------------------------------------------------------------
    def linkScaleVector(self, origin, sat, scale):
        """used for pos and directio, scales the satellite vector to scale
           and adds it to origin"""
        
        scaled = self.scale(sat, scale)
        
        added = self.add(origin, scaled)
        
        return added
                
    

def angleBetweenTwoPoints(p1, p2):
    '''return in angle in deg of the angle between two points'''
    #old way 0-360
    a1 = math.atan2(p1[1], p1[0])
    a2 = math.atan2(p2[1], p2[0])
    angle1 = (a1 - a2) % (2 * math.pi)
    angle1 = math.degrees(angle1)
    #print 'first way :', angle1
    
    #new way seems to work better -180 - 180
    x = p2[0] - p1[0]
    y = p2[1] - p1[1]
    angle2 = math.atan2(y, x)  #* (180 / math.pi)
    angle2 = math.degrees(angle2)
    #print 'second way:', angle2
    
    return round(angle1)

#----------------------------------------------------------------------
def sign(x):
    """returns the sign of x: -1, 0, or 1"""
    
    return cmp(x, 0)


#----------------------------------------------------------------------
def distBetweenTwoPoints(p1, p2):
    """Calculates the distance between two points"""
    
    x = p2[0] - p1[0]
    y = p2[1] - p1[1]    

    return x, y


#----------------------------------------------------------------------
def createGrid():
    """makes a list of grids topleft corners, and fills em in"""
    
    print 'starting grid'
    
    
    ##explicitly calling the size of the game
    #width = 800
    #height = 600
    #cellsize = 25  #size of each cell
    width = constants.WIDTH
    height = constants.HEIGHT
    cellsize = constants.CELLSIZE
    
    
    
    key_cords = []  #key cords are the topleft corner of the cell
    cells = {}  #dict of all the cells > coords
    global tiles
    tiles = []  #using this later, instead of returning. Will need to change
    
    #Have to find the topleft corner of all the tiles in the game
    
    #for every row in the length of the height plus one, 
    # with an interval of cellsize
    for y in xrange(0, height+1, cellsize):
        #same thing for columns
        for x in xrange(0, width+1, cellsize):
            #append the coord to key_cords
            key_cords.append((x, y))
            
    #for each corner/key coordinate
    for corner in key_cords:
        #find all coordinates inside by adding a number between 0 and cellsize
        # eg +0,+1,+2...+cellsize
        cell = []
        for y in range(cellsize):
            for x in range(cellsize):
                cell.append((corner[0] + x, corner[1] + y))
        #put the cell in a dict OR:        
        cells[corner] = cell
        #or create a tile inst
        tile = Tile(cell, (corner[0]/cellsize, corner[1]/cellsize), (255, 255, 200))
        if len(tiles) % 100 == 0:
            tile.unwalkable = True 
        tiles.append(tile)
        
   
    
    print 'Done building grid'
    
    print 'Finding neighbors'
    for tile in tiles:
        tile.findNear()    
    print 'Found all neighbors'    
    
    return tiles


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
        self.font = pygame.font.SysFont('Times', 10)

        self.unwalkable = False

        
        
        #finds all neighboring tiles
        #self.findNear()
        
        self.G = ''
        self.F = ''
        self.H = ''
        self.parent = ''
        
        #creates a surface with the height and width found in self.rect()
        self.surface = pygame.surface.Surface((self.rect.w, abs(self.rect.h)))        
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
        self.rect = pygame.Rect(self.topLeft, (self.w, self.h))
        
        
        
        
    #----------------------------------------------------------------------
    def draw(self):
        """returns a surf with a number in the middle of self"""
        
        ##creates a surface with the height and width found in self.rect()
        #self.surface = pygame.surface.Surface((self.rect.w, abs(self.rect.h)))
        #fills it in with a color, chosen on construction
        self.surface.fill(self.color)
        if self.unwalkable:
            self.surface.fill((0, 0, 0))
        #color key is the invisible color used when blitting
        # I like this one, because it's quick to type.
        self.surface.set_colorkey((123, 123, 123))
        
        ##draws the ID on a surface
        #number = self.font.render('{}'.format(self.ID), 0, (0, 0, 0))
        ##blits (draws) the ID onto the top left corner of the tile
        #self.surface.blit(number, (0, 0))
        
        return self.surface
    
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
        
        self.nearby = []
        
        x, y = self.ID

        #find all the neighbors, gotta be a better way
        for tile in tiles:
            if tile.ID == (x + 1, y):
                self.nRight = tile
                self.nearby.append(tile)
            elif tile.ID == (x + 1, y + 1):
                self.nBtmRight = tile
                self.nearby.append(tile)
            elif tile.ID == (x, y + 1):
                self.nBtm = tile
                self.nearby.append(tile)
            elif tile.ID == (x - 1, y + 1):
                self.nBtmLeft = tile
                self.nearby.append(tile)
            elif tile.ID == (x - 1, y):
                self.nLeft = tile
                self.nearby.append(tile)
            elif tile.ID == (x - 1, y - 1):
                self.nTopLeft = tile
                self.nearby.append(tile)
            elif tile.ID == (x , y - 1):
                self.nTop = tile
                self.nearby.append(tile)
            elif tile.ID == (x + 1, y - 1):
                self.nTopRight = tile
                self.nearby.append(tile)
                
        #print "len nearby", len(self.nearby)


vectors = Vector()


#----------------------------------------------------------------------
def createSurface(w, h, fill='trans', key='trans'):
    """creates a PyGame surface with a fill and colorkey"""
    
    if fill == 'trans':
        fill = constants.TRANS
    if key == 'trans':
        key = constants.TRANS
    
    surface = pygame.surface.Surface((w, h))
    surface.fill(fill)
    surface.set_colorkey(key)
    
    return surface

if __name__ == '__main__':
    """Run the following if module is top module"""
    
    #test
    loadTextFile(r'AmericanMaleNames.txt')