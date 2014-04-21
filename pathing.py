from pprint import pprint as p


########################################################################
class AStar(object):
    """pathfinding"""

    #----------------------------------------------------------------------
    def __init__(self, start, end):
        """Constructor"""
        
        self.openList = []
        self.closedList = []
        
        self.edgeG = 10
        self.cornerG = 14
        
        self.start = start
        self.end = end
        
        print 'starting search'
        self.beginSearch()
        print 'done searching'
        
        
    #----------------------------------------------------------------------
    def beginSearch(self):
        """starts pathfinding"""
        
        # ( tile , parent ) > now it's just tile
        self.start.parent = self.start
        self.start.G = 0
        self.start.H = self.calcH(self.start, self.end)
        self.start.F = self.calcF(self.start)
        self.openList.append(self.start)  #1
        
        #loop starts here
        x = 1
        #print 'end:', self.end
        while self.end not in self.closedList:
            self.openList.sort(key=lambda tile:tile.F, reverse=False)
            print 'loop start, round', x
            #print 'len of closed list', len(self.closedList)
            #print 'lowest
            x += 1
            #4, find lowest F from openlist put it in closed
            possibleTile = self.openList[0]
            self.openList.remove(possibleTile)
            self.closedList.append(possibleTile)
            
            #5 check nearby, add them to open if not in open or closed list
            for tile in possibleTile.nearby:

                if tile not in self.closedList:
                    if not tile.ID[0] < 0 \
                       and not tile.ID[1] < 0\
                       and not tile.ID[0] > 1000 \
                       and not tile.ID[1] > 1000\
                       and not tile.unwalkable:  #and also unwalkable
                        if tile not in self.openList:
                            tile.parent = possibleTile
                            tile.G = self.calcG(tile.parent, tile)
                            tile.H = self.calcH(tile, self.end)
                            tile.F = self.calcF(tile)
                            tile.parent = possibleTile
                            self.openList.append(tile)
                        elif tile in self.openList:
                            #6 if going through possible tile is faster 
                            if self.calcG(possibleTile, tile) < \
                                  tile.G:  #possibleTiles not the parent, test the G
                                # to see if it is faster if it IS.
                                tile.parent = possibleTile
                                tile.G = self.calcG(tile.parent, tile)
                                tile.F = self.calcF(tile)
            
        print 'done searching, length of path:', len(self.closedList)
                        
        return self.buildPath()        
        
        
    #----------------------------------------------------------------------
    def buildPath(self):
        """go through all the tiles parents to another"""
        
        self.path = []
        
        node = self.end
        while node != self.start:
            
            self.path.append(node)
            node = node.parent
        
        print 'done building path'
        return self.path
        
        
        
    #----------------------------------------------------------------------
    def calcH(self, currentTile, endTile):
        """finds the h with manhattan algo"""
        
        sx, sy = currentTile.ID
        ex, ey = endTile.ID
        
        H = (ex - sx) + (ey - sy)
        
        return H
    
    #----------------------------------------------------------------------
    def calcG(self, sourceTile, currentTile):
        """finds G from sourceTile to currentTile by adding
        sources's G to e's corner or edge value"""
        
        sx, sy = sourceTile.ID
        ex, ey = currentTile.ID  
    
        if sx != ex and sy != ey:
            #print 'corner!'
            g = self.cornerG
            
        else:
            #print 'edge!'
            g = self.edgeG
            
        return g + sourceTile.G
        
    #----------------------------------------------------------------------
    def calcF(self, currentTile):
        """adds G and H together"""
        
        F =  currentTile.G + currentTile.H
        
        return F
    

#########################################################################
#class AI:
    #"""class that handles all AI"""

    ##----------------------------------------------------------------------
    #def __init__(self):
        #"""Constructor"""
        
        
    
    