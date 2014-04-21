import pygame as PG

#----------------------------------------------------------------------
def popUp(msg='text', title=None, w=250,background=(255, 200, 175),
            font='Times', fsize=12, fcolor=(0, 0, 0)):
    """pops up a box with text on it
    returns the surface w/ the dialog"""
    
    
    borderWidth = 4
    cornerRadius = 10
    lineColor = (11, 11, 101)
    #text inside
    f = PG.font.SysFont(font, fsize)
    
    if title:
        titleLines = breakupText(title, f, w, borderWidth, cornerRadius)
        listTitleSurfs = renderTextToSurf(titleLines, f, fcolor, 1)

    #break up the title and text into lines to render
    lines = breakupText(msg, f, w, borderWidth , cornerRadius)
    #put textSurfaces with the rendered text in the created list
    listLinesSurfs = renderTextToSurf(lines, f, fcolor)
    
    #calc their combined height
    height = 0
    for surface in listLinesSurfs:
        height += surface.get_rect().h
        #print 'before h', height
        
    if title:
        #beforeTitleHeight = height
        for surface in listTitleSurfs:
            height += surface.get_rect().h
            
            #print 'after h', height
            
        #afterTitleHeight = height
    
    
    #create a surf to blit texts too, to put borders onto
    surfaceLines = PG.surface.Surface((w, height))
    surfaceLines.set_colorkey((123, 123, 123))
    surfaceLines.fill((123, 123, 123))
    
    #move all the renderedTexts to the larger surface
    #n = 0
    #height of blitting
    drawingH = 0
    if title:
        for surface in listTitleSurfs:
            surfaceLines.blit(surface, (0, drawingH))
            drawingH += surface.get_rect().h
        
    for surface in listLinesSurfs:
        surfaceLines.blit(surface, (0, drawingH))
        #n += 1
        drawingH += surface.get_rect().h
        
    #now we have a surface with all the text on it: surfaceLines
    
    borderedSurface = drawBorders(drawingH, cornerRadius, w,
                                  background, lineColor, borderWidth)
    
    borderedSurface.blit(surfaceLines, (cornerRadius + borderWidth, borderWidth))
    
    #print 'returning a surface', borderedSurface
    return borderedSurface

#----------------------------------------------------------------------
def breakupText(rawText, font, w, borderWidth, cornerRadius):
    """breaks up text into lines that are smaller that width"""
    f = font
    
    splitText = rawText.split('\n')
    #for each line in rawText
    allLines = []
    for text in splitText:
            
        #get width of surface with text on it
        width = f.size(text)[0]
        #print 'width:', width
        #if width is too wide, try breaking down the lines:
        lines = []
        if width >= w - 20:
            #break down the sentence by word
            wordList = text.split(' ')
            widthNeeded = w - (borderWidth * 2)
            #while textwidth is wider than width
            while f.size(' '.join(wordList))[0] >= widthNeeded:
                
                wordCount = 0
                linesize = 0
                currentLine = []
                while f.size(' '.join(currentLine))[0] < widthNeeded:
                    #try to add another word, test first if itd fit
                    listed = list(wordList[wordCount])
                    if f.size(' '.join(currentLine + listed))[0] < widthNeeded:
                        currentLine.append(wordList[wordCount])
                        wordCount += 1
                    else:
                        break
                        
                    
                lines.append(currentLine)
                for word in currentLine:
                    wordList.remove(word)
                    
            #print 'leftover words:', wordList
            lines.append(wordList)
        else:
            lines.append(text)
          
        allLines.append(lines)

    return allLines


#----------------------------------------------------------------------
def drawBorders(drawingH, cornerRadius, w, background, lineColor, borderWidth):
    """draws the borders of a window"""
    
    h = drawingH + cornerRadius
    surf = PG.surface.Surface((w, h))
    surf.fill(background)
    surf.set_colorkey((123, 123, 123))
    
    #corners of the surface
    tlcorner = (0, 0)
    trcorner = (w - 1, 0)
    blcorner = (0, h - 1)
    brcorner = (w - 1, h - 1)
    points = (tlcorner, trcorner, brcorner, blcorner)
    
    size = (25, 25)
    
    #set up rects with corners from above
    rects = []
    for pos in points:
        rect = PG.Rect(pos, size)
        rect.center = pos
        rects.append(rect)
    
    #draw each circle in the corners
    for rect in rects:
        PG.draw.circle(surf, lineColor , rect.center, cornerRadius)
        
    #draw lines to each corner
    PG.draw.lines(surf, lineColor, 1, points, borderWidth)
    
    return surf

#----------------------------------------------------------------------
def renderTextToSurf(lines, font, fcolor, underline=0):
    """renders a list of lines of text, and returns a list of them"""
    listLinesSurfs = []

    font.set_underline(underline)
        
    for line in lines:
        printable = ' '.join(line)
        surfaceText = font.render(printable, 0, fcolor)
        listLinesSurfs.append(surfaceText)
        
    return listLinesSurfs
  
  
#----------------------------------------------------------------------
def splitLines(text, width):
    """splits lines according to width"""
    
    lines = []
    if width >= w - 20:
        
        #break down the sentence by word
        wordList = msg.split(' ')
        widthNeeded = w - (borderWidth * 2)
        #while msgwidth is wider than width
        while f.size(' '.join(wordList))[0] >= widthNeeded:
            
            wordCount = 0
            linesize = 0
            currentLine = []
            while f.size(' '.join(currentLine))[0] < widthNeeded:
                #try to add another word, test first if itd fit
                listed = list(wordList[wordCount])
                if f.size(' '.join(currentLine + listed))[0] < widthNeeded:
                    currentLine.append(wordList[wordCount])
                    wordCount += 1
                else:
                    break
                    
                
            lines.append(currentLine)
            for word in currentLine:
                wordList.remove(word)
                
       #print 'leftover words:', wordList
        lines.append(wordList)
      
    return lines  