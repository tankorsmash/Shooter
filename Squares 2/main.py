'''Launch this file for game control'''
import tools, logic, GUI, stats, actors
import multiprocessing as mp

if __name__ == '__main__':
    """Run the following if module is top module"""
        
    '''New or Load screen'''
    #tools.newOrLoad()
    #skip it:
    stats.newOrLoad =  'New'
    
    #create or load game info
    if stats.newOrLoad == 'New':
        '''create new files to use'''
        print 'creating new game instance'
        #processLogic = mp.Process(target=logic.gameStart, name='processLogicSTR')
        #processLogic.start()
        #print 'logic thread started !'
        
        print 'not using threads right now'
        logic.gameStart()
        #won't do anything now, but will later on when I've got a better idea
        
    elif stats.newOrLoad == 'Load':
        '''loads previous files'''
        print 'loading previous game instance'
        
    else:
        print 'can\'t use', stats.newOrLoad


    #while processLogic.is_alive():
        
        #pass
    
    #else: print 'logic thread closed!'

#left from if name main idiom        
else:
    'run main.py as the toplevel'