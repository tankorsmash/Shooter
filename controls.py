'''Controls module for the project, contains keyboard, mouse and joypad handling'''

import pygame as PG

import tools, actors, lists, constants
import loadImages

#movement list
movementCtrlsDict = {'w': 'up',
                 'a': 'left',
                 's': 'down',
                 'd': 'right',
                 }

dirDict= {'up': (0, -1),
              'down': (0, 1),
              'left': (-1, 0),
              'right': (1, 0),
              }

shooterCtrlsDict = {'c': 'shootBullet',
                }

debugCtrlsDict = {'b': 'createAnything',
              }

#----------------------------------------------------------------------
def initJoysticks():
    """counts all the joysticks,assigns to a list"""
    
    print 'BEGIN JOYSTICK LOAD'
    #number of joysticks connected
    njoy = PG.joystick.get_count()
    print '\tFound', njoy, 'joysticks.'
    
    #add each to list
    global gamePad
    gamePad = []
    for pad in xrange(njoy):
        joy = PG.joystick.Joystick(pad)
        joy.init()
        print '\t\tJoystick', pad, 'has', joy.get_numbuttons(), 'buttons'
        gamePad.append(joy)
    

    print 'END JOYSTICK LOAD\n'
    #except:
        #print 'no gamepad'    



#----------------------------------------------------------------------
def inputHandler():
    """handles mouse and keyboard events"""
    
    
    for e in PG.event.get():
            
        if e.type == PG.KEYDOWN \
             or e.type == PG.KEYUP: 
            keyHandler(e)
            
        elif e.type == PG.MOUSEBUTTONDOWN \
             or e.type == PG.MOUSEBUTTONUP \
             or e.type == PG.MOUSEMOTION:
            mouseHandler(e)
            
        pass

#----------------------------------------------------------------------
def timeTheShit(n):
    """time the two calls, one is local the other is module"""
    
    def here():
        print 'this ones here'
        
    import timeit
    
    a = timeit.timeit(here, number=n)
    
    b = timeit.timeit(tools.there, number=n)
    
    from tools import there

    c = timeit.timeit(there, number=n)
    
    print a, b, c

#----------------------------------------------------------------------
def movementControls(action):
    """handles movement controls. Ex: wasd"""
    print '\taction:', action
    
    if not lists.ANYTHINGs[0].moving:
        lists.ANYTHINGs[0].moving = True
    print '\tdict result', dirDict[action]
    lists.ANYTHINGs[0].direction = dirDict[action]
    print '\tnew dir', lists.ANYTHINGs[0].direction
    #else:
        #lists.ANYTHINGs[0].moving = False
        
    
        
    
    
    pass
#----------------------------------------------------------------------
def shooterControls(action):
    """handles shooter controls. Ex: shoot bullet"""

    if action == 'shootBullet':
        lists.ANYTHINGs[0].components['shooter'].fire()
        
    pass

#----------------------------------------------------------------------
def debugControls(action):
    """handles debug controls. Ex: createActor"""
    
    if action == 'createActor':
        actors.spawnAnything(screen, imageList)
    pass
    
#----------------------------------------------------------------------
def keyHandler(e):
    """handles only keyboard"""
   
    #letter keys
    #try:
        
        #if chr(e.key) in range(256):
        
        #isLetter = 1
        
    #else:
        #isLetter = 0
    if e.type == PG.KEYDOWN and e.key in xrange(256):
        
        #save the keydown key
        lists.keysDown.append(chr(e.key))
        #print 'added', e.key
        
            
        #movement
        if chr(e.key) in movementCtrlsDict.keys():
            print 'start movement controls'
            movementControls(movementCtrlsDict[chr(e.key)])
            print 'end movement controls'
            
            
        #shooter
        elif chr(e.key) in shooterCtrlsDict.keys():
            print 'start shooter controls'
            shooterControls(shooterCtrlsDict[chr(e.key)])
            print 'end shooter controls'
            
        #debug
        elif chr(e.key) in debugCtrlsDict.keys():
            print 'start debug controls'
            debugControls(debugCtrlsDict[chr(e.key)])
            print 'end debug controls'
            
        #other
        else:
            print e.key, 'is not assigned to a list'
            
            if isKey(e.key,'l'):
                print 'caught', chr(e.key)
                
                flames = loadImages.loadImages(r'./art/flames/', 'png', (16, 16))
                
                lists.flames = flames
                constants.FLAMES = True
                
            elif isKey(e.key,'c'):
                print 'caught', chr(e.key)
                
                #create a random anything instance
                actors.spawnAnything(screen, imageList)
    
                
            elif isKey(e.key,'m'):
                print 'caught', chr(e.key)
                
                x, y = lists.ANYTHINGs[0].pos()
                PG.mouse.set_pos(x, y)
                
            elif isKey(e.key, 'q'):
                print 'caught', chr(e.key)
                
                print 'facing', lists.ANYTHINGs[0].facing
                print 'direction', lists.ANYTHINGs[0].direction
                print 'pos', lists.ANYTHINGs[0].pos()
                print 'mouse', PG.mouse.get_pos()
    
    elif e.type == PG.KEYUP and e.key in xrange(256):
        lists.keysDown.remove(chr(e.key))
        #print 'removed', e.key, lists.keysDown
        
        mixedList = [k for k in lists.keysDown if k in movementCtrlsDict.keys()]
        #print 'mixed', len(mixedList)
        if len(mixedList) == 0:
            
            lists.ANYTHINGs[0].moving = False
#----------------------------------------------------------------------
def isKey(event, key):
    """if event key is key return true"""
    
    try:
        event = chr(event)
        
    except:
        print 'not a character key'
        
    #print 'event, key:', event, key
    if event == key:
        return True
    
    else: return False
     
        
#----------------------------------------------------------------------
def mouseHandler(e):
    """handles only mouse events"""
    
    #if left-click
    if e.type == PG.MOUSEBUTTONDOWN and e.button == 1:  # or e.type == PG.MOUSEBUTTONUP:
        pass
    
        lists.ANYTHINGs[0].moving = True
        #try:
        #find the angle between player, direction and mouse
        angle = tools.vectors.angleObjToAnother(lists.ANYTHINGs[0], e)
        #angle = tools.vectors.sineRule(e.pos,
                                       #lists.ANYTHINGs[0].direction,
                                       #lists.ANYTHINGs[0].pos())
        #print 'angle between mouse and pos:', angle
        
        #rotate direction by angle
        newDirRotated = tools.vectors.rotate(lists.ANYTHINGs[0].direction, angle)
        
        #change player dir
        lists.ANYTHINGs[0].direction = newDirRotated
        
        angle = tools.vectors.angleObjToAnother(lists.ANYTHINGs[0], e)
        #angle = tools.vectors.sineRule(e.pos,
                                       #lists.ANYTHINGs[0].direction,
                                       #lists.ANYTHINGs[0].pos())            
        #print '2angle between mouse and pos:', angle
        
        if angle != 0:
            print 'wrong way'
            
            #rotate direction by angle
            newDirRotated = tools.vectors.rotate(lists.ANYTHINGs[0].direction, -angle)
            
            #change player dir
            lists.ANYTHINGs[0].direction = newDirRotated                

        #except RuntimeError:
            #print 'runtme error'
            
        #pass
    
    elif e.type == PG.MOUSEBUTTONUP and e.button == 1:
        try:
            lists.ANYTHINGs[0].moving = False
        
        except:
            print 'no one to move'
            
            
    #elif right-click
    elif e.type == PG.MOUSEBUTTONDOWN and e.button == 3:
        
        #angle mouse, dir
        print 'click, angle between', tools.angleBetweenTwoPoints(e.pos, lists.ANYTHINGs[0].direction)
        pass
        
    #elif mouse moved
    elif e.type == PG.MOUSEMOTION:
        
        
        pass
        
    #elif scroll up
    elif e.type == PG.MOUSEBUTTONDOWN and e.button == 4:
    
        #rotate all by -45
        for thing in lists.ANYTHINGs:
            thing.rotate(-45)
    
    
    #elif scroll down
    elif e.type == PG.MOUSEBUTTONDOWN and e.button == 5:
    
        #rotate player by 45
        lists.ANYTHINGs[0].rotate(45)
        
        pass
    
    #elif other buttons
    elif e.type == PG.MOUSEBUTTONDOWN:
        
        print 'button', e.button
        print 'event:', e
