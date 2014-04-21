print 'OLD DEAR GOD WHY'

import pygame as pygame
#from pygame.locals import *
import random
import os.path
import glob
import math
import time
import Tkinter as tk
#import statsWin
import GUI
import tools
import multiprocessing as multi

#constants
WIDTH = 800
HEIGHT = 600
   
FRAMERATE = 30

#directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

TLEFT = (-1,-1)
TRIGHT = (1,-1)
BLEFT = (-1,1)
BRIGHT = (1,1)

DIRECTIONS = [UP,DOWN,LEFT,RIGHT,TLEFT,TRIGHT,BLEFT,BRIGHT]

STOP = (0,0)



#keyboard directions and their equivalents
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


#rotations
leftTurns= {
            UP:LEFT,
            LEFT:DOWN,
            DOWN:RIGHT,
            RIGHT:UP}


rightTurns = {
            UP:RIGHT,
            RIGHT:DOWN,
            DOWN:LEFT,
            LEFT:UP}


acrossTurns = {UP:DOWN,
               DOWN:UP,
               LEFT:RIGHT,
               RIGHT:LEFT}

#ai levels
DUMB = 0
AVG = 1
SMART = 2

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

mousePressed = False

def isKey(event, k):
    '''short for event.key == pygame.K-KEY'''
    #getattr wo
    methodToCall = getattr(pygame, 'K_{0}'.format(k))
    if event.key == methodToCall:        return True
        
    



#set game icon

class Spawner():
    '''used to spawn entities'''
    def __init__(self, *args):
        pass
    
    def spawn(self, subject, *args):
        '''spawn an entity '''
        if subject == 'mob':
            print 'mob made'
            shot = shooter(1, 100)
            AI = ai(DUMB)
            
            W = WIDTH * random.random()
            H = HEIGHT * random.random()
            mob = anything((W, H),'Bob',pathname, shooter=shot, ai= AI)
            mob.shooter.getTarget()
            return mob
        
        else :
            print 'spawn nothing'

class Stats():
    '''A class for managing statistics and information 
    about any given instance, acting asadvanced dictionary use'''
    
    def __init__(self, owner):
        '''init it all'''
        self.owner = owner
        #get the stats
        self.getBasicStats()
        self.getShooterStats()
        
    def getBasicStats(self):
        '''gets all the basic stats for a creature such as name 
        and position upon creation'''
   
        self.basicStats = {
    
            'Name': self.owner.name, 
            'Pos': self.owner.pos,
                            }  
              
    def getShooterStats(self):
        '''get the stats from the shooter component'''
        
        if self.owner.shooter:
            print self.owner.name, 'is a shooter'
            self.shooterStats = {
               'Times Fired': self.owner.shooter.timesFired,
               'Times Hit': self.owner.timesHit,
                               }
        else:
            print self.owner.name, 'isn\'t a shooter'
        
    def getAiStats(self):
        '''gets the stats from the AI component'''
        
        if self.owner.ai:
            print self.owner.name, 'is an AI'
            self.aiStats  = {
                '': '',}
            
        else:
            print self.owner.name, 'isn\'t an AI'


#handle keys
def key_event(event):
    
    ##WORKING ON THIS: TRY TO MAKE THIS A LIST INSTEAD 
    ## OF ALL THE DIRECTIONS ONE AFTER ANOTHER
    if event.type == pygame.KEYUP:
        #tuple below is directions
        if event.key in keyDirs.keys():
            #for brick in bricks:
                #brick.setMove(moving=False, dir =brick.dir)
            circle.go(False)
    elif event.type == pygame.KEYDOWN:
        if event.key in keyDirs.keys():
            

            #print 'keys pressed'
            direction= keyDirs[event.key] 
            circle.changeDir(direction)
            circle.go(True)


        elif isKey(event, 'n'):
            reload(GUI2)
            print 'reloaded module GUI'
            pass

        elif isKey(event, 'c'):
            circle.shooter.fire(circle.direction,'bullet')
            print 'FIRED {0} TIMES'.format(circle.shooter.timesFired)
            pass 
        
        #clear screen, slopilly.
        elif isKey(event,'RETURN'):
            screen.fill((0,0,0))

        #elif isKey(event,'z'):
            #print 'circle: ',circle.getPos(), ' bob: ', bob.getPos()
            
        elif isKey(event,'z'):
            if hasattr(GUI2, 'root'):
                print GUI2.root.TEST
            
        elif isKey(event,'x'):
            '''check if circle is in bob's rect'''
            print 'RECTS for circle: ', circle.rect.x,\
                                        circle.rect.y,
            print 'RECTS for bob: ', bob.rect.x,\
                                     bob.rect.y
             
            if circle.rect.colliderect(bob):
                print 'COLLISION!!'   
                                        
                            
                                        
            

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
            
            circle.curFrameNum = keys[event.key]
            circle.curFrame = circle.animList[circle.curFrameNum].copy()
            circle.direction = RIGHT
            circle.rotate()
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
            spawner.spawn('mob')
            
            
        



        
class ai:
    def __init__(self, int=DUMB):
        '''judges when to fire and when to move'''
        
        #how smart the AI is out of 3: DUMB, AVG, SMART
        self.int = int
        
        self.wantToMove = False
        
        self.target = circle
        
        ALLTHINGS.add(self)
        AIs.append(self)
        
    def __repr__(self):
        if self.name:
            return self.name
        
        else:
            return self
        
    def canSee(self,target):
        #selfPos:
        sP = self.owner.getPos()
        #D in wolfire
        D = self.owner.direction
        #enemyPos
        eP = self.target.getPos()  
        #V in wolfire
        v = V.subtract(sP,eP)
        
        Dd = V.norm(D)
        Vd = V.norm(v)
        
        #angle between Dd and Vd
        
        #first and seconds values of each multi'd
        ZERO = Dd[0]*Vd[0]
        ONE = Dd[1]*Vd[1]
        #then summed
        SUM = ZERO + ONE
        if 2 > SUM < 1.0 :
            SUM = 1.0
            
        #passed to acosine
        theta = math.acos(SUM)
        theta = V.radToDeg(theta)
        
        
        #so if Theta is < 1/2vision, can see.
        if theta <= self.owner.visionRadius/2 and V.distance(sP, eP) < 200:
            #print 'can see!'
            return True
        
        else :
            #print 'can\'t see'
            return False
        
        
    def drawVision(self):
        '''draw two lines on edges of vision'''
        #print 'woulda drawVision'
        #print self.owner.direction
        
        #take pos and center added together for center pos on screen
        pos = self.owner.getPos()
        pos2 = self.owner.curFrame.get_rect().center
        pos = tuple([a+b for a,b in zip(pos,pos2)])
        
        dist = V.distance(pos,self.target.getPos())
        
        #if dist is further then visionDist, set dist to 
        # that so the line doesn't keep drawing forever, 
        # in order to better define each persons vision.
        if dist > self.owner.visionDist:
                
            dist = self.owner.visionDist
        
        #angle of left half of vision
        leftLine = self.owner.rotateVector(self.owner.direction,
                                           -self.owner.visionRadius/2)
        #take the vector and scale it 50x
        leftLine = self.owner.scale(leftLine,dist)
        
        rightLine = self.owner.rotateVector(self.owner.direction,
                                           self.owner.visionRadius/2)
        rightLine = self.owner.scale(rightLine,dist)

        
        #add pos to leftLine and rightLine so that vectors will be
        # relevant rather than < 1.
        leftLine= tuple([a+b for a,b in zip(leftLine,pos)])
        rightLine= tuple([a+b for a,b in zip(rightLine,pos)])
        
        pygame.draw.line(screen, BLUE, pos, leftLine,2)
        pygame.draw.line(screen, BLUE, pos, rightLine, 2)
        
        #else:
            #pass  
         
    def check(self):  
        #every second of gametime:
        # move or shoot
        if frame_count % FRAMERATE == 0:
            #if target is in view  stop and fire:
            # else move for 1/2s then rotate for 1/2s
            if self.canSee(self.target):
                self.wantToMove = False
                self.owner.shooter.fire(self.owner.direction,'bullet')
                  
            elif not self.canSee(self.target):  
                self.wantToMove = True
        #remainder of eq means less than half a second has passed since last 1s
        elif frame_count % FRAMERATE < FRAMERATE/2 and self.wantToMove:
            self.owner.moving = True
            
        elif frame_count % FRAMERATE >= FRAMERATE/2 and self.wantToMove \
             and not self.canSee(self.target):
            #stop moving in order to rotate
            self.owner.moving = False

            #figure out the new direction vector to face in
            dir = self.owner.rotateVector(self.owner.direction, 15)
            
            #set it
            self.owner.direction = V.norm(dir)
            self.drawVision()
            #if self can't see target, rotate, else draw a cone
            if not self.canSee(self.target):
                #print 'can\'t see'
                self.owner.rotate()
            
    def remove(self):
        
            AIs.remove(self)
        
    
    
        
        

        
         
#class basicEnemy():
    #def __init__(self, intLvl=1):
        #self.intLvl = intLvl


        

#def gameInit():

if __name__ == '__main__':
    
    # ########INIT######### #
    pygame.init()
    pygame.display.set_caption('Line Moving App')
    #seticon('bricks.ico')    
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    #screen.fill(BLUE)
    screen.set_colorkey((255,255,254))
    
    #background = pygame.Surface(screen.get_size())
    #background = background.convert()
    #background.fill(WHITE)
    
    clock = pygame.time.Clock()
    
    pygame.display.flip()
    
    basicFont = pygame.font.SysFont(None, 48)   
    
    V = tools.Vector()
    
    spawner = Spawner()
    
    # ############### #
    
    
        
    pathname = os.path.abspath(os.path.curdir)
    pathname += '/art/man/'
    #print pathname
    shot = shooter(1,100)
    circle = anything((400,200),'Josh', pathname,shooter=shot)
    circle.shooter.getTarget()

    circle.shooter.getTarget()
    #bob.shooter.getTarget()
    
    # window for stats
    '''reference new module for stats here'''
    #window = statsWin.start()
    
    running = 1      
    
    frame_count = 0
    frame_rate = 0
    t0 = time.clock()
    while running:
        #window()
        
        screen.fill(WHITE)
        #bob.ai.drawVision()
        #check for movements, and draw after
        for object in MEN:
            object.move()
            #object.check()
            
            #print object.name, 'is drawn', frame_count
            object.drawFrame()
             
        
            
        for object in BULLETS:
            object.update()
            
        for object in SHRAPNEL:
            object.update()
            
        #AIs think
        for object in AIs:
            object.check()
            object.drawVision()
        frame_count += 1
        if frame_count % 15 == 0:
            t1 = time.clock()
            frame_rate = 15 / (t1-t0)
            t0 = t1
       
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = 0
                
            elif event.type == pygame.KEYDOWN or event.type== pygame.KEYUP:
                key_event(event)
            
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                #print event.button
                (circle.x,circle.y) = event.pos
                circle.go(False)
                
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                bob.x, bob.y = event.pos
                
                
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                print event.button
                print 'mouse pressed'
                if mousePressed: circle.go(False)
                #take pos as vector:
                mousePos = (x,y) = event.pos            
                circlePos = (circle.x,circle.y)
                print mousePos, circlePos
                
                #in relation to circle, directions the vector away from them.
                
                #subtract current selfx from x and same for selfy and y
                direction=  tuple([a - b for a, b in zip(mousePos, circlePos)])
                print direction
                home = [a /200 for a in direction]
                print home
                
                #normalize home
                normed = V.norm(home)
                
                #new direction is normed
                
                circle.changeDir(normed)
                circle.go(True)
                mousePressed = True
                
                
                            
                    
                    
        
        the_text = basicFont.render('Frame = {0},  rate = {1:.2f} fps'
                          .format(frame_count, frame_rate), True, (0,0,0))
        screen.blit(the_text, (10, 10))
        
        for object in MEN:
            object.check()
                
        pygame.display.flip()
    
        
        # #### #
        clock.tick(FRAMERATE)

#if __name__ == '__main__':
    
    #gameInit()