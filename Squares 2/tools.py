'''Tools for games'''

import math

import stats, visuals,  pygame
from Tkinter import *


def calcAngle(p1, p2):
    '''returns the rounded degrees different between two points
       uses: angle = math.atan2(Bx-Ax, By-Ay) '''
    
    #split up points
    Ax, Ay = p1
    Bx, By = p2
    
    #calc angle
    rad = math.atan2(Bx-Ax, By-Ay)
    #print rad
    
    #convert rad to degree
    degree =  math.degrees(rad)    
    
    return int(round(degree))
class Vector():
    

    def radToDeg(self, rad):
        #rad / (pi/180) = degree
        deg = rad / (3.14/180)
        return deg
        
    def degToRad(self, deg):
        #rad = degree * (pi/180)
        return deg * (3.14/180)
    
    def subtract(self, first,second):
        '''substract second from first'''
        print 'first,', first, 'second', second
        sub = tuple([b-a for a,b, in zip(first,second)])
        return sub
    
    def dot(self, *parts):
        
        list = []
        for part in parts:
            part = self.norm(part)
            list.append(part)
        
        dot =  (list[0][0] * list[1][0]) + (list[0][1]*list[1][1])
        print 'dot: ',dot
        return dot
    
    
    def revNorm(self, vector):
        '''reverses norm(), but doesn't'''
        x = vector[0]
        y = vector[1]
        
        #length
        revNormed = ((x*5),(y*5))
        
        return revNormed
    
    def norm(self, vector):
        
        x = vector[0]
        y = vector[1]
        #normalize a vector by dividing it by its length
        len = self.length(vector)
        try:
            normalized = ((x/len),(y/len))
        except ZeroDivisionError:
            normalized = (0,0)
        #print 'norm: ', normalized
        return normalized
    
    def length(self, vector):
        
        x = vector[0]
        y = vector[1]
        
        length =math.sqrt(( x**2 + y**2))
        #print 'length: ',length
        return length
    
    def distance(self, first, second):
        
        dist= tuple([b-a for a,b in zip(first,second)])
        dist = self.length(dist)
        
        #print 'distance: ', dist
        return dist

def createGrid():
    listOfGrids = []
    
    #go through all the pixels in a game screen
    for w in xrange(0, stats.WIDTH +1, 5):
        for h in xrange(0, stats.HEIGHT +1, 5):
            g =  Grid()
            g.origin = w, h
            listOfGrids.append(g)
            #print 'new grid started at', w, h
                
    print 'done gridding, now adding all the points to each grid'
    
    #for each grid in list, go through at add all the pixels it covers
    for grid in listOfGrids:
        origin =  grid.origin  #origin is the top left pixel of the grid
        for w in xrange(0, 5):
            for h in xrange(0, 5):
                grid.coords.append((origin[0] + w, origin[1] + h))
                #print 'added {0} to {1} grid'.format(new_coord, origin)
        #print grid.coords, 'length :', len(grid.coords) 
    print 'done adding all co-ords'
    
    return listOfGrids

#----------------------------------------------------------------------
class Grid:
    
    def __init__(self):
        """"""
        #coords are tuples of w, h pairs
        self.coords =  []
        
#----------------------------------------------------------------------
def inWhichGrid(coords, listOfGrids):
    """searches through all the grids to find the coords
        and returns grid origin"""
    
    for grid in listOfGrids:
        if coords.pos in grid.coords:
            #print 'found em in', grid.origin
            #draw a line to the grid
            visuals.drawLine(grid.origin, (100, 100), width= 5)
            pygame.display.flip()
            break
        
    else: print coords.pos, 'not found'


def seticon(iconname):
    """
    give an iconname, a bitmap sized 32x32 pixels, black (0,0,0) will be alpha channel
    
    the windowicon will be set to the bitmap, but the black pixels will be full alpha channel
     
    can only be called once after pygame.init() and before somewindow = pygame.display.set_mode()
    
    from:http://www.pygame.org/docs/ref/display.html#pygame.display.set_icon comments
    """
    #create a surface for icon
    icon=pygame.Surface((256,256))
    icon.set_colorkey((255,255,255))#and call that color transparent
    rawicon= pygame.image.load(iconname)#must be 32x32, black is transparent
    for i in range(0,256):
        for j in range(0,256):
            icon.set_at((i,j), rawicon.get_at((i,j)))
    #pygame.display.set_icon(icon)#set wind







def newOrLoad():
    
    ########################################################################
    class TitleScreen(Frame):
        """Create all the assets for a Title Screen"""
    
        #----------------------------------------------------------------------
        def __init__(self, master):
            Frame.__init__(self, master,)
            Label(self, text='New or Load?').grid(row = 0)
            Button(self, text='New', command=self.new).grid(column = 0, row = 1)
            Button(self, text='Load', command=self.load).grid(column = 1, row = 1)
            
        def new(self):
            stats.newOrLoad = 'New'
            root.destroy()
            
        def load(self):
            stats.newOrLoad = 'load'
            root.destroy()
            
    #----------------------------------------------------------------------
    def makeTitleScreen(frame):
        """create a title screen then blit to root"""
        
        title = TitleScreen(frame)
        
        title.grid()
        
        return title
        
    
    #----------------------------------------------------------------------
    def init():
        """load up title and prompt for new/load/quit"""
        
        root = Tk('Title Screen' )
        
        #create a titlescreen and send it to root
        title = makeTitleScreen(root)
        root.title('TITLE SCREEN')
        
        return root, title
    
    root, title = init()
    root.mainloop()
    return root,  title
    #print stats.NEWorSAVE
    
V = Vector()

