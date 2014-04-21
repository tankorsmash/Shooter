'''the GUI for the game, want to make it so you can edit the values on the fly
for debugging'''

from Tkinter import *  
#import squares
import tkFont
import threading



class Debug(Frame):
    '''Main debug frame that updates with squares'''
    
    def __init__(self, parent=None, **options):
        Frame.__init__(self, parent, **options)
        
        print 'packed debug'
        
        self.lbl_Title = Label(self, text='DEBUG!')
        
        self.lbl_Title.grid(column=0, row=0, sticky='we')
        #self.lbl_Title.config(bg='black', )
        #self.lbl_Title.rowconfigure(0, weight=2, )
        
        self.TEST = 123
        
        self.bind('a', (lambda event: self.changeTEST(222)),)
        
        self.grid(column = 0, row = 0,)
        #self.build()
        
    
    def update(self):
        '''update entries, and send them over to squares'''
        
        pass
    
    def changeTEST(self, value):
        '''change TEST to value'''
        print 'changed TEST'
        self.TEST = value
    
    def build(self):
        '''create entry widgets'''
        root.bind('<Destroy>', (lambda e:root.destroy))
        
        self.buildBasicStats(squares.player)
        
        self.buildShooterStats(squares.player)
    
    def buildBasicStats(self,subject):
        '''use the subject.stats.basicStats dict to build a list 
        of entries that you can edit later in the GUI'''
        
        #create the frame
        basic = Frame(self)
        basic.config(bg='red',)
        
        #title label
        basicTitle = Label(basic, text='Basic Stats')
        basicTitle.grid(column= 0, sticky='we', columnspan=3 )
        basicTitle.config(font =tkFont.Font(slant=tkFont.ITALIC))
        
        #italics
        #ital = tkFont(slant=tkFont.ITALIC)
        #bas
        
        r = 1 #values to increase 
        c = 1 # as loop goes on
        for key, value in subject.stats.basicStats.items():
            
            #create a label/entry pair for k/v
            lblKey = Label(basic, text=key + ':')
            entValue = Entry(basic)
            
            #insert a value for the entry
            entValue.insert(0, value)
            
            #pack em in with grid
            lblKey.grid(column=0, row=r)
            entValue.grid(column=1, row=r)
            
            #increase the values since the loop ran
            r += 1
            c += 1
            
        basic.grid()
        
    def buildShooterStats(self,subject):
        '''use the subject.stats.shooterStats dict to build a list 
        of entries that you can edit later in the GUI'''
        
        #create the frame
        shooter = Frame(self)
        shooter.config(bg='red',)
        
        #title label
        shooterTitle = Label(shooter, text='Shooter Stats')
        shooterTitle.grid(column= 0, sticky='we', columnspan=3 )
        shooterTitle.config(font =tkFont.Font(slant=tkFont.ITALIC))
        
        #italics
        #ital = tkFont(slant=tkFont.ITALIC)
        #bas
        
        r = 1 #values to increase 
        c = 1 # as loop goes on
        for key, value in subject.stats.shooterStats.items():
            
            #create a label/entry pair for k/v
            lblKey = Label(shooter, text=key + ':')
            entValue = Entry(shooter)
            
            #insert a value for the entry
            entValue.insert(0, value)
            
            #pack em in with grid
            lblKey.grid(column=0, row=r)
            entValue.grid(column=1, row=r)
            
            #increase the values since the loop ran
            r += 1
            c += 1
            
        shooter.grid()
        
            
        
    
    
    def buildBasicInfo(self, parent, subject):
        '''going to just create a name and position entry for 
        the subject'''
        
        #called self because that's going to be root
        basic = Frame(parent)
        
        basicTitle = Label(basic, text='Basic Info')
        basicTitle.grid(column=0, sticky='w')
        
        
        r = 1
        for item in [subject.name, subject.pos]:
            ent = Entry(basic)
            ent.insert(0, item)
            ent.grid(column = 0, row=r)
            r += 1
            #ent.bind('a', (lambda event: self.changeTEST(222)),)
            
        basic.grid(row=1)
    
    def buildMiscInfo(self, parent, subject):
        '''add more fun stats, like kills and shots fired'''
    
        misc = Frame(parent)
        
        miscTitle = Label(misc, text='Misc Info')
        miscTitle.grid(column=0, sticky='w')
        
        r = 1
        for item in [subject.shooter.timesFired, ]:
            ent = Entry(misc)
            ent.insert(0, item)
            ent.grid(row=r)
            r += 1
            #ent.bind('a', (lambda event: self.changeTEST(222)),)
            
        misc.grid(row=2)
def run():
    '''create and run the GUI '''
    global root
    root = Tk()
    main = Debug(root)
    
    print root.geometry('0x0+1+1')
    print '>>made root'
    main.build()
    print 'build basic'
    root.mainloop()
    print 'root closed<<'
    #root.destroy()
    #main.destroy()
    #print 'root destroy'
    #kill the thread so I can open it again
    #squares.thread_GUI2.


if __name__ == '__main__':
    
    print 'Idiot. =D'