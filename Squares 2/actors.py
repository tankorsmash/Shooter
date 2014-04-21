'''handles all the actors, which is like players, npc, and projectiles.
Pretty much anything that moves.'''

import stats, logic, tools,  visuals,  ai

import wingdbstub
import glob, os.path,  pygame, math, random

class anything:
    def __init__(self, (x,y),name, animFolder,
                 direction= logic.RIGHT, moving=False,
                 shooter= None, ai = None, isPlayer=False):
        '''supposed to be the thing every class is inherited from
         but hey, here we are'''
        
        #determine if the instance is the player
        self.isPlayer = isPlayer
        
        #create and append appropriate stats for object
        self.initLists()
        
        self.name = name
        
        
        
        self.originalXY =  (x, y)
        
        #testing for pos changed
        self.animList = self.animLister(animFolder)
        self.curFrameNum = 0
        
        #self.rect so center is center of instance. Pos is rect.center
        self.rect =  pygame.Rect((x, y), (self.WIDTH, self.HEIGHT))
        if name == 'Player':
                
            print 'xy before', x, y
            print 'center before', self.rect.center
            self.rect.center = (x, y)
            print 'center after', self.rect.center
            print 'xy after', x, y
            #print '::init rect', self.rect.center
            #print '::init pos', self.pos
        #self.pos =  self.rect.center

        #direction is the direction the frame is facing
        self.direction = tools.V.norm(direction)
        
        #facing is the direction the frame is currently facing
        #self.facing = self.direction
        self.curRotation = 0
        
        #frame info
        self.curFrame = self.animList[self.curFrameNum].copy()
        self.drawable = self.curFrame
        self.oldCenter = self.curFrame.copy().get_rect().center
        
        #movement info
        self.moving = moving
        self.speed = 5
        
        #vision
        self.visionRadius = 90
        self.visionDist = 200
        
        #components
        self.shooter = shooter        
        if self.shooter: 
            self.shooter.owner = self
            self.shooter.getTarget()
        
        self.ai = ai
        if self.ai: self.ai.owner = self
        
        #self.stats = Stats(self)
        #owner is passed in to construct
        #self.stats.owner = self
        
        #print self.rect.size, 'init size'
        
        #determine if the instance is the player
        ##if isPlayer:
            ##self.isPlayer =  True
        ##else:
            ##self.isPlayer = False
        
        #testing for pos changed
        if name == 'Player':                
            print '  END', self.name
            print 'ini orig', self.originalXY
            print 'ini pos', self.getPos()
            print 'ini ctr', self.rect.center
            
    def die(self):
        '''remove from alive lists and record frame died on'''
        logic.MEN.remove(self)
        if self.ai:
            self.ai.remove()
        
        print self.name, ' died... RIP'
        
        self.rect = pygame.rect.Rect(0, 0, 0, 0)
        
    def __repr__(self):
        if self.name:
            
            return self.name
        else:
            return self
     
    def initLists(self):
        ''' lists and stats of everything relevant to this instance'''
        ##considering making a stats class to append here though, might make
        ###life a bit easier
        logic.ALLTHINGS.add(self)
        logic.MEN.append(self)
        
        self.timesHit = 0
        
        
    def gotHit(self,damage):
        '''Stuff that happens upon getting hit'''
        #record the hit
        self.timesHit += 1
        
        #take damage
        self.shooter.takeDamage(damage)
        
        
        
        #try :
            #self.curFrameNum +=1
            #self.curFrame = self.animList[self.curFrameNum].copy()
            #self.doRotate(self.curRotation)
        #except IndexError:
            #self.curFrameNum = 0
            #self.curFrame = self.animList[self.curFrameNum].copy()
            #self.doRotate(self.curRotation)
            
    def check(self):
        '''Check to see if level up or dead'''
        if self.shooter.curHp <= 0:
            self.die()
        
        
    def scaleImage(self,imagepath):
        #loads image, scales it, returns scaledimage.
        image = pygame.image.load(imagepath).convert()
        image.set_colorkey(visuals.WHITE)
        
        scaled = pygame.transform.scale(image, (32,32))
        scaledRect =  scaled.get_rect()
        self.WIDTH =  scaledRect.w
        self.HEIGHT =  scaledRect.h
        
        scaled.set_at((0, 0), visuals.GREEN)
        
        #imagename = imagepath.split('/')[-1]
        #print '{0}\'s scaled width: {1}'.format(imagename,scaled.get_width()) 
        return scaled
        
    def animLister(self,folder):
        '''must have png named 1 thru 100
        and this func will go through them in that
        order and add them to a list to animate'''
        
        
        #func to list all jpgs in folder 
        #then count em all for len later
        animationList = []
        for filepath in glob.glob(folder+r'\*.png'):
            #print filepath
            frame  = self.scaleImage(filepath)
            animationList.append(frame)
             
        return animationList
    
    def drawFrame(self):
        
        #changed from curFrame to drawable 
        #and save the rect on 'screen'
        visuals.screen.blit(self.drawable, (self.rect.topleft))

        
    def changeDir(self,direction, moving = True):
        # - check pos
        # - rotate part of the way
        # - go
        
        #trying to do it with vectors, if dot is positive its a right turn
        # if negative, it's a left turn.
        direction = tools.V.norm(direction)
        #print 'new direction: ', direction
        self.direction = direction
        self.move()
        #self.drawFrame()
        
    def go(self,move):
        self.moving = move
        
    def move(self):
        x, y = self.getPos()
        #x, y = self.pos
        if self.moving:

            self.rotate()
            #if x or y is out of boundaries do nothing
            if x + self.direction[0] * self.speed >     \
                        stats.WIDTH - self.rect.w or \
               y + self.direction[1] * self.speed >     \
                        stats.HEIGHT - self.rect.h or\
               x + self.direction[0] * self.speed < 0 or\
               y + self.direction[1] * self.speed < 0  :
                
                pass
                #print 'not inside screen'
                
            #else do move
            else:
                x = self.direction[0] * self.speed
                y = self.direction[1] * self.speed
                
                #print 'x', self.x, '<', WIDTH
                #print 'y', self.y, '<', HEIGHT
                
                #move self.rect's x and y to this
                self.rect =  self.rect.move(x, y)
                
    def rotateVector(self,vector,angle):
        #45 degrees = pi/4 radians
        x,y = vector
        rad = tools.V.degToRad(angle)
        xNew = round((math.cos(rad) * x + math.sin(rad) * y),2)
        yNew = round((math.sin(rad) * x - math.cos(rad) * y),2)
        new_vector = xNew,yNew
        #print 'Old vector: ', vector
        #print 'Rotated Vec:', new_vector
        
        return new_vector

    def scale(self,vector, distance):
        '''move vector to distance away'''
        x,y = vector 
        x *= distance
        y *= distance
        #print 'Scaled Vec: ', (x,y)
        return (x,y)

            
    def roundTo(self,x,rounder):
        x = x/rounder
        x = round(x) 
        x = x*rounder
        #print(x) 
        return x 
    
    def rotate(self):  
        '''rotates facing to match direction'''
        
        frame = self.curFrame
        self.oldCenter = frame.get_rect().center
        
        #find the angle between default (RIGHT) and current direction
        angle = tools.calcAngle(self.direction, logic.RIGHT)
        
        #round the angle to integer if float
        angle = int(round(angle,0))
        #print 'current angle for {0}: '.format(self.name), angle

        #make sure it's not over 360, in order to avoid extra rotation.
        self.curRotation = angle 
        while self.curRotation > 359:
            self.curRotation -= 360
            #print self.curRotation
            
        #drawing will be rounded
        self.curRotation= self.roundTo(self.curRotation,2)

       
        #self.drawable = pygame.transform.rotate(frame, self.curRotation)
        self.doRotate(self.curRotation)
        #self.drawable.get_rect().center = oldCenter
        #print f, d
        #self.facing = self.direction


    def doRotate(self,angle):
        self.drawable = pygame.transform.rotate(self.curFrame, angle)
        #self.drawable.get_rect().center = self.oldCenter
        #print self.facing, self.direction
        #self.facing = self.direction
        
    def calcAngle(self,p1, p2):
        '''return in angle in deg'''
        a1 = math.atan2(p1[1], p1[0])
        a2 = math.atan2(p2[1], p2[0])
        angle = (a1 - a2) % (2 * math.pi)
        return tools.V.radToDeg(angle)
    
        
    
    
    def getPos(self):
        pos = self.rect.center
        
        #print "pos = ", pos
        return pos
    
    
    
class shooter:
    def __init__(self, level, maxHp):
        '''handles damage and exp level'''
        
        self.level = level
        self.maxHp = maxHp
        self.curHp = maxHp
        
        
        self.initLists()
        
        
    def takeDamage(self, damage):
        ''' sub damage from curHP'''
        self.curHp -= damage
        
    #----------------------------------------------------------------------    
    def initLists(self,):
        ''' init all the lists and stuff relevant'''
        
        self.timesFired = 0
        
    #----------------------------------------------------------------------    
    def getTarget(self,):
        '''figure out who the target is'''
        #print self.owner, 'is player?', self.owner.isPlayer
        #print logic.MEN,  '<-- logic.MEN'
        if self.owner.isPlayer:
            
            self.target = [thing for thing in logic.MEN]
            self.target.remove(self.owner)
        else: self.target = [thing for thing in logic.MEN if thing.name == 'Player']
        
        
        
        
        
    #----------------------------------------------------------------------
    #def __repr__(self):
        #if self.owner.name:
            
            #return self.owner.name, '\'s shooter componet'
        #else:
            #return self
            
     #----------------------------------------------------------------------       
    def  fire(self, direction, variety):
        #spawn and fire projectile in direction
        bull= projectile(self.owner,self.owner.direction, self.owner.shooter.target, 'bullet')
        if not type(self.timesFired ) is int:
            self.timesFired = int(self.timesFired)
        self.timesFired += 1
        #print len(BULLETS)
        

class projectile():
    def __init__(self, source, direction, target, variety):
        '''is any projectile fired'''
        logic.ALLTHINGS.add(self)
        
        #source of proj. likely who shot self
        self.source = source
        #rect of 
        self.curFrame = source.curFrame
        
        self.direction = direction
        
        #target is a list
        self.target = target
        
        #whether or not the projectile is alive
        self.active = True
        
        #assing to proper group
        self.variety = variety
        
        if self.variety == 'bullet':
            self.speed = 10
            self.groupList = logic.BULLETS
            self.colors = [visuals.RED, visuals.BLACK]
            
        elif self.variety == 'shrapnel':
            self.speed = 3
            self.groupList = logic.SHRAPNEL
            self.colors = [visuals.BLUE, visuals.GREEN]
        self.groupList.append(self)
        
        self.color = visuals.BLACK
        
        #get rect of curFrame's center x y
        #self.x,self.y = self.source.getPos()
        
        self.height= 4
        
        #actually fire the projective
        self.fire()
        
 
        #name it based on number of game objects
        self.name()
        
        #init lists
        self.initLists()
        
    def update(self):
        #update color and height
        self.changeColor()
        self.changeSize()
        
        #move and draw
        self.move()
        self.draw()
        
        #make sure targets in self.target is still alive
        #
        # if MEN has changed from the original copy
        if self.oldMEN != logic.MEN:
            print 'MEN is not the same'
            #go through and find the MEN that aren't there
            for object in self.oldMEN:
                print object.name, 'might get removed'
                #and remove them from target
                if object not in logic.MEN:
                    self.target.remove(object)
                
    def changeColor(self):
        #print self.travelled
        if self.travelled % 2 == 0:
            self.color = self.colors[0]
        else : self.color = self.colors[1]
        
    def changeSize(self):
        if self.travelled % 3 == 0:
            self.height *= 2
            
        elif self.travelled % 10 == 0:
            #self.height *= 3
            
            #see Cross product from wolfire blog, reversing x and y
            # with x being made negative and y negative for right turn
            left = -self.direction[1], self.direction[0]
            right = self.direction[1], -self.direction[0]
            

            
            
            #draw them
            projectile(self,left,[player],'shrapnel')
            projectile(self,right,[player],'shrapnel')
            #print 'broke up'
            
            
        else: self.height = 4
    def initLists(self):
        self.travelled = 0
        
        self.oldMEN = logic.MEN
    def name(self):
        self.name = '{0} No. {1}'.format(self.variety,len(logic.ALLTHINGS))
        
    def fire(self):
        #get rect of curFrame's center x 
        if self.variety == 'bullet':
            self.x,self.y = self.curFrame.get_rect().center
            
            #spawn at first position out from source
            # add the center of the rect to the center of 
            # shooter then move bit a bit
            self.x = self.x + self.source.getPos()[0] + \
                (self.direction[0] * self.curFrame.get_rect().width)
            self.y = self.y + self.source.getPos()[1] + \
                (self.direction[1] * self.curFrame.get_rect().height)
        elif self.variety == 'shrapnel':
            self.x,self.y = self.source.getPos()
            #spawn at first position out from source
            # add the center of the rect to the center of 
            # shooter then move bit a bit
            self.x = self.x + self.direction[0] 
            self.y = self.y + self.direction[1] 
        self.draw()
        
    def move(self):
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        #print 'bullet moving'
        #if self still in play
        if self.active:
            self.travelled +=1
            
            #or if hit another
            # test all rects
            hit_something = False
            
            
            #for t in self.target:
                #if self.size.collidelist(self.target):
                    #hit_something = t
                    #break
            #print self.target[0].rect.size
            hit_something = self.size.collidelist(self.target)
            #print self.target[hit_something]
                
                
            #remove self if off screen
            if self.x > stats.WIDTH + 1 or self.y > stats.HEIGHT \
               or 0 > self.x or 0 > self.y:
                self.remove()
                #print 'removed: ', self.name
                
     
            elif hit_something != -1:
                print 'BULLET HIT!'
                self.target[hit_something].gotHit(5)
                #print self.target, 'is the target list for', self.source
                print self.source, 'is the source'
                self.remove()
                
            #add 1 movement to count. change color accordingly
            
            elif self.variety == 'shrapnel':
                
                if self.travelled > 3:
                    if self in logic.SHRAPNEL:
                        self.remove()
                    else : print 'shrapnel not in SHRAPNEL'
    def checkSize(self,):
        self.size = pygame.rect.Rect(self.x - (self.height /2),
                                     self.y - (self.height /2),
                                     self.height, 
                                     self.height)
        #self.size.center = self.source.curFrame.get_rect().center
        #self.size.center = self.size.center + (self.x,self.y)
        
    def getPos(self):
        self.pos = (self.x,self.y)
        #print "pos = ", self.pos
        return self.pos
    def draw(self):   
        self.checkSize()
        ##draw a rect
        #pygame.draw.rect(screen, self.color ,
                         #self.size)
                         
        ##draw a circle
        pygame.draw.circle(visuals.screen, self.color ,
                         (self.size.x,self.size.y), 2)
    
    def hit(self):
        '''remove self from active list -> dead list'''
        #do damage to target,
        #animate
        self.remove()
        
    def remove(self):
        '''remove from pertinent lists and add to stats'''
        print 'Gah, I\'m done!, signed, ', self.name, self.variety, 'I hit', self.target
        logic.STATS.append(self)
        if self.variety == 'bullet':
            logic.BULLETS.remove(self)
        elif self.variety == 'shrapnel':
            logic.SHRAPNEL.remove(self)
            
        #kill the self in class
        self.active = False
        
        
        
class Spawner():
    '''used to spawn entities'''
    def __init__(self, *args):
        pass
    
    def spawn(self, subject, *args):
        '''spawn an entity '''
        if subject == 'mob':
            print 'mob made'
            shot = shooter(1, 20)
            AI = ai.ai(stats.DUMB)
            
            W = stats.WIDTH * random.random()
            H = stats.HEIGHT * random.random()
            
            pathname = os.path.abspath(os.path.curdir)
            pathname += '/art/man/'
            
            mob = anything((W, H),'Bob',pathname, shooter=shot, ai= AI)
            mob.shooter.getTarget()
            return mob
        
        else :
            print 'spawn nothing'
            

#----------------------------------------------------------------------
def newPlayer():
    """creates a player from scratch"""
    
    x =  (stats.WIDTH / 2)
    y =  (stats.HEIGHT / 2)
    s =  shooter(0, 100)
    s2 =  shooter(0, 99999)
    pathname = os.path.abspath(os.path.curdir)
    pathname += '/art/man/'    
    #create player
    global player
    player =  anything((x, y), "Player",
                       pathname, logic.RIGHT, False, s, None, True)
    defTarget =  anything((x - 100, y + 10), "Default Target Instance",
                          pathname, logic.RIGHT, False, s2, None)
    #put player is actors namespace
    global player
    #logic.MEN.append(player)
    #logic.MEN.append(defTarget)
    
    print 'made player and defTarget'
    
spawner = Spawner()