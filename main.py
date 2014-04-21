import pygame as PG, time, random, sys, datetime

import actors, constants, lists, toolsV2, controls
import loadImages, dialogs

scaledDir = (1, 1)
addDir = (1, 1) 
#don't forget this!sdd
#from constants import * 

print 'start2'

##----------------------------------------------------------------------
#def getScreen():
    #"""returns the screen object """
    
    #return screen

def init():
    '''initializes screen'''
    global screen, background_surface
    #initializes pygame
    PG.init()
    

    #starts the screen
    screen = PG.display.set_mode((constants.WIDTH, constants.HEIGHT))
    
    #set Icon, may not work off windows
    icon = loadImages.loadImages(r'./art/man/', 'png')
    icon = icon[7]
    PG.display.set_icon(icon)    
    
    #fills the screen with a color
    screen.fill(constants.BACKGROUND)
    
    #loads the background image
    background_surface = loadImages.loadImages(r'./art/backgrounds/',
                                                       r'pond.png',
                                                       (screen.get_rect().w,
                                                        screen.get_rect().h))
    background_surface = background_surface.convert()
    
    screen.blit(background_surface, (0, 0))    
    
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
        
    for bullet in lists.BULLETs:
        
        bullet.update()
        

    
    pass


#----------------------------------------------------------------------
def drawUI():
    """basic ui info, name health kills xp"""
    
    #first text box
    plrHP = lists.ANYTHINGs[0].components['shooter'].curHP
    plrKls = lists.ANYTHINGs[0].components['shooter'].kills
    text1 = 'Heath: {hp}\nKills: {kills}'.format(hp = plrHP, kills = plrKls)
    
    popupbox1 = dialogs.popUp(str(text1), background=(12, 214, 0))
    screen.blit(popupbox1, (0, 0))
    
    #second text bos
    text2 = 'will be a target\'s name'
    
    popupbox2 = dialogs.popUp(str(text2), background=(12, 214, 0))
    screen.blit(popupbox2, (popupbox1.get_rect().w, 0))
    
    
#----------------------------------------------------------------------
def angleDrawer():
    """draws lines that represent angle between mouse and player dir"""
    
    plr = lists.ANYTHINGs[0]

    #player pos
    pos = plr.pos()
    
    #direction 25 spaces away 
    dir = toolsV2.vectors.scale(plr.direction, 250)
    dir = toolsV2.vectors.add(dir, pos)
    
    #mouse pos
    mPos = PG.mouse.get_pos()
    
    for lines in ((pos, dir), (pos, mPos)):
        PG.draw.line(screen, constants.BLUE, lines[0], lines[1], 2)
    
#----------------------------------------------------------------------
def drawItems(functions):
    """calls all functions in list"""
    
    for func in functions:
        eval('{}()'.format(func))

#----------------------------------------------------------------------
def drawing():
    """draws objects to screen"""
    
    try:
        try:
            #paint background
            screen.blit(background_surface, (0, 0))
            
            drawUI()
            
            drawItems(lists.FUNCs)
            
        except IOError:
            print 'IO ERROR'
        
        
        
        #draw anythings
        for thing in lists.ANYTHINGs:
            thing.draw(screen)
       
        #draw lines to represent angles, if lines is true
        lines = 1
        if lines:
                
            addDir = toolsV2.vectors.linkScaleVector(lists.ANYTHINGs[0].pos(),
                                                   lists.ANYTHINGs[0].direction,
                                                   100)
            points = [lists.ANYTHINGs[0].pos(), PG.mouse.get_pos(), addDir]
            PG.draw.lines(screen, constants.BLACK, True, points, 1)
            
            
            #draw line to represent players direction
            adjDir = toolsV2.vectors.scale(lists.ANYTHINGs[0].direction, 25)
            adjDir = toolsV2.vectors.add(lists.ANYTHINGs[0].pos(), adjDir)
            PG.draw.line(screen, constants.GREEN,
                         lists.ANYTHINGs[0].pos(), addDir)
        
        #-----        
        for bullet in lists.BULLETs:
            bullet.move()
            bullet.draw(screen)            

        ##drawing grid where player is
        #try:
           
            ##pos_list = []
        
            ##pos_tiles = []
            #for tile in lists.all_tiles:
                #for thing in lists.ANYTHINGs:
                    #pos = thing.pos()
                
                    #if tile.range_x[0] <= pos[0] <= tile.range_x[1]:
                        #if tile.range_y[0] <= pos[1] <= tile.range_y[1]:
                            ##pos_tiles.append(tile)
                            ##screen.blit(tile.draw(), tile.rect.topleft)
                            #pass                
            ##print len(pos_tiles)        
        
        #except Exception as e:
            #print e
            #pass
        
        #flip display to monitor
        PG.display.flip()          
        
    except PG.error, message:
        print '\nGame Exited:'
        print message, '\n'
        
    #except UnboundLocalError:
        
        #screen.bllit(lists.flames[1], (100, 100))
        #flameNum = 0
        
    
    pass


##----------------------------------------------------------------------
#def drawFlames(surface):
    #"""draw the flames that switch frames 3 times per second"""
    ##draw the flames that switch frames 3 times per second
    
    #flame = lists.flames[constants.flameNum]
    #if constants.frameNum % 15 == 0:
        
        
        #if constants.flameNum >= len(lists.flames) - 1:
            #constants.flameNum = 0
        
        #else:
            #constants.flameNum += 1
        
        
        
        #pass

    ##blit to surface
    #surface.blit(flame, (100, 100))    

#----------------------------------------------------------------------
def mainloop():
    """main game loop"""


    global  oldFrames
        
    #create a timer for FPS
    fpsTimer = PG.time.Clock()
    
    #init of fps counter
    #t = 0.0
    dt = 1 / float(constants.FRAMERATE) 
    currentTime = float(PG.time.get_ticks()) 
    
    oldFrames = time.clock()
    
    #frame counter
    constants.frameNum = 0
    
    print 'starting main loop'
    
    global gameRunning, delta
    gameRunning = True
    while gameRunning:
        
        #fps
        newTime = float(PG.time.get_ticks()) 
        frameTime = float(newTime) - float(currentTime)
        currentTime = newTime
        
        
        #if quit event in in queue, quit
        if PG.event.peek(PG.QUIT):
            gameRunning = False
            break
        
        #handle input
        controls.inputHandler(screen)

        #while frameTime > 0.0:
            ##print frameTime    
            #deltaTime = min(frameTime, dt)   
            ##run logic
            #gameLogic()
            ##frameTime -= deltaTime
            ##t += deltaTime
            
        #draw to screen
        drawing()
    
        
        
        
    
        ##limit framerate and find the delta time
        diff = fpsTimer.tick(constants.FRAMERATE)
        #print delta, constants.FRAMERATE
        #constants.frameNum += 1

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
