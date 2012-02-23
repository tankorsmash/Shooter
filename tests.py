import unittest
import tools

########################################################################
class vectorTester(unittest.TestCase):
    """tests functions of vectors"""

    

    ##----------------------------------------------------------------------
    #def __init__(self):
        #"""Constructor"""
        
        
    #----------------------------------------------------------------------
    def testLength(self):
        """assert that length of 5,0 is 5"""
        
        self.assertEqual(tools.vectors.length((5, 0)), 5, 'length is wrong')
        
    def testSub(self):
        '''sub between 1,1 and 0,0'''
        
        self.assertEqual(tools.vectors.sub((2, 1), (0, 0)), (2, 1))
        
        
    def testDistance(self):
        '''distance vector between'''
        
        self.assertAlmostEqual(tools.vectors.distance((5, 5), (0, 0)), 7, 0)
        
    #----------------------------------------------------------------------
    def testScale(self):
        """"""
        self.assertEqual(tools.vectors.scale((1, 1), 5), (5, 5))
        
if __name__ == '__main__':
    """Run the following if module is top module"""
    
    unittest.main()        