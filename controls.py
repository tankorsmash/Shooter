'''Controls module for the project, contains keyboard, mouse and joypad handling'''

import pygame as PG, random

import toolsV2, actors, lists, constants, pathing
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
def inputHandler(surface):
    """handles mouse and keyboard events, surface is the main screen"""
    
    
    for e in PG.event.get():
            
        if e.type == PG.KEYDOWN \
             or e.type == PG.KEYUP: 
            keyHandler(e, surface)
            
        elif e.type == PG.MOUSEBUTTONDOWN \
             or e.type == PG.MOUSEBUTTONUP \
             or e.type == PG.MOUSEMOTION:
            mouseHandler(e, surface)
            
        pass

#----------------------------------------------------------------------
def timeTheShit(n):
    """time the two calls, one is local the other is module"""
    
    def here():
        print 'this ones here'
        
    import timeit
    
    a = timeit.timeit(here, number=n)
    
    b = timeit.timeit(toolsV2.there, number=n)
    
    from toolsV2 import there

    c = timeit.timeit(there, number=n)
    
    print a, b, c

#----------------------------------------------------------------------
def movementControls(action, surface):
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
        print '\t', 
        lists.ANYTHINGs[0].components['shooter'].fire()
        
    pass

#----------------------------------------------------------------------
def debugControls(action, surface):
    """handles debug controls. Ex: createActor"""
    
    if action == 'createAnything':
        try:
            tile = random.choice(lists.all_tiles)
            pos_chosen = random.choice(tile.coords)
            
            actors.spawnAnything(surface, loadImages.loadImages(
                            r'./art/man/', 'png'),
                            pos=pos_chosen)
        
        except IndexError as e:
            print str(e).upper(), 'grid\'s probably not made, right click and try again'
        
#----------------------------------------------------------------------
def keyHandler(e, surface):
    """handles only keyboard"""
   
    #letter keys
    #try:
        
        #if chr(e.key) in range(256):
        
        #isLetter = 1
        
    #else:
        #isLetter = 0
    if e.type == PG.KEYDOWN and e.key in xrange(256):
        print 'caught the "', chr(e.key), '" key'
        
        #save the keydown key
        lists.keysDown.append(chr(e.key))
        #print 'added', e.key
        
            
        #movement
        if chr(e.key) in movementCtrlsDict.keys():
            print 'start movement controls'
            movementControls(movementCtrlsDict[chr(e.key)], surface)
            print 'end movement controls'
            
            
        #shooter
        elif chr(e.key) in shooterCtrlsDict.keys():
            print 'start shooter controls'
            shooterControls(shooterCtrlsDict[chr(e.key)])
            print 'end shooter controls'
            
        #debug
        elif chr(e.key) in debugCtrlsDict.keys():
            print 'start debug controls'
            debugControls(debugCtrlsDict[chr(e.key)], surface)
            print 'end debug controls'
            
        #other
        else:
            print e.key, 'is not assigned to a list'
            
            if isKey(e.key,'l'):
                
                
                flames = loadImages.loadImages(r'./art/flames/', 'png', (16, 16))
                
                lists.flames = flames
                constants.FLAMES = True
                
            elif isKey(e.key,'z'):
                
                
                plr = lists.ANYTHINGs[0]
                #create a random anything instance
                lists.ANYTHINGs[0].point2 = toolsV2.vectors.rectPerimeter(
                                            lists.ANYTHINGs[0].rect,
                                            lists.ANYTHINGs[0].direction)
    
                #new way
                lists.ANYTHINGs[0].point2 = toolsV2.vectors.intersect_perimeter(
                                            plr.direction[0], 
                                            plr.direction[1],
                                            plr.rect.w, 
                                            plr.rect.h, ) 
                plr.point2 = toolsV2.vectors.add(plr.point2, plr.rect.center)
                
            elif isKey(e.key,'m'):
                
                x, y = lists.ANYTHINGs[0].pos()
                PG.mouse.set_pos(x, y)
                
            elif isKey(e.key, 'q'):
                
                print 'facing', lists.ANYTHINGs[0].facing
                print 'direction', lists.ANYTHINGs[0].direction
                print 'pos', lists.ANYTHINGs[0].pos()
                print 'mouse', PG.mouse.get_pos()
                
            elif isKey(e.key, 'h'):
                
                #loads the image of a house and counts the points that are transparent
                house = loadImages.loadImages(r'./art/house/', 'house1.png', 'orig')
                trans_points = []
                colorkey = house.get_colorkey()
                for x in xrange(house.get_rect().w-1):
                    for y in xrange(house.get_rect().h-1):
                        color = house.get_at((x, y))
                        if color == colorkey:
                            trans_points.append((x, y))
                            pass
                #adds the transparent points to the list
                lists.DEBUGs['house'] = house, trans_points
                print 'number of transparent points in house', len(trans_points)
                
            elif isKey(e.key, 'p'):
                global path_found
                path_found = pathing.AStar(lists.TILEs[0][0], lists.TILEs[10][22])
                
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
def mouseHandler(e, surface):
    """handles only mouse events"""
    
    #if left-click
    if e.type == PG.MOUSEBUTTONDOWN and e.button == 1:  # or e.type == PG.MOUSEBUTTONUP:
        pass
    
        lists.ANYTHINGs[0].moving = True
        #try:
        #find the angle between player, direction and mouse
        
        isSameAngle = 0
        count = 0
        while not isSameAngle:
                
            angle = toolsV2.vectors.angleOfTwoPoints(lists.ANYTHINGs[0].pos(),
                                                     lists.ANYTHINGs[0].direction,
                                                     e.pos)
            print 'angle between mouse and direction', angle
            
            #rotate direction by angle
            newDirRotated = toolsV2.vectors.rotate(lists.ANYTHINGs[0].direction,
                                                 angle)
            
            
            angle = toolsV2.vectors.angleOfTwoPoints(lists.ANYTHINGs[0].pos(),
                                                     newDirRotated,
                                                     e.pos)
            
            print 'angle between mouse and newDir', angle, 'that number should be zero'
            
            #change player dir
            lists.ANYTHINGs[0].direction = newDirRotated                
    
            if angle == 0:
                isSameAngle = 1
                
            else:
                #make sure it doesn't run forever
                count += 1
                if count > 100:
                    print 'stopped inf loop in rotation'
                    break
    
            #except RuntimeError:
                #print 'runtme error'
                
            #pass
        print '\n'
    
    elif e.type == PG.MOUSEBUTTONUP and e.button == 1:
        try:
            lists.ANYTHINGs[0].moving = False
        
        except:
            print 'no one to move'
            
            
    #elif right-click
    elif e.type == PG.MOUSEBUTTONDOWN and e.button == 3:
        
        
        lists.TILEs = toolsV2.createGrid()
        pass
        
    #elif mouse moved
    elif e.type == PG.MOUSEMOTION:
        
        
        pass
        
    #elif scroll up
    elif e.type == PG.MOUSEBUTTONDOWN and e.button == 4:
    
        ##rotate all by -45
        #for thing in lists.ANYTHINGs:
            #thing.rotate(-45)
    
        #lists.ANYTHINGs[0].bodySurface = \
            #PG.transform.scale2x(lists.ANYTHINGs[0].bodySurface)
        
        PG.display.iconify()
    
    #elif scroll down
    elif e.type == PG.MOUSEBUTTONDOWN and e.button == 5:
    
        ##rotate player by 45
        #lists.ANYTHINGs[0].rotate(45)
        
        lists.ANYTHINGs[0].bodySurface = lists.ANYTHINGs[0].spriteList[1]
        
        pass
    
    #elif other buttons
    elif e.type == PG.MOUSEBUTTONDOWN:
        
        print 'button', e.button
        print 'event:', e
