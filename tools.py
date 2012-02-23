'''random tools for the project'''

import math

#----------------------------------------------------------------------
def loadTextFile(filepath):
    """loads a textfile to a variable, returns a list of lines"""
    
    #open filepath, read data
    with open(filepath, 'r') as f:
        
        #create a list to hold lines
        data = []
        #fetch lines
        for line in f.readlines():
            line = line.rstrip()
            data.append(line)
            
        #return list of lines
        return data
    
    
########################################################################
class Vector(object):
    """class for doing vector math, imports math"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        pass
    
    
    #----------------------------------------------------------------------
    def normalize(self, vector):
        """divide each component by the length of the vector"""
        
        x = vector[0]
        y = vector[1]
        
        length = self.length(vector)
        
        nX = x / length
        nY = y / length
        
        return nX, nY            
                
    #----------------------------------------------------------------------
    def rotate(self, vector, degree):
        """rotates a vector by degrees"""
        
        x, y = vector
        
        theta = math.radians(degree)
        
        cs = math.cos(theta)
        sn = math.sin(theta)
        
        px = x * cs - y * sn
        py = x * sn + y * cs
        
        #return (round(px, 10), round(py, 10))
        px, py = self.normalize((px, py))
        
        return px, py
    
    #----------------------------------------------------------------------
    def length(self, vector):
        """length of a vector with pythagoras"""
        
        #x **2 + y **2
        a = (vector[0]**2 + vector[1]**2)
        
        length = math.sqrt(a)
        
        return length
    
    #----------------------------------------------------------------------
    def distance(self, p1, p2):
        """distance between two vectors:
           length of the differential vector length(p2-p1)"""
        
        diff = self.sub(p1, p2)
        
        len = self.length(diff)
        
        return len
        
        
        
    #----------------------------------------------------------------------
    def scale(self, v, scale):
        """scale the vector bigger or smaller"""
        
        x = v[0] * scale
        y = v[1] * scale
        
        return x, y
    
    #----------------------------------------------------------------------
    def add(self, V1, V2):
        """add two vectors"""
        #change pos
        x,y = V1
        x += V2[0]
        y += V2[1]
        return x, y
  
    #----------------------------------------------------------------------
    def sub(self, V1, V2):
        """subract v2 from v1"""
        
        x = V1[0] - V2[0]
        y = V1[1] - V2[1]
        
        return x, y
    
    def angle(self, o, p1, p2):
        '''the angle between two points around origin
        
        eq= len(op1)**2 + len(op2)**2 - len(p1p2)**2 over
             / 2*len(op1)*len(op2) '''

        ##norm both points
        #p1 = self.normalize(p1)
        #p2 = self.normalize(p2)
        
        
        #lengths of both points from origin
        a = self.distance(o, p1)
        b = self.distance(o, p2)
        c = self.distance(p1, p2)
        
        #print 'distance of a, b, c:', a, b, c       
        
        
        #main equation
        cosC = (a ** 2 + b ** 2 - c ** 2) / (2 * a * b)
        #print 'result of equation', cosC
        
        
        ##solve cos with var cosC
        #Ccos = math.cos(cosC)
        #print 'used equations result and cosd it', Ccos
        
        try:
            
            C = math.acos(cosC)
            
        except ValueError:
            C = 0
        #print 'angle between the two points in relation to origin in rads', C
        
        #value in degrees
        angle = math.degrees(C)
        #print 'C in degrees', degC
        return round(angle, 2)
        
        
    #----------------------------------------------------------------------
    def sineRule(self, a='coord', bVec='velocity', c='coord'):
        """uses the triangle rule returns rounded angle to two places
            also treats bVec as a velocity away from c(player)"""
        
        #distance of c to a
        lenCA = self.distance(c, a)
        
        #make c to b the same distance #maybe not needed though
        scaledCB = self.scale(bVec, lenCA)
        
        #joinedBC is not the same length as CA
        b = self.add(c, scaledCB)
        
        #to find the and of C corner
        angle = self.angle(a, b, c)
        
        return round(angle)
        
        
        
    #----------------------------------------------------------------------
    def angleObjToAnother(self, obj, other):
        """origin object with a velocity vector and a target object
           returns the angle between the object's velocity and other's postion"""
        
        #get pos from function else its a attribute
        try:
            otherPos = other.pos()
            
        except TypeError:
            otherPos = other.pos
        
        #find the length between object and other's postion
        objToOtr = self.distance(obj.pos(), otherPos)
        #multiply that distance to the direction of the object
        scaledDirection = self.scale(obj.direction, objToOtr)
        #combined vector of postion and direction to properly 
        # place the direction on the cartesian plane
        addDir = self.add(obj.pos(), scaledDirection)
        #calc angle between pos, dir, other
        angle =  self.angle(obj.pos(), addDir, other.pos)
        
        #print '### angle between direction and mouse ###', angle
 
        return round(angle)
        
    #----------------------------------------------------------------------
    def linkScaleVector(self, origin, sat, scale):
        """used for pos and directio, scales the satellite vector to scale
           and adds it to origin"""
        
        scaled = self.scale(sat, scale)
        
        added = self.add(origin, scaled)
        
        return added
                
    

def angleBetweenTwoPoints(p1, p2):
    '''return in angle in deg of the angle between two points'''
    #old way 0-360
    a1 = math.atan2(p1[1], p1[0])
    a2 = math.atan2(p2[1], p2[0])
    angle1 = (a1 - a2) % (2 * math.pi)
    angle1 = math.degrees(angle1)
    #print 'first way :', angle1
    
    #new way seems to work better -180 - 180
    x = p2[0] - p1[0]
    y = p2[1] - p1[1]
    angle2 = math.atan2(y, x)  #* (180 / math.pi)
    angle2 = math.degrees(angle2)
    #print 'second way:', angle2
    
    return round(angle1)



#----------------------------------------------------------------------
def distBetweenTwoPoints(p1, p2):
    """Calculates the distance between two points"""
    
    x = p2[0] - p1[0]
    y = p2[1] - p1[1]    

    return x, y

vectors = Vector()

#----------------------------------------------------------------------
def there():
    """used for timing"""
    
    print 'there motherfucker'
        
if __name__ == '__main__':
    """Run the following if module is top module"""
    
    #test
    loadTextFile(r'AmericanMaleNames.txt')