target = (75, 75)

########################################################################
class tile(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, lowCord, highCord):
        """Constructor"""
        
        self.xs = lowCord[0], highCord[0]
        self.ys = lowCord[1], highCord[1]
        
    
    
tile1 = tile((1, 1), (25, 25))

tile2 = tile((26, 26), (50, 50))

tile3 = tile((51, 51), (75, 75))

tile4 = tile((76, 76), (100, 100))

tiles = [tile1, tile2, tile3, tile4] * 206
for i in xrange(61):
        
    for tile in tiles:
        if tile.xs[0] <= target[0] <= tile.xs[1]:
            if tile.ys[0] <= target[1] <= tile.ys[1]:
                #print tile
                pass
        
print 'done'
print len(tiles)

