#builtins
import random, pygame

#customs
import lists, constants, toolsV2, loadImages, main


########################################################################
class error(Exception):
    """overrides"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        
        print 'error'
    
    

########################################################################
class Anything(object):
    """General class that contains drawing, movement, position
    will be  """

    #----------------------------------------------------------------------
    def __init__(self, topSurface, position, imageListIn, actType='ship'):
        """Constructor"""
        
        #actor type, gun ship etc
        self.actType = actType
        
        #main spritelist
        self.imageListIn = imageListIn
        self.topSurface = topSurface
        
        #size
        self.width = 32
        self.height = 32
        
        #rect of the size of the image to be
        self.rect = pygame.rect.Rect(0, 0, self.width, self.height)
        #set the rects center to the anythings pos
        self.rect.center = position
        
        #name
        self.name = random.choice(constants.namesAmericanMale)
        
        #movement
        self.speed = constants.unit / 5
        self.direction = toolsV2.vectors.normalize((1, 0))
        self.moving = False
        
        #make a spriteList for drawing
        self.spriteIndex = 0
        self.flamesIndex = 0
        self.assemble2(imageListIn, 1)        

        #loads sprite images, from imageListIn
        


        #degrees sprite is rotated
        self.currentRotation = 0
        
        #vector the sprite is facing
        self.facing = self.direction
        
        #add self to ANYTHING list
        lists.ANYTHINGs.append(self)
        
        ##create blit here for no reason
        #self.blitted = topSurface.blit(self.surface, self.rect)
        
        #a dict to hold all the components
        self.components = {}
        
        #if hit wall
        self.wallHit = False
        
        #bounding boxes, the perimiter of the rects, in a list
        self.bboxsList = self.getBboxes()
        
        #updates gun and exhaust points
        self.findPoints()
   
        #is alive or not
        self.alive = True
        
        #IDK
        self.surface = self.combine()
    #----------------------------------------------------------------------
    def getBboxes(self):
        """finds the 4 lines/rects that represent the outsides of the rect"""
        sr = self.rect
        
        bboxes = []
        
        #top width line
        tw = pygame.rect.Rect((sr.topleft), (sr.w, 1))
        #bottom width
        bw = pygame.rect.Rect((sr.bottomleft), (sr.w, 1))
        #left height
        lh = pygame.rect.Rect((sr.topleft), (1, sr.h))
        #right height
        rh = pygame.rect.Rect((sr.topright), (1, sr.h))
        
        for l in (tw, bw, lh, rh):
            
            bboxes.append(l)
    
        return bboxes
    
    #----------------------------------------------------------------------
    def move(self):
        """moves the center of a rect for position"""
        
        if self.moving:
            #change pos which is actually rect.center
            x, y = self.rect.center
            x += self.direction[0] * self.speed
            y += self.direction[1] * self.speed
            
            #make sure bounds aren't broken
            if  not 0 > x and not x > constants.WIDTH:
                if not 0 > y and not y > constants.HEIGHT:
                    self.rect.center = x, y
                    self.wallHit = False

                else:
                    #print 'y is out'
                    self.moving = False
                    self.wallHit = True
            else:
                #print 'x is out'
                self.moving = False
                self.wallHit = True
            
            #if isinstance(self, Bullet):
                #print 'bullet pos', self.pos(), self.rect.center
            
    #----------------------------------------------------------------------
    def pos(self):
        """returns pos, or self.rect.center"""
        
        return self.rect.center
        
            
    #----------------------------------------------------------------------
    def draw(self, surface):
        """draw self.surface to screen, assign blitted surface as blitted"""
        
        
        #blits the image to where rect it, blitted is the rect of where the thing is on screen
        self.blitted = surface.blit(self.surface, self.rect)
        
        box = 0
        if box:
            pass
            pygame.draw.rect(surface, constants.RED,
                             (self.exPt, (5, 5))
                             ,2) 
            pygame.draw.rect(surface, constants.RED,
                             (self.gunPt, (5, 5))
                             ,2) 
            ##draws a rect around the surface
            ##pygame.draw.rect(surface, constants.BLUE, self.rect, 1)
            for rect in self.bboxsList:
                pygame.draw.rect(surface, constants.BLUE, rect, 1)
            
            

        
    #----------------------------------------------------------------------
    def rotate(self, angle):
        """rotates the surface by angle"""
        #print 'angle', angle
        #takes the argument angle and add to it self.angle to maintain proper angles
        angle = self.currentRotation + angle
        
        #forgets old surface and resets it to default right facing one
        #self.surface = self.spriteList[self.spriteIndex]
        self.surface = self.combine()
        #self.surface = self.assAll()

        #since blitted is the rect of surface on screen, takes its center (pos)
        #oldCenter = self.blitted.center
        oldCenter = self.rect.center
        
        
        #rotate the newly reset surface
        self.surface = pygame.transform.rotate(self.surface, angle)
        
        
        #updates currentRotation for next time
        self.currentRotation = angle
        
        #sets self.rect to the new surface
        self.rect = self.surface.get_rect()
        #self.rect = self.bodySurface.get_rect() #for later use this, smaller

        #print 'self.rect.w', self.rect.w
        #updates its pos to match original pos.
        self.rect.center = oldCenter
        
        #since sprite is correctly rotated, update facing direction and facing
        self.facing = self.direction
        
    #----------------------------------------------------------------------
    def update(self):
        """check facing angle and direction angle to see if they match
           or not"""
        
        
        #move
        self.move()
        
        #update bbox
        self.bboxsList = self.getBboxes()
 
        #find angles between pos and facing/pos and direction
        facingAngle = toolsV2.angleBetweenTwoPoints(self.pos(), self.facing)
        directionAngle = toolsV2.angleBetweenTwoPoints(self.pos(), self.direction)
        #print 'angles f and d', facingAngle, directionAngle
        
        #if angles are different
        #if facingAngle != directionAngle:
        difference = facingAngle - directionAngle
        #rotate the surface
        self.rotate(-difference)
        
        #updates gun and exhaust points
        self.findPoints()
        
               
    #----------------------------------------------------------------------
    def assemble2(self, images, index):
        """takes all the images and deals with them, returning the right one"""
        
        self.spriteList = images
        
        #main body surface
        try:
            self.bodySurface = self.spriteList[index]
        except TypeError:
            print 'error, only one surface'
            self.bodySurface = self.spriteList
        
        #etc stuff, flames, turrets etc
        self.etc = {}
        
        if self.actType == 'ship':
            flames = loadImages.loadImages(r'./art/flames/', 'png', (16, 16))
            
            self.etc['flames'] = flames
            
        
        
        
            
    #----------------------------------------------------------------------
    def assemble(self, images):
        """loads the images in two steps:
        - the main sprite images or body
        - the weapons/movement stuff
        - creates the final surface to blit and rotate on main screen"""
        self.spriteList = images
       
        
        self.surface = self.assAll()
        self.surface.set_colorkey(constants.TRANS)
        #self.surface.fill((233, 23, 233))
        
    
    #----------------------------------------------------------------------
    def assBody(self):
        """assembles body of the sprite,
        returns the screen with the body on it"""
        
        
        self.surfaceBody = self.spriteList[self.spriteIndex]
        self.surfaceBody.set_colorkey(constants.TRANS)
        
        
    #----------------------------------------------------------------------
    def assLimbs(self):
        """assembles the jets, weapons, mods on top of
        the body surface"""
        
        #right now it's just flames, but there'll be more later
        
        #load flames and make that the list of surfaces to use
        self.surfaceLimbsList = loadImages.loadImages(r'./art/flames/', r'png', (16, 16))
        #load the right flame based on the limbsNum
        self.surfaceLimbsPart = self.surfaceLimbsList[self.limbsNum]
        #print 'self.limbsNum', self.limbsNum
        #finalize the surface will all the limbs on it
        self.surfaceLimbs = self.surfaceLimbsPart
        self.surfaceLimbs.set_colorkey(constants.TRANS)
        

    #----------------------------------------------------------------------
    def assAll(self):
        """puts the limbs on top of body surface,
        later will add misc surf too"""

        #take the widths of the surfs and add em together, make a surface that width
        #place the limbs on the same Y plane as body's center
        #return that new surface with all the stuff on it
        
        self.assBody()
        self.assLimbs()        

        body = self.surfaceBody
        limbs = self.surfaceLimbs
        
        bW = body.get_rect().width
        bH = body.get_rect().height
        bC = body.get_rect().center
        
        lW = limbs.get_rect().width
        lH = limbs.get_rect().height
        lC = limbs.get_rect().center
        lR = limbs.get_rect()  #create rect
        lR.center = bC
        
        #the width is the width of both part
        newSurface = pygame.surface.Surface((bW + lW, bH))
        newSurface.set_colorkey(constants.TRANS)
        newSurface.fill(constants.TRANS)
        
        
        #place body after limbs' width
        newSurface.blit(body, (lW+1, 0))
        newSurface.blit(limbs, lR)
        
        self.surface = newSurface
        return newSurface
       
       
    #----------------------------------------------------------------------
    def combine(self):
        """combines main body with etc parts like exhaust and turrets"""
        
        bodyRect = self.bodySurface.get_rect()
        try:
            flamesRect = self.etc['flames'][0].get_rect()
        except KeyError:
            #print 'key error, no flames'
            pass
        fullH = bodyRect.h
        try:
            fullW = bodyRect.w + flamesRect.w
        except:
            #print 'error'
            fullW = bodyRect.w
            
            
        fullSurface = toolsV2.createSurface(fullW, fullH)
        
        #blit body to surface
        fullSurface.blit(self.bodySurface, (fullW - bodyRect.w, 0))
        
        #blit flames to surface
        fullSurface = self.combineEtc(fullSurface)
        
        
        #fullsurface is the complete sprite with exhaust and all
        self.surface = fullSurface
        
        return self.surface
    
    #----------------------------------------------------------------------
    def combineEtc(self, fullSurface):
        """handles non body drawing ex flames"""
        #called a second time, its called once in combine()
        
        #flames
        if self.moving:
            if self.actType != 'bullet':
                try:
                    flamesRect = self.etc['flames'][int(self.flamesIndex)].get_rect()   
                
                except IndexError:
                    self.flamesIndex = 0
                    flamesRect = self.etc['flames'][int(self.flamesIndex)].get_rect()
                    
                fullSurface.blit(self.etc['flames'][int(self.flamesIndex)],
                                     (0, (flamesRect.h / 2)))
                self.flamesIndex += .1
        
        return fullSurface
      
    #----------------------------------------------------------------------
    def die(self):
        """removes self from related lists, add to dead list"""
        
        #print self, 'is removed'
        
        self.alive = False
        
        #remove self from all lists self is in
        for l in (lists.ANYTHINGs, lists.BULLETs):
            if self in l:
                l.remove(self)
                
        lists.DEADs.append(self)
        
        
    #----------------------------------------------------------------------
    def findPoints(self):
        """returns the coord of the outer perimeter of the actor"""
        
        #create a random anything instance
        #self.point2 = toolsV2.vectors.rectPerimeter(
                                    #self.rect,
                                    #self.direction)

        #new way to find front/gun point
        self.gPoint = toolsV2.vectors.intersect_perimeter(
                                    self.direction[0], 
                                    self.direction[1],
                                    self.rect.w, 
                                    self.rect.h, ) 
        self.gunPt = toolsV2.vectors.add(self.gPoint, self.rect.center)
        
        self.ePoint = toolsV2.vectors.intersect_perimeter(
                                    self.direction[0]*-1, 
                                    self.direction[1]*-1,
                                    self.rect.w, 
                                    self.rect.h, ) 
        self.exPt = toolsV2.vectors.add(self.ePoint, self.rect.center)        
        
        #return self.gunPt
            

########################################################################
class Shooter(object):
    """component for something that shoots"""

    #----------------------------------------------------------------------
    def __init__(self, owner, maxHP=100, currentHP='maxHP'):
        """Constructor"""
        
        #adds this component to owner
        owner.components['shooter'] = self
        
        self.owner = owner
        
        self.kills = 0

        #hitpoints
        self.maxHP = maxHP
        if currentHP == 'maxHP':
            self.curHP = maxHP
            
    #----------------------------------------------------------------------
    def takeDamage(self, damage):
        """takes damage, and dies if necessary"""
        
        self.curHP -= damage
        
        if self.curHP <= 0:
            self.owner.die()
            
            
    #----------------------------------------------------------------------
    def fire(self, ammo='bullet'):
        """fires an ammo type"""
        
        print 'firing'
        
        if ammo == 'bullet':
            
            
            self.owner.point = (0, 0)
            #scale the direction by speed*2
            dir = toolsV2.vectors.scale(self.owner.direction, self.owner.rect.w/2)
            #add the direction to self pos
            pos = toolsV2.vectors.add(self.owner.pos(), dir)
            #create the bullet at pos
            Bullet(self.owner.topSurface, self.owner.gunPt,
                   self.owner.direction, self.owner.speed,
                   self.owner)
        
        
        pass
    

########################################################################
class Projectle(Anything):
    """any time of projecttile to be fired"""

    #----------------------------------------------------------------------
    def __init__(self, topSurface, pos, dir, spd, owner, actType='bullet'):
        """Constructor"""
        imageListIn = loadImages.loadImages(r'./art/bullet/', 'png', (16, 16))
        
        super(Projectle, self).__init__(topSurface,
                                     pos, imageListIn, actType)
        
        print 'spawned:', self
        #self.pos = pos
    
        self.imageList= loadImages.loadImages(r'./art/bullet/', 'png', (16, 16))

        #size
        #self.width = constants.unit * 2
        #self.height = constants.unit * 2
        self.width = 16
        self.height = 16
        
        #rect of the size of the image to be
        self.rect = pygame.rect.Rect(0, 0, self.width, self.height)
        #set the rects center to the anythings pos
        self.rect.center = pos
        
        #direction
        self.direction = dir
        self.facing = (1, 0)
        
        #degrees sprite is rotated
        self.currentRotation = 0
        
        
        #speed 
        self.speed = spd
        
        #drawable surface
        self.surface = self.imageList
        #self.surface.fill(constants.BLUE)
        
        self.topSurface = topSurface
        
        #who fired it
        self.owner = owner
        
        #bounding boxes, the perimiter of the rects, in a list
        self.bboxsList = self.getBboxes()
   
        self.point = (0, 0)
        self.point2 = (0, 0), (0, 0)
        
        

    #----------------------------------------------------------------------
    def die(self):
        """explodes and removes self from main list"""
        super(Projectle, self).die()
        
        self.explode()
        
    #----------------------------------------------------------------------
    def explode(self):
        """changes the drawable surface to an explosion"""
        
        self.surface = loadImages.loadImages(r'./art/explosion/',
                                             'png', (16, 16))
        
    #----------------------------------------------------------------------
    def hit(self):
        """function is triggered when collides with rects of ANYTHINGS"""
        
        hit = self.rect.collidelist(lists.ANYTHINGs)
        if hit != -1:
            print 'hey'
            
    #----------------------------------------------------------------------
    def update(self):
        """"""
        super(Projectle, self).update()
        #update bbox
        self.bboxsList = self.getBboxes()
        
        self.findPoints()
            
            
        

########################################################################
class Bullet(Projectle):
    """projectile subclass, bullet uses owners speed, pass it in unchanged"""

    #----------------------------------------------------------------------
    def __init__(self, topSurface, pos, dir, spd, owner):
        """Constructor"""
        super(Bullet, self).__init__(topSurface, pos, dir, spd, owner)
        
        lists.BULLETs.append(self)
        
        self.moving = True
        
        self.damage = 10
        
        
        pass
    
    #----------------------------------------------------------------------
    def move(self):
        """move, different than anything in that it dies when it hits the edge"""
        super(Bullet, self).move()
        
        #if hit wall, explode then destroy
        if self.wallHit:
            self.die()
            
    #----------------------------------------------------------------------
    def update(self):
        """checks for collisions"""
        super(Bullet, self).update()
        
               
        for thing in lists.ANYTHINGs:
            if self.rect.colliderect(thing.rect):
                if thing  is not self.owner and thing is not self:
                    print 'collided with', thing
                    print 'thing width', thing.rect.w
                    thing.components['shooter'].takeDamage(self.damage)
                    if not thing.alive:
                        print self.owner, 'got a kill'
                        self.owner.components['shooter'].kills += 1
                    #since it's a bullet,die
                    self.die()
    
    

#----------------------------------------------------------------------
def spawnAnything(surface, imageList, pos = 'random'):
    """spawns an Anything instance at a random pos"""
    
    if pos == 'random':
        #random position
        x = random.randint(1, constants.WIDTH)
        y = random.randint(1, constants.HEIGHT)
    else:
        x = pos[0]
        y = pos[1]
    
    #create a character
    character = Anything(surface, (x, y), imageList)
    Shooter(character, maxHP=10)
    print 'Spawnname:', character.name, 'pos:', character.rect.center    

