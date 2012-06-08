import numpy as N
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
    translate_dict['sgu'] = 'sample_upper_tilt'
    #translate_dict['time'] = 
    #translate_dict['detector'] = 
    #translate_dict['monitor'] = 

    
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
    
    translate_dict['sgl'] = 'sample_lower_tilt'
    translate_dict['stl'] = 'sample_lower_translation'
    translate_dict['stu'] = 'sample_upper_translation'
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
    
 
    
def get_tokenized_line(myfile,returnline=['']):
    lineStr = myfile.readline()
    returnline[0] = lineStr.rstrip()
    strippedLine = lineStr.lower().rstrip()
    tokenized = strippedLine.split()

    return tokenized



def readcolumns(myfile):
    columndict,columnlist=get_columnmetadatas(myfile)
    # get the names of the fields
    #prepare to read the data
    count =  0
    while 1:
        lineStr = myfile.readline()
        if not(lineStr):
            break
        if lineStr[0] != "#":
            count=count+1
            strippedLine=lineStr.rstrip().lower()
            tokenized=strippedLine.split()
            for i in range(len(tokenized)):
                field=columnlist[i]
                columndict[field].append(float(tokenized[i]))
    return columndict,columnlist


def get_columnmetadatas(tokenized, data):
    # initializes all fields in data to empty lists.
    columnlist = []

    for i in range(1, len(tokenized)):
        field = tokenized[i]
        columnlist.append(field)
        data[field] = []
        
    return columnlist



def readfile(myfilestr):
    #get first line
    myFlag = True
    header = []
    returnline = ['']
    
    myfile = open(myfilestr)
    data = {}
    metadata = {}

    while myFlag:
        tokenized = get_tokenized_line(myfile, returnline=returnline)
        if tokenized == []:
            tokenized = ['']
            
        if tokenized[1] == 'pt.':
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
            myFlag = False
    if len(columndict[columnlist[0]]) == 0:
        columndict={}
        columnlist=[]
        #This is a drastic step, but if the file is empty, then no point in even recording the placeholders

    data=Data()
    data.header=deepcopy(header)
    data.data=deepcopy(columndict)
    data.metadata=deepcopy(metadata)
    data.columnlist=deepcopy(columnlist)
    data.additional_metadata=deepcopy(additional_metadata)
    return data


class Data(object):
    def __init__(self):
        self.header = []
        self.metadata = {}
        self.data = {}
        self.columnlist = []
        self.additional_metadata = {}


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
        metadata = {}
        #file_list = genfiles([1,1])        
        #data = readfile(file_list[0], metadata)
        
        myfilestr = r'hfir_data/HB3/exp331/Datafiles/HB3_exp0331_scan0001.dat'
        data = readfile(myfilestr)
        print data
        
        
        
