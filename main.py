import pygame as PG, time, random

import actors, constants, lists, tools, controls
import loadImages

scaledDir = (1, 1)
addDir = (1, 1)
#don't forget this!
#from constants import * 

print 'start2'

##----------------------------------------------------------------------
#def getScreen():
    #"""returns the screen object """
    
    #return screen

def init():
    '''initializes screen'''
    global screen
    #initializes pygame
    PG.init()
    #starts the screen
    screen = PG.display.set_mode((constants.WIDTH, constants.HEIGHT))  
    #fills the screen with a color
    screen.fill(constants.BACKGROUND)
    
    #loads joyticks to gamePad list
    controls.initJoysticks()
    

    
    global imageList
    imageList = loadImages.loadImages(r'./art/man/', 'png')
    
    #create a first Anything
    actors.spawnAnything(screen, imageList, (400, 400))  
    actors.Shooter(lists.ANYTHINGs[0])
    
    
    PG.display.flip()
    
    return screen



#----------------------------------------------------------------------
def gameLogic():
    """handles movement and AI"""
    
    for anything in lists.ANYTHINGs:
        
        
        #update, right now only checking to see if facing == direction
        anything.update()
        

    
    pass


#----------------------------------------------------------------------
def drawing():
    """draws objects to screen"""
    
    try:
        #paint background
        screen.fill(constants.BACKGROUND)
        
        #draw anythings
        for thing in lists.ANYTHINGs:
            thing.draw(screen)
       
        #draw lines to represent angles, if lines is true
        lines = 0
        if lines:
                
            addDir = tools.vectors.linkScaleVector(lists.ANYTHINGs[0].pos(),
                                                   lists.ANYTHINGs[0].direction,
                                                   100)
            points = [lists.ANYTHINGs[0].pos(), PG.mouse.get_pos(), addDir]
            PG.draw.lines(screen, constants.BLACK, True, points, 1)
            
            
            #draw line to represent players direction
            adjDir = tools.vectors.scale(lists.ANYTHINGs[0].direction, 25)
            adjDir = tools.vectors.add(lists.ANYTHINGs[0].pos(), adjDir)
            PG.draw.line(screen, constants.GREEN, lists.ANYTHINGs[0].pos(), addDir)
            
            
        if constants.FLAMES:
            #draws flames on at 100,100
            drawFlames(screen)
            #draw the flames that switch frames 3 times per second

        
        blits = 0
        if blits:
            screen.blit(lists.ANYTHINGs[0].surfaceBody, (100, 200))
            screen.blit(lists.ANYTHINGs[0].surfaceLimbs, (170, 200))
            screen.blit(lists.ANYTHINGs[0].surface, (240, 200))
            
        for bullet in lists.BULLETs:
            bullet.move()
            bullet.draw(screen)            
            
            
        #flip display to monitor
        PG.display.flip()
        
    except PG.error, message:
        print '\nGame Exited:'
        print message, '\n'
        
    #except UnboundLocalError:
        
        #screen.bllit(lists.flames[1], (100, 100))
        #flameNum = 0
        
    
    pass


#----------------------------------------------------------------------
def drawFlames(surface):
    """draw the flames that switch frames 3 times per second"""
    #draw the flames that switch frames 3 times per second
    
    flame = lists.flames[constants.flameNum]
    if constants.frameNum % 15 == 0:
        
        
        if constants.flameNum >= len(lists.flames) - 1:
            constants.flameNum = 0
        
        else:
            constants.flameNum += 1
        
        
        
        pass

    #blit to surface
    surface.blit(flame, (100, 100))    

#----------------------------------------------------------------------
def mainloop():
    """main game loop"""


    global  oldFrames
        
    #create a timer for FPS
    fpsTimer = PG.time.Clock()
    
    #init of fps counter
    oldFrames = PG.time.get_ticks()
    oldFrames = time.clock()
    
    #frame counter
    constants.frameNum = 0
    
    print 'starting main loop'
    
    global gameRunning
    gameRunning = True
    while gameRunning:
        
        #if quit event in in queue, quit
        if PG.event.peek(PG.QUIT):
            gameRunning = False
            break
        
        #handle input
        controls.inputHandler()

        #run logic
        gameLogic()
        
        #draw to screen
        drawing()
    
        
        
        
    
        #limit framerate
        fpsTimer.tick(constants.FRAMERATE)
        constants.frameNum += 1

        #every second, do:
        if constants.frameNum % constants.FRAMERATE == 0:
            pass
            
    else: print 'else exit loop'
    
    print 'mainloop is over, thanks for playing'


if __name__ == '__main__':
    """Run the following if module is top module"""
    screen = init()
    
    mainloop()
    
else:
    print __name__, 'wasnt ran as mainfile,', __package__
