#builtins
import random, pygame

#customs
import lists, constants, tools, loadImages, main

########################################################################
class Anything(object):
    """General class that contains drawing, movement, position
    will be  """

    #----------------------------------------------------------------------
    def __init__(self, topSurface, position, imageListIn):
        """Constructor"""
        
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
        self.direction = tools.vectors.normalize((1, 0))
        self.moving = False
        
        #make a spriteList for drawing
        self.spriteIndex = 0
        self.limbsNum = 0
        self.assemble(imageListIn)        

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
        
        #draws a rect around the surface
        pygame.draw.rect(surface, constants.BLUE, self.rect, 1)
        
        #blits the image to where rect it, blitted is the rect of where the thing is on screen
        self.blitted = surface.blit(self.surface, self.rect)
        
        #print 'type',type(self)
        
        
        
    #----------------------------------------------------------------------
    def rotate(self, angle):
        """rotates the surface by angle"""
        #print 'angle', angle
        #takes the argument angle and add to it self.angle to maintain proper angles
        angle = self.currentRotation + angle
        
        #forgets old surface and resets it to default right facing one
        #self.surface = self.spriteList[self.spriteIndex]
        self.surface = self.assAll()
        
        #since blitted is the rect of surface on screen, takes its center (pos)
        #oldCenter = self.blitted.center
        oldCenter = self.rect.center
        
        #rotate the newly reset surface
        self.surface = pygame.transform.rotate(self.surface, angle)
        
        
        #updates currentRotation for next time
        self.currentRotation = angle
        
        #sets self.rect to the new surface
        self.rect = self.surface.get_rect()
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
        
 
        #find angles between pos and facing/pos and direction
        facingAngle = tools.angleBetweenTwoPoints(self.pos(), self.facing)
        directionAngle = tools.angleBetweenTwoPoints(self.pos(), self.direction)
        #print 'angles f and d', facingAngle, directionAngle
        
        #if angles are different
        #if facingAngle != directionAngle:
        difference = facingAngle - directionAngle
        self.rotate(-difference)
        
        
        #cycle through flames.
        if constants.frameNum % 15 == 0:
                
                if self.limbsNum >= len(self.surfaceLimbsList) - 1:
                    self.limbsNum = 0
                
                else:
                    self.limbsNum += 1
                
                
                
                pass
        
        
            
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
    def die(self):
        """removes self from related lists, add to dead list"""
        
        for l in (lists.ANYTHINGs, lists.BULLETs):
            if self in l:
                l.remove(self)
                
        lists.DEADs.append(self)
        
        
            

########################################################################
class Shooter(object):
    """component for something that shoots"""

    #----------------------------------------------------------------------
    def __init__(self, owner, maxHP=100, currentHP='maxHP'):
        """Constructor"""
        
        #adds this component to owner
        owner.components['shooter'] = self
        
        self.owner = owner

        #hitpoints
        self.maxHP = maxHP
        if currentHP == 'maxHP':
            self.curHP = maxHP
            
            
    #----------------------------------------------------------------------
    def fire(self, ammo='bullet'):
        """fires an ammo type"""
        
        print 'firing'
        
        if ammo == 'bullet':
            #scale the direction by speed*2
            dir = tools.vectors.scale(self.owner.direction, self.owner.speed*2)
            #add the direction to self pos
            pos = tools.vectors.add(self.owner.pos(), dir)
            #create the bullet at pos
            Bullet(self.owner.topSurface, pos, self.owner.direction, self.owner.speed)
        
        
        pass
    

########################################################################
class Projectle(Anything):
    """any time of projecttile to be fired"""

    #----------------------------------------------------------------------
    def __init__(self, topSurface, pos, dir, spd):
        """Constructor"""
        
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
        
        #speed
        self.speed = spd
        
        #drawable surface
        self.surface = self.imageList[0]
        #self.surface.fill(constants.BLUE)
        
        self.topSurface = topSurface
        
        #self.draw(topSurface)
        
        
    #----------------------------------------------------------------------
    def rotate(self):
        """testing overrides"""
        
        pass
    

    #----------------------------------------------------------------------
    def die(self):
        """explodes and removes self from main list"""
        super(Projectle, self).die()
        
        self.explode()
        
    #----------------------------------------------------------------------
    def explode(self):
        """changes the drawable surface to an explosion"""
        
        self.surface = loadImages.loadImages(r'./art/explosion/',
                                             'png', (16, 16))[0]
        
    #----------------------------------------------------------------------
    def hit(self):
        """function is triggered when collides with rects of ANYTHINGS"""
        
        hit = self.rect.collidelist(lists.ANYTHINGs)
        if hit != -1:
            print 'hey'
            
            
        

########################################################################
class Bullet(Projectle):
    """projectile subclass, bullet uses owners speed, pass it in unchanged"""

    #----------------------------------------------------------------------
    def __init__(self, topSurface, pos, dir, spd):
        """Constructor"""
        super(Bullet, self).__init__(topSurface, pos, dir, spd)
        
        lists.BULLETs.append(self)
        
        self.moving = True
        
        
        pass
    
    #----------------------------------------------------------------------
    def move(self):
        """move, different than anything in that it dies when it hits the edge"""
        super(Bullet, self).move()
        
        #if hit wall, explode then destroy
        if self.wallHit:
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
    print 'Spawnname:', character.name, 'pos:', character.rect.center    

