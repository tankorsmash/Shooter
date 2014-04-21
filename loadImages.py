import pygame

import constants


#----------------------------------------------------------------------
def loadImages(folder, filetype, size=(32, 32)):
    """load images from a given folder of a given format,
    returns a surface of each or takes a single file and returns 1 surface"""
    
    import glob
    #list of all the images to be returned
    imageList = []    
    
    if '.' not in filetype:
        path =  folder+r'*.{0}'.format(filetype)
    else:
        path = folder + filetype
    
    ##to check abs path
    #print 'path', path
    #import os.path
    #print os.path.abspath(path)
    
    
    for filepath in glob.glob(path):
        #print 'filepath:', filepath
        
        #scale the image at filepath
        image = scaleImage(filepath, size)
        
        #append the image to the list of images
        imageList.append(image)
        
    #when its done, return the list or single image surce
    try:
        if len(imageList) > 1:
            return imageList
        
        else:
            return imageList[0]
            
    except IndexError:
        
        print 'bad image'
        

#----------------------------------------------------------------------
def scaleImage(path, (size)):
    """scales an image to size tuple"""
    
    #load the image to a surface and set the colorkey
    imageSurface = pygame.image.load(path).convert()
    imageSurface.set_colorkey(constants.TRANS)
    
    #print path
    
    #scale it and get the rect of the surface
    if type(size) == tuple:
        scaledSurface = pygame.transform.scale(imageSurface, size)

    else:  #or dont scale
        scaledSurface = imageSurface
        
    scaledSurface.set_colorkey(constants.TRANS)
    scaledRect = scaledSurface.get_rect()
    
    return scaledSurface