import numpy as np
#import pylab
import datetime
from time import mktime
#import mx.DateTime
import writebt7
import re
import scanparser
import os
from copy import deepcopy

translate_dict = {}

def construct_translate_dict():
    # Commented fields do not need to have their names changed.
    
    #translate_dict['pt.'] = 
    translate_dict['sgu'] = 'smplutilt' #'sample_upper_tilt'
    translate_dict['time'] = 'duration'
    #translate_dict['detector'] = 
    #translate_dict['monitor'] = 

    '''
    #??? what are these fields???
    translate_dict['mcu'] = 
    translate_dict['focal_length'] = 
    translate_dict['m1'] = 
    translate_dict['m2'] = 
    translate_dict['mcrystal'] = 
    translate_dict['marc'] = 
    translate_dict['mtrans'] = 
    translate_dict['mfocus'] = 
    translate_dict['s1'] = 
    translate_dict['s2'] = 
    '''
    translate_dict['sgl'] = 'smplltilt' #'sample_lower_tilt'
    translate_dict['stl'] = 'smplltrn' #'sample_lower_translation'
    translate_dict['stu'] = 'smplutrn' #'sample_upper_translation'
    #translate_dict['a1'] = 
    #translate_dict['a2'] = 
    #translate_dict['q'] = 
        
    #translate_dict['h'] = 
    #translate_dict['k'] = 
    #translate_dict['l'] = 
    #translate_dict['ei'] = 
    #translate_dict['ef'] = 
    #translate_dict['e'] = 
    #translate_dict['coldtip'] = 
    
    #NOTE: hfir files have these axes for 2D plotting, whereas dataflow uses it for 3D
    # if these below are uncommented, translate_fields must check metadata to replace keys
    # and incorporate them into data_abstraction's translate()
    #translate_dict['def_x'] = 'xaxis'
    #translate_dict['def_y'] = 'yaxis'
    
def translate_fields(data):
    """
    Given a data dictionary, translates field names based on the translate_dict
    """
    if translate_dict == {}:
        construct_translate_dict()

    for key in translate_dict.keys():
        if data.has_key(key):
            data[translate_dict[key]] = data[key]
            del data[key]
    
def get_tokenized_line(myfile,returnline=['']):
    lineStr = myfile.readline()
    returnline[0] = lineStr.rstrip()
    strippedLine = lineStr.lower().rstrip()
    tokenized = strippedLine.split()

    return tokenized

def get_columnmetadatas(tokenized, data):
    # initializes all fields in data to empty lists.
    columnlist = []

    for i in range(1, len(tokenized)):
        field = tokenized[i].lower()
        if field == 'h':
            field = 'qx'
        if field == 'k':
            field = 'qy'
        if field == 'l':
            field = 'qz'
            
        #if field == 't-act':
        #    field = 'temp'
      
        columnlist.append(field)
        data[field] = []
        
    return columnlist

def convert_time(values):
    # converts times from am/pm to the 24 hour timescale
    time_info = values.split(' ')
    times = time_info[0].split(':')
    
    for i in range(len(times)): #convert strings to integers
        times[i] = int(times[i])
        
    if time_info[1].lower() == 'pm' and not int(times[0]) == 12:
        times[0] += 12
    elif time_info[1].lower() == 'am' and int(times[0]) == 12:
        times[0] = 0
        
    return times




def readfile(myfilestr):
    #get first line
    myFlag = True
    returnline = ['']
    
    myfile = open(myfilestr, 'r')
    data = {}
    metadata = {}

    while myFlag:
        tokenized = get_tokenized_line(myfile, returnline=returnline)
        if not tokenized:
            break
        elif tokenized == [] or tokenized == ['']:
            #TODO check that this is necessary
            continue #skip blank lines
            
        if tokenized[1].lower() == 'col_headers':
            tokenized = get_tokenized_line(myfile, returnline=returnline)
            columnlist = get_columnmetadatas(tokenized, data)
            
            while 1:
                lineStr = myfile.readline()
                if not(lineStr):
                    break
                if lineStr[0] != "#":
                    strippedLine = lineStr.rstrip()
                    tokenized = strippedLine.split()
                    
                    # getting data points 
                    for i in range(len(tokenized)):
                        field = columnlist[i]
                        data[field].append(float(tokenized[i]))
            
        else: #if not column headers or the actual data lines, then it's metadata
            field = tokenized[1]
            line = returnline[-1]
            
            #if tokenized[2] == '=':
            values = line.split('=')[1].strip() # everything right of the '='
            
            if field == 'time':
                time_value = convert_time(values)
                metadata['start_time'] = time_value
            elif field == 'date':
                date_info = values.split('/')
                metadata['month'] = date_info[0]
                metadata['day'] = date_info[1]
                metadata['year'] = date_info[2]
            elif field == 'latticeconstants': #make dictionary of a,b,c,alpha,beta,gamma
                values = values.split(',')
                lattice_dict = {'a': float(values[0]), 'b': float(values[1]), 'c': float(values[2]),
                                'alpha': float(values[3]), 'beta': float(values[4]), 'gamma': float(values[5])}
                metadata['lattice'] = lattice_dict
            elif field == 'ubmatrix':
                values = np.array(values.split(','), dtype='float64')
                metadata[field] = values
            elif field == 'plane_normal':
                values = np.array(values.split(','), dtype='float64')
                metadata[field] = values
            elif field.lower() == 'sum': # Sum of Counts
                pass
            elif field.lower() == 'center': # Center of Mass
                pass
            elif field.lower() == 'full': # Full Width Half-Maximum
                pass
            elif tokenized[-1].lower() == 'completed.': # last line with time when scan was completed
                myFlag = False # stop reading the file
            else:
                try:
                    metadata[field] = float(values)
                except:
                    metadata[field] = values

    translate_fields(data)
    data = Data(metadata, data)    
    return data


class Data(object):
    def __init__(self):
        self.metadata = {}
        self.data = {}
        #self.columnlist = []
        #self.additional_metadata = {}
    def __init__(self, metadata, data):
        self.metadata = metadata
        self.data = data


def num2string(num):
    numstr=None
    if num<10:
        numstr='00'+str(num)
    elif (num>=10 & num <100):
        numstr='0'+str(num)
    elif (num>100):
        numstr=str(num)
    return numstr

def genfiles(myfile_nums, myfile_end='.dat',mydirectory=r'/hfir/HB3/exp331/Datafiles',myfile_base='HB3_exp0331_scan'):
    file_list=[]
    for myfile_num in myfile_nums:
        if myfile_num<10:
            myfile_numstr='000'+str(myfile_num)
        elif myfile_num>9 and myfile_num<100:
            myfile_numstr='00'+str(myfile_num)
        elif myfile_num>99 and myfile_num<1000:
            myfile_numstr='0'+str(myfile_num)
        else:
            myfile_numstr=str(myfile_num)
        myfilestr=os.path.join(mydirectory,myfile_base+myfile_numstr+myfile_end)
        print myfilestr
        file_list.append(myfilestr)
    return file_list

if __name__=='__main__':
    if 0:
        mon0=9000
        myfilestr=r'hfir_data/HB3/exp331/Datafiles/HB3_exp0331_scan0001.dat'
               
        
        #0014.dat
        myfile_num=84
        file_list=genfiles(range(84,100))
        print file_list
        #metadata={}
        #data=readfile(myfilestr,metadata)
        #print data.header
        #print data.metadata
        #print data.columnlist
        
    if 1:
        #file_list = genfiles([1,1])
        
        myfilestr = r'hfir_data/HB3/exp331/Datafiles/HB3_exp0331_scan0001.dat'
        data = readfile(myfilestr)
        print data
        
        
        
