'''This module is the main logic behind the game'''

import pygame, sys

import tools

import wingdbstub
#wingdbstub.Ensure()

# ------------------------------------#
#other imports are below the constants#
# ------------------------------------#

#-#lists#-#
ALLTHINGS = set()

#all live chars
MEN = []

# ...and their AIs
AIs = []

#all live bullets
BULLETS = []
SHRAPNEL = []

#all dead things
STATS = []

# --------- #

#directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

TLEFT = (-1,-1)
TRIGHT = (1,-1)
BLEFT = (-1,1)
BRIGHT = (1,1)

import stats, time, visuals,  actors,  tools
#kb directions
keyDirs = {
            pygame.K_DOWN : DOWN,
            pygame.K_UP : UP,
            pygame.K_LEFT: LEFT,
            pygame.K_RIGHT: RIGHT,
            
            pygame.K_s : DOWN,
            pygame.K_w : UP,
            pygame.K_a: LEFT,
            pygame.K_d: RIGHT,
            
            pygame.K_KP2: DOWN,
            pygame.K_KP8: UP,
            pygame.K_KP4: LEFT,
            pygame.K_KP6: RIGHT,
            
            pygame.K_KP7: TLEFT,
            pygame.K_KP9: TRIGHT,
            pygame.K_KP1: BLEFT,
            pygame.K_KP3: BRIGHT,
            
            }

def isKey(event, k):
    '''helper function short for event.key == pygame.K-KEY'''
    #getattr wo
    methodToCall = getattr(pygame, 'K_{0}'.format(k))
    if event.key == methodToCall:        return True
        

def key_event(event):
    
    ##WORKING ON THIS: TRY TO MAKE THIS A LIST INSTEAD 
    ## OF ALL THE DIRECTIONS ONE AFTER ANOTHER
    if event.type == pygame.KEYUP:
        #tuple below is directions
        if event.key in keyDirs.keys():
            #for brick in bricks:
                #brick.setMove(moving=False, dir =brick.dir)
            actors.player.go(False)
    elif event.type == pygame.KEYDOWN:
        if event.key in keyDirs.keys():
            

            #print 'keys pressed'
            direction= keyDirs[event.key] 
            actors.player.changeDir(direction)
            actors.player.go(True)


        elif isKey(event, 'n'):
            reload(GUI2)
            print 'reloaded module GUI'
            pass

        elif isKey(event, 'c'):
            actors.player.shooter.fire(actors.player.direction,'bullet')
            print 'FIRED {0} TIMES'.format(actors.player.shooter.timesFired)
            pass 
        
        #clear screen, slopilly.
        elif isKey(event,'RETURN'):
            visuals.screen.fill((0,0,0))

        #elif isKey(event,'z'):
            #print 'circle: ',circle.getPos(), ' bob: ', bob.getPos()
            
        elif isKey(event,'z'):
            if hasattr(GUI2, 'root'):
                print GUI2.root.TEST
            
        #elif isKey(event,'x'):
            #'''check if circle is in bob's rect'''
            #print 'RECTS for circle: ', actors.player.rect.x,\
                                        #actors.player.rect.y,
            #print 'RECTS for bob: ', bob.rect.x,\
                                     #bob.rect.y
             
            #if actors.player.rect.colliderect(bob):
                #print 'COLLISION!!'   
               
        elif isKey(event,'x'):
            print 'player getPos', actors.player.getPos()
                            
                                        
            

        #change animation 
        elif event.key in (pygame.K_0,pygame.K_1,pygame.K_2,
                           pygame.K_3,pygame.K_4,pygame.K_5,
                           pygame.K_6,pygame.K_7,pygame.K_8,
                           pygame.K_9):
            
            keys = {pygame.K_0 :9,
                    pygame.K_1 :0,
                    pygame.K_2 :1,
                    pygame.K_3 :2,
                    pygame.K_4 :3,
                    pygame.K_5 :4,
                    pygame.K_6 :5,
                    pygame.K_7 :6,
                    pygame.K_8 :7,
                    pygame.K_9 :8}
            
            actors.player.curFrameNum = keys[event.key]
            actors.player.curFrame = actors.player.animList[actors.player.curFrameNum].copy()
            actors.player.direction = RIGHT
            actors.player.rotate()
            print 'changed frame'


        elif isKey(event,'m'):
            #func = GUI2.run
            #threading module
            #thread_GUI2 = threading.Thread(group = None, target = func, name='GUI THREAD')
            #thread_GUI2.start()
            
            #no threading
            GUI2.run()
            
            #multiprocessing module
            #thread_GUI2 = multi.Process(target = func, name='GUI THREAD')
            #thread_GUI2.start()
            
            print 'thread ran'
            
        elif isKey(event, 'b'):
            actors.spawner.spawn('mob')
            
        elif isKey(event, 'v'):
            global allGrids
            allGrids = tools.createGrid()
            print allGrids[0].coords, 'is the first grid'
            
        elif isKey(event, 'f'):
            tools.inWhichGrid(actors.player, allGrids)
            stats.lineDraw =  True
            
        elif isKey(event, 't'):
            
            visuals.multiLine('tits though')
            

#----------------------------------------------------------------------
def eventHandler():
    """handles events to the pygame screen"""
    
    #degree =  tools.calcAngle(actors.player.rect.center, pygame.mouse.get_pos())
    #actors.player.doRotate(degree-90)
    #degree =  actors.player.calcAngle(actors.player.getPos(), pygame.mouse.get_pos())
    #actors.player.doRotate(degree)
    
    #print 'degree difference between player and mouse:', degree, 'degrees'
    
    #rotate player's frame in relation to mouse:
    
    
    
    for event in pygame.event.get():
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            print 'Button: {0}, Position: {1}'.format(event.button, event.pos)
            #print 'player direction: {0} and pos: {1}'.format(actors.player.direction, actors.player.getPos())
                       
        if event.type == pygame.QUIT:
            global gameRunning
            gameRunning= 0
            print 'caught close command'
            
            
        elif event.type == pygame.KEYDOWN or event.type== pygame.KEYUP:
            key_event(event)
        
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            print 'event.pos ', event.pos
            #actors.player.pos = event.pos
            #actors.player.go(False)
            
            #mouse and player po
            mpos =  event.pos
            ppos =  actors.player.getPos()
            print '\nmpos {0}, ppos {1}'.format(mpos, ppos)
            
            #sub mpos from ppos
            sub = tools.V.subtract(mpos, ppos)
            print 'sub pos: {0}'.format(sub)
            
            #normalize sub
            norm =  tools.V.norm(sub)
            print 'norm pos: {0}'.format(norm)
            
            #calculate the angle
            angle =  tools.calcAngle(ppos, mpos)
            print 'angle between ppos and mpos: {0}'.format(angle)
            
            #player direction = norm
            actors.player.direction =  norm
            actors.player.rotate()
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            bob.x, bob.y = event.pos
            
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print event.button
            print 'mouse pressed'
            
            if stats.mousePressed: actors.player.go(False)
            #take pos as vector:
            mousePos = (x,y) = event.pos            
            circlePos = actors.player.getPos()
            #print mousePos, circlePos
                        
            #in relation to circle, directions the vector away from them.
            
            #subtract current selfx from x and same for selfy and y
            direction=  tuple([a - b for a, b in zip(mousePos, circlePos)])
            print direction,  'is direction'
            home = [a /200 for a in direction]
            print 'home', home
            
            #normalize home
            normed = tools.V.norm(home)
            #print 'normalized', normed
            #new direction is normed
            
            actors.player.changeDir(normed)
            actors.player.go(True)
            stats.mousePressed = True
            
            #draw a line from player.pos to mouse.pos
            
            pygame.draw.rect(visuals.screen, visuals.BLACK, actors.player.rect)
            
            pygame.draw.line(visuals.screen, visuals.BLACK,
                             actors.player.rect.center, mousePos)
 
 
#----------------------------------------------------------------------
def drawCrossScreen():
    """draws a + across the screen"""
    
    pygame.draw.line(visuals.screen, visuals.BLACK,
                     (0, stats.HEIGHT/2),(stats.WIDTH, stats.HEIGHT / 2))
    pygame.draw.line(visuals.screen, visuals.BLACK,
                     (stats.WIDTH/2, 0),(stats.WIDTH/2, stats.HEIGHT))
    
 
#----------------------------------------------------------------------
def textDisplays():
    """displays text in specialzed boxes"""
    
    text = visuals.multiLine('Player\'s pos: {0}, Mouse pos: {1}'.format(actors.player.getPos(), pygame.mouse.get_pos())) 
    #TextBox('Player\'s pos: {0}, Mouse pos: {1}'.format(actors.player.getPos(), pygame.mouse.get_pos()))
    pass

########################################################################
class TextBox():
    """a class for text boxes """

    #----------------------------------------------------------------------
    def __init__(self, text):
        """Constructor"""
        
        self.w = stats.WIDTH / 2
        self.h = stats.HEIGHT / 8
        
        self.surf = pygame.Surface((self.w , self.h))
        self.rect = self.surf.get_rect().inflate(-3, -3)
        self.surf.set_colorkey((0, 0, 0))
        
        textFont =  visuals.basicFont.render(text, False, visuals.BLUE)
        self.surf.blit(textFont, (0 + 3, 0 + 3))
        
        #self.rect = pygame.Rect(0, 0, self.w, self.h)
        self.corners =  [self.rect.topleft, self.rect.topright,
                         self.rect.bottomright, self.rect.bottomleft,  ]
        pygame.draw.polygon(self.surf, visuals.GREEN, self.corners, 2)
        
        visuals.screen.blit(self.surf, (0, stats.HEIGHT / 8))
        
    
    
    
#----------------------------------------------------------------------
def gameStart():
    """use new or load to get the game going then hit the game loop
       soon after."""
    visuals.start()
    actors.newPlayer()
    #for FPS counting
    timeStart = time.clock()
    clock = pygame.time.Clock()
    
    
    
    
    #__main loop__:
    global gameRunning
    gameRunning = True
    
    print 'player pos before mainloop', actors.player.rect.center
    #print '-----  LOOP START  -----'
    while gameRunning:
        visuals.screen.fill(visuals.WHITE)
        
        #extra lines
        drawCrossScreen()
        if stats.lineDraw:
            tools.inWhichGrid(actors.player, allGrids)
        pygame.draw.line(visuals.screen, visuals.RED,
                                 actors.player.getPos(), (200, 200), 10)        
           
        
        #print 'player direction', actors.player.direction
        
        
        eventHandler()
        
        textDisplays()
        
        #loop over: men, bullets and shrapnel, AIs
        for object in MEN:
            object.shooter.getTarget()
            object.move()
            object.drawFrame()
            #a = object.calcAngle(RIGHT,(0.84996560382278508, -0.52683818418767669))
            #object.doRotate(a)
        for object in BULLETS:
            object.update()
        for object in SHRAPNEL:
            object.update()
        
        for ai in AIs:
            ai.check()           
            
            
        #FPS stuff
        stats.frame_count += 1
        if stats.frame_count % 15 == 0:
            timeEnd = time.clock()
            stats.frame_rate =  15 /  (timeEnd - timeStart)
            timeStart = timeEnd
        text = 'Frame = {0},  rate = {1:.2f} fps'.format(stats.frame_count, stats.frame_rate)
        fps_text = visuals.basicFont.render(text,  True, (0,0,0))    
        visuals.screen.blit(fps_text, (10, 10))
        stats.frame_history.append(text)
            
        
        visuals.pygame.display.flip()
        clock.tick(stats.FRAMERATE)
        sys.stdout.flush()
        
        ##print 'game running'
        ##testing for pos changed
        #print 'end loop:'
        #print '--original:', actors.player.originalXY
        #print '--rect:', actors.player.rect.center
        #print '--current:', actors.player.pos        
        
        
    pygame.quit()
    print 'tried to quit'
            
    
if __name__ == '__main__':
    """Run the following if module is top module"""
    
    
    
    
    #starts pygame
    visuals.start()
    
    #for FPS counting
    timeStart = time.clock()
    clock = pygame.time.Clock()
    
    #main loop:
    gameRunning = True
    while gameRunning:
        
        visuals.screen.fill(visuals.WHITE)
        
        #loop over: men, bullets and shrapnel, AIs
        for object in MEN:
            object.move()
            object.drawFrame()
        for object in BULLETS:
            object.update()
        for object in SHRAPNEL:
            object.update()
            
        #FPS stuff
        stats.frame_count += 1
        if stats.frame_count % 15 == 0:
            timeEnd = time.clock()
            stats.frame_rate =  15 /  (timeEnd - timeStart)
            timeStart = timeEnd
            
        text = 'Frame = {0},  rate = {1:.2f} fps'.format(stats.frame_count,
                                                         stats.frame_rate)
        fps_text = visuals.basicFont.render(text,  True, (0,0,0))    
        visuals.screen.blit(fps_text, (10, 10))
        stats.frame_history.append(text)
            
        eventHandler()
        visuals.pygame.display.flip()
        print 'game running', stats.FRAMERATE
        #print stats.FRAMERATE
        clock.tick(stats.FRAMERATE)
        
        