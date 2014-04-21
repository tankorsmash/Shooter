
##----------------------------------------------------------------------
#def entryExit(f):
    #""""""
    #def new_f():
        
        #print 'entering', f.__name__
        #f()
        #print 'exiting', f.__name__
        
    #return new_f


#@entryExit
#def hello():
    #print 'hello'
    
    
#hello()

########################################################################
class deco(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, f):
        """Constructor"""
        
        print 'init'
        self.f = f
        
        
    #----------------------------------------------------------------------
    def __call__(self, *args, **argsv):
        """"""
        
        print 'call'
        self.f(*args, **argsv)
        print 'out of call'
        
    
@deco
def hello(a, b, c):
    print 'hello', a, b, c
    
hello('asd', 'bc', 'qwe')
