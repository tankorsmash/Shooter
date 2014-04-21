'''this is just code that was not used anymore. hopefully ill put it up on
the internet and someone might like it. Every class represents a module it
was taken from'''

#----------------------------------------------------------------------
def actors(object):
    """"""
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
       
      