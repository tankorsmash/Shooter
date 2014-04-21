"""module to handle AI"""

import logic,  stats,  tools,  visuals

import math,  pygame

class ai:
    def __init__(self, int=stats.DUMB):
        '''judges when to fire and when to move'''
        
        #how smart the AI is out of 3: DUMB, AVG, SMART
        self.int = int
        
        self.wantToMove = False
        
        #self.target = [circle]
        
        logic.ALLTHINGS.add(self)
        logic.AIs.append(self)
        
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
        # was originally this but changed to hardcode player
        #eP = self.owner.shooter.target.getPos()  
        eP = self.owner.shooter.target[0].getPos()
        #V in wolfire
        v = tools.V.subtract(sP,eP)
        
        Dd = tools.V.norm(D)
        Vd = tools.V.norm(v)
        
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
        theta = tools.V.radToDeg(theta)
        
        
        #so if Theta is < 1/2vision, can see.
        if theta <= self.owner.visionRadius/2 and tools.V.distance(sP, eP) < 200:
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
        
        dist = tools.V.distance(pos,self.owner.shooter.target[0].getPos())
        
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
        
        pygame.draw.line(visuals.screen, visuals.BLUE, pos, leftLine,2)
        pygame.draw.line(visuals.screen, visuals.BLUE, pos, rightLine, 2)
        
        #else:
            #pass  
         
    def check(self):  
        #every second of gametime:
        # move or shoot
        if stats.frame_count % stats.FRAMERATE == 0:
            #if target is in view  stop and fire:
            # else move for 1/2s then rotate for 1/2s
            if self.canSee(self.owner.shooter.target):
                self.wantToMove = False
                self.owner.shooter.fire(self.owner.direction,'bullet')
                  
            elif not self.canSee(self.owner.shooter.target):  
                self.wantToMove = True
        #remainder of eq means less than half a second has passed since last 1s
        elif stats.frame_count % stats.FRAMERATE < stats.FRAMERATE/2 and self.wantToMove:
            self.owner.moving = True
            
        elif stats.frame_count % stats.FRAMERATE >= stats.FRAMERATE/2 and self.wantToMove \
             and not self.canSee(self.owner.shooter.target):
            #stop moving in order to rotate
            self.owner.moving = False

            #figure out the new direction vector to face in
            dir = self.owner.rotateVector(self.owner.direction, 15)
            
            #set it
            self.owner.direction = tools.V.norm(dir)
            self.drawVision()
            #if self can't see target, rotate, else draw a cone
            if not self.canSee(self.owner.shooter.target):
                #print 'can\'t see'
                self.owner.rotate()
            
    def remove(self):
        
            AIs.remove(self)