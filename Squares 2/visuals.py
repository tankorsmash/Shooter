'''handles all of the visual screen stuff, so pygame essentially'''

#builtins
import os
#squares
import pygame, tools, stats

import txtlib



#colors
BLACK = (0,0,0) 
WHITE = (255,255,255)

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#----------------------------------------------------------------------
def multiLine(text):
    """prints a line of text"""
    txtBox = txtlib.Text((500, 300), 'Arial', text=text)
    txtBox.update()
    screen.blit(txtBox.area,(0, 100) )


#----------------------------------------------------------------------
def drawLine(start, end,  color= BLACK, width = 1):
    """draws line on screen"""
    pygame.draw.line(screen, color, start, end, width)

#----------------------------------------------------------------------
def start():
    """create and returns the pygame screen"""
    global screen, basicFont
    pygame.init()
    pygame.display.set_caption('Line Moving App')
    
    #tools.seticon('bricks.ico')    
    
    screen = pygame.display.set_mode((stats.WIDTH, stats.HEIGHT))
    screen.set_colorkey((255,255,254))
    
    #setup a font for the game
    basicFont = pygame.font.SysFont(None, 32)   
    #a pygame clock inst
    
    
    pygame.display.flip()
    
    pathname = os.path.abspath(os.path.curdir)
    pathname += '/art/man/'
    
    return screen
    #spawner = Spawner()    

if __name__ == '__main__':
    """Run the following if module is top module"""
        
    # ########INIT######### #
    pygame.init()
    pygame.display.set_caption('Line Moving App')
    
    #tools.seticon('bricks.ico')    
    
    screen = pygame.display.set_mode((stats.WIDTH, stats.HEIGHT))
    screen.set_colorkey((255,255,254))
    
    #setup a font for the game
    basicFont = pygame.font.SysFont('Arial', 16)   
    #a pygame clock inst
    clock = pygame.time.Clock()
    
    pygame.display.flip()
    
    pathname = os.path.abspath(os.path.curdir)
    pathname += '/art/man/'
    
    
    #spawner = Spawner()
    
    #___x___
    #__x_x__
    #_x_x_x_
    #___x___
    #___x___