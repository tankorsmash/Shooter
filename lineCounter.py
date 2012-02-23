import glob

if __name__ == '__main__':
    """Run the following if module is top module"""
    
    #folder
    folder = r'.\\'
    #path becomes folder with the format
    path =  folder + r'*.{0}'.format('py')
    
    #files list
    fileList = []
    for filepath in glob.glob(path):
            #print 'filepath:', filepath
            
            print filepath
            
            fileList.append(filepath)
            
            
    linesList = []
    for path in fileList:
        
        with open(path, 'r') as f:
            
            for line in f.readlines():
                linesList.append(line)
                
                
    print len(linesList)
    
    for line in linesList:
        print line
    #print linesList