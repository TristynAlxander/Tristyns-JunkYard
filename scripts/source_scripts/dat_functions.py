import os

class DatFileList:
    def __init__(self, file_path):
        self.data       = None                                                   #
        self.file_path  = file_path                                              #
        self.dimensions = 2
        
        if(os.path.isfile(self.file_path)):
            dat_file = open(self.file_path,"r")                                 #
            
            # Do Preliminary read to make sure every line is same number of data?
            data_length = 0
            parsable = True
            for line in dat_file:                                               # Horizontal Split ( into rows    ) 
                cols = [s.strip() for s in line.split('  ') if s]
                if(data_length == 0):
                    data_length = len(cols)
                if(len(cols) != data_length):
                    print("bad_data: Requires Abnormal Whitespace Parsing")
                    parsable = False
            dat_file.seek(0)                                                    # Reset Pointer
            if(parsable):
                if(data_length>1):
                    for line in dat_file:                                           # Horizontal Split ( into rows    ) 
                        cols = [s.strip() for s in line.split('  ') if s]
                        if(self.data == None):
                            self.data = [[] for i in range(0,len(cols))]
                        for d,c in zip(self.data,cols):
                            d.append(c)
                else:
                    self.data = [line for line in dat_file]
                    self.dimensions = 1
            else:
                print("could not parse data")
                print("consider encoding without whitespace\n(i.e. replace whitespace with underscores)")
        else:
            dat_file = open(self.file_path,"w+")                                #
            self.data = []                                                      #
class DatFileList_T:
    def __init__(self, file_path):
        self.data       = None                                                   #
        self.file_path  = file_path                                              #
        self.dimensions = 2
        
        if(os.path.isfile(self.file_path)):
            dat_file = open(self.file_path,"r")                                 #
            
            # Do Preliminary read to make sure every line is same number of data?
            data_length = 0
            parsable = True
            for line in dat_file:                                               # Horizontal Split ( into rows    ) 
                cols = [s.strip() for s in line.split('  ') if s]
                if(data_length == 0):
                    data_length = len(cols)
                if(len(cols) != data_length):
                    print("bad_data: Requires Abnormal Whitespace Parsing")
                    parsable = False
            dat_file.seek(0)                                                    # Reset Pointer
            if(parsable):
                if(data_length>1):
                    for line in dat_file:                                           # Horizontal Split ( into rows    ) 
                        cols = [s.strip() for s in line.split('  ') if s]
                        self.data.append(cols)
                else:
                    self.data = [line for line in dat_file]
                    self.dimensions = 1
            else:
                print("could not parse data")
                print("consider encoding without whitespace\n(i.e. replace whitespace with underscores)")
        else:
            dat_file = open(self.file_path,"w+")                                #
            self.data = []                                                      #
class DatFileDict_T:
    def __init__(self, file_path):
        self.data      = None                                                   #
        self.file_path = file_path                                              #
        
        if(os.path.isfile(self.file_path)):
            dat_file = open(self.file_path,"r")                                 #
            
            # Do Preliminary read to make sure every line is same number of data?
            data_length = 0
            parsable = True
            for line in dat_file:                                               # Horizontal Split ( into rows    ) 
                cols = [s.strip() for s in line.split('  ') if s]
                if(data_length == 0):
                    data_length = len(cols)
                if(len(cols) != data_length):
                    print("bad_data: Requires Abnormal Whitespace Parsing")
                    parsable = False
                    break
                if(data_length == 1):
                    print("bad_data: Dictionaries Require Two Dimensions")
                    parsable = False
                    break
            dat_file.seek(0)                                                    # Reset Pointer
            
            if(parsable):
                self.data = {}
                for line in dat_file:                                           # Horizontal Split ( into rows    ) 
                    cols = [s.strip() for s in line.split('  ') if s]
                    if(self.data == {}):
                        for col in cols:
                            self.data[col] = []
                    else:
                        for (k,d),c in zip(self.data.items(),cols):
                            d.append(c)
            else:
                print("could not parse data")
                print("consider encoding without whitespace\n(i.e. replace whitespace with underscores)")
        else:
            dat_file = open(self.file_path,"w+")                                #
            self.data = []                                                      #
            
class DatFileDict:
    def __init__(self, file_path):
        self.data      = None                                                   #
        self.file_path = file_path                                              #
        
        if(os.path.isfile(self.file_path)):
            dat_file = open(self.file_path,"r")                                 #
            
            # Do Preliminary read to make sure every line is same number of data?
            data_length = 0
            parsable = True
            for line in dat_file:                                               # Horizontal Split ( into rows    ) 
                cols = [s.strip() for s in line.split('  ') if s]
                if(data_length == 0):
                    data_length = len(cols)
                if(len(cols) == 1):
                    print("bad_data: Dictionaries Require Two Dimensions")
                    parsable = False
                    break
            dat_file.seek(0)                                                    # Reset Pointer
            
            if(parsable):
                self.data = {}
                for line in dat_file:                                           # Horizontal Split ( into rows    ) 
                    cols = [s.strip() for s in line.split('  ') if s]
                    self.data[cols[0]] = cols[1:]
                for k,d in self.data.items():
                    if(len(d) == 1):
                        self.data.update({k:d[0]})
            else:
                print("could not parse data")
                print("consider encoding without whitespace\n(i.e. replace whitespace with underscores)")
        else:
            dat_file = open(self.file_path,"w+")                                #
            self.data = []                                                      #
            