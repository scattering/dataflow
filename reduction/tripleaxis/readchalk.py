import sys, os
import re,copy
import numpy as np
#from matplotlib import pylab
from matplotlib.ticker import FormatStrFormatter
import matplotlib.delaunay as D
from matplotlib.ticker import NullFormatter, MultipleLocator,MaxNLocator, NullLocator
#from scipy.signal.signaltools import convolve2d


translate_dict = {}

def construct_translate_dict():
    """
    Creates a dictionary to translate names (keys) used in chalk files into the ones
    used in data_abstraction.py's TripleAxis objects' fields.
    
    Names unique to chalk files that may be left as they are (commented out)
    """

    translate_dict['run'] = 'run'
    translate_dict['database id'] = 
    translate_dict['sha1'] = 
    translate_dict['point'] = 
    translate_dict['sig'] = 'detector' # signal counts

    translate_dict['dbhf'] = 'diffracted_beam_horizontal_field'
    translate_dict['dbvf'] = 'diffracted_beam_vertical_field'
    translate_dict['sbvf'] = 'scattering_beam_vertical_field'
    translate_dict['sbhf'] = 'scattering_beam_horizontal_field'

    translate_dict['2tm'] = 'a2' # two theta monochromator
    translate_dict['psi'] = 'a3' # theta sample 
    translate_dict['phi'] = 'a4' # two theta sample
    translate_dict['2ta'] = 'a6' # two theta analyzer
    translate_dict['a'] = 
    translate_dict['anax'] = 
    translate_dict['arm'] = 'arm'

'''
translate_dict['monochromator_theta'] = 'a1'
translate_dict['monochromator_two_theta'] = 'a2'
translate_dict['sample_theta'] = 'a3'
translate_dict['sample_two_theta'] = 'a4'
translate_dict['analyzer_theta'] = 'a5'
translate_dict['analyzer_two_theta'] = 'a6'
'''
    
    
    translate_dict['ctemp']
    translate_dict['date']
    translate_dict['db'] = 'monitor'
    translate_dict['det'] = 'eta_step'
    translate_dict['dze'] = 'zeta_step'
    translate_dict['dnu'] = 'energy_step'
    #translate_dict['dspace_anax'] = 'analyzer_dspacing'
    #translate_dict['dspace_monox'] = 'monochromator_dspacing'
    translate_dict['eprim'] = 'e' #Energy of the incident beam (THz)--> should convert to meV
    
    translate_dict['eta'] = 'eta'
    translate_dict['zeta'] = 'zeta'        
    translate_dict['etm'] = 'eta_scan_center'
    translate_dict['zem'] = 'zeta_scan_center'
    
    translate_dict['field']
    translate_dict['file']
    translate_dict['hhconst']
    translate_dict['hhihf']
    translate_dict['ihfa'] = 'current_horizontal_coil_a'
    translate_dict['ihfb'] = 'current_horizontal_coil_b'
    translate_dict['ihfc'] = 'current_horizontal_coil_c'    
    translate_dict['ivfb'] = 'current_vertical_coil_bottom' 
    translate_dict['ivft'] = 'current_vertical_coil_top' 
    
    #translate_dict['kprim'] 
    translate_dict['mfield']
    translate_dict['mode'] = 'scan_type'
    translate_dict['monox']
    translate_dict['npts']
    translate_dict['nu']
    translate_dict['num']
    

    translate_dict['r']
    translate_dict['rbc']
    translate_dict['rec']
    translate_dict['rtemp']
    
    translate_dict['seq']
    translate_dict['stemp'] = 'temp'
    translate_dict['time']
    
    
    

def get_tokenized_line(myfile, returnline=None):
    if returnline==None:
        returnline=['']
    lineStr=myfile.readline()
    if lineStr=='':
        returnline=None
        tokenized=None
        return tokenized
    returnline[0]=lineStr.rstrip()
    strippedLine=lineStr.lower().rstrip()
    tokenized=strippedLine.split()
    
    return tokenized

class Data(object):
    def __init__(self,metadata,data,header=None,additional_metadata=None):
        self.metadata=metadata
        self.data=data
        self.header=header
        self.additional_metadata=additional_metadata
        self.pp={}
        self.pm={}
        self.mm={}
        self.mp={}
        self.angles={}


def get_column_meta_data(tokenized,columndict,columnlist):
    for i in np.arange(len(tokenized)):
        field = tokenized[i].lower()
        if field == 'mon=':
            continue
        if field =='sig='.lower():
            continue
        if 1:
            columndict[field]=[]
            columnlist.append(field)
    return columndict,columnlist

def metawrapper(metadata,key,value):
    if metadata.has_key(key):
        metadata[key].append(value)
    else:
        #CHECK: should all metadata be a list???
        metadata[key]=[]
        metadata[key].append(value)

'''
def readaof(myfilestr,run_range=None):
    myfile=open(myfilestr,'r')
    #get first line
    myFlag=True
    if run_range==None:
        run_range=[-np.inf,np.inf]
    metadata={}
    header=[]
    point_lines=0
    data=Data()
    while myFlag:
        returnline=['']

        tokenized=get_tokenized_line(myfile,returnline=returnline)
        print returnline
        if tokenized==None:
            break

        if tokenized==[]:
            tokenized=['']
            continue
        if tokenized[0]=='reserved':
            continue
        if tokenized[0]=='use' and tokenized[1]=='name':
            continue
        if tokenized[0]=='use' and tokenized[1]=='comment':
            #skip the next two lines to be safe...
            get_tokenized_line(myfile,returnline=returnline)
            get_tokenized_line(myfile,returnline=returnline)
            continue
            
        if tokenized[0]=='mode':
            metawrapper(metadata,tokenized[0],tokenized[1])
            metawrapper(metadata,tokenized[2],tokenized[3])
            metawrapper(metadata,tokenized[4],tokenized[5])
            continue
        
        if tokenized[0]=='monox':
            metawrapper(metadata,tokenized[0],tokenized[1])
            metawrapper(metadata,tokenized[5],tokenized[6])
            metawrapper(metadata,'dspace_monox',tokenized[3].split(']')[0])
            metawrapper(metadata,'dspace_anax',tokenized[8].split(']')[0])
            continue
            
        if tokenized[0].lower()=="#Date".lower():
            pass
        if returnline[0].find('=')<0 and not tokenized[0]=='point':
            for i in range(0,len(tokenized)-1,2):
                #if tokenized[i]==']':
                #    if tokenized[i]=='monox':
                #        metadata['dspace_monox']=tokenized[i+1]
                #    if tokenized[i]=='anax':
                #        metadata['dspace_anax']=tokenized[i+1]
                #    i=i+1
                metawrapper(metadata,tokenized[i],tokenized[i+1])
                if tokenized[i]=='date':
                    metawrapper(metadata,'time',tokenized[-1])
        if metadata.has_key('run'):
            curr_run=int(metadata['run'][-1])
            if curr_run<run_range[0]:
                continue
            if curr_run>run_range[1]:
                myFlag=False
                break
                    
            
        else:
            i=0
            while i < len(tokenized)-1:
                if tokenized[i].find('=')>=0:
                    if tokenized[i].split('=')[0][-1]==']':
                        #metadata[tokenized[i-2]]=tokenized[i+1] #parsing the monitor line is a pain!!!!
                        i=i+1
                    else:
                        metawrapper(metadata,tokenized[i].split('=')[0],tokenized[i+1])
                        i=i+2
                else:
                    i=i+1
                  
        if returnline[0].lower().find('point')>=0:
            columndict1={}; columnlist1=[]; columnlist2=[]; columndict2={}
            columndict1,columnlist1=get_column_meta_data(tokenized,columndict1,columnlist1)
            tokenized=get_tokenized_line(myfile,returnline=returnline)
            columndict2,columnlist2=get_column_meta_data(tokenized,columndict2,columnlist2)
            #columndict2=copy.deepcopy(columndict1)
            #print columndict1
            #print columndict2
            #print columnlist1
            #print columnlist2
            #print 'reading'
            if data.angles=={}:
                data.angles=copy.deepcopy(columndict1)
                data.pp=copy.deepcopy(columndict2)
                data.pm=copy.deepcopy(columndict2)
                data.mp=copy.deepcopy(columndict2)
                data.mm=copy.deepcopy(columndict2)
            #start reading points
            myFlag2=True
            currpoint=1
            prevpoint=None
            overshot=False  #to deal with when we've reached the next point...
            while myFlag2:
                if not overshot:
                    tokenized=get_tokenized_line(myfile,returnline=returnline)
                overshot=False
                if tokenized==[] or tokenized==None:
                    myFlag2=False
                    continue
                else:
                    #read in the angles
                    for i in range(len(columnlist1)):
                        field=columnlist1[i]
                        data.angles[field].append(float(tokenized[i]))
                    currpoint=tokenized[0]
                    prevpoint=tokenized[0]
                    #read in polarized beam channels
                    polarized_flag=True
                    while polarized_flag:
                        #read in the polarized beam data
                        tokenized=get_tokenized_line(myfile,returnline=returnline)
                        if tokenized==[] or tokenized==None:
                            break
                        currpoint=tokenized[0]
                        if currpoint==prevpoint:
                            for i in range(len(columnlist2)):
                                field=columnlist2[i]
                                #DB SB
                                if float(tokenized[-2])==0 and float(tokenized[-1])==0:
                                    channel='pp'
                                if float(tokenized[-2])==0 and float(tokenized[-1])>0:
                                    channel='pm'
                                if float(tokenized[-2])>0 and float(tokenized[-1])==0:
                                    channel='mp'
                                if float(tokenized[-2])>0 and float(tokenized[-1])>0:
                                    channel='mm'
                                
                                datachannel=getattr(data,channel)  
                                datachannel[field].append(float(tokenized[i]))
                        else:
                            polarized_flag=False
                            overshot=True
                    
                    #read in the second polarized beam channel
                    #tokenized=get_tokenized_line(myfile,returnline=returnline)  
                    #for i in range(len(columnlist2)):
                    #    field=columnlist2[i]
                    #    data.pm[field].append(float(tokenized[i]))
                    ##print data.angles
                        
                    
                    
            if len(data.angles['point'])==0:
                columndict={}
                columnlist=[]
                data.pp={}
                data.angles={}
                data.pm={}
                data.mm={}
                data.mp={}
                #This is a drastic step, but if the file is empty, then no point in even recording the placeholders
                #print self.columndict['Qx']
                #print self.columnlist
                
    return data,metadata
''' 
            
def readacf(myfilestr, data=None, metadata=None):
    myfile = open(myfilestr,'r')

    myFlag=True
    header=[]
    point_lines = 0
    curr_run = 0
    
    if data == None:
        data={}
    if metadata == None:
        metadata={}
        
    while myFlag:
        returnline = ['']
        tokenized = get_tokenized_line(myfile, returnline=returnline)
        
        if tokenized == None:
            # end of file
            break
        
        if tokenized == []:
            # read an empty line
            tokenized=['']
            continue
        '''
        # no longer permitting a certain number of runs to be read; now read whole file
        if tokenized[0] == 'run':
            curr_run = curr_run + 1
            if fileExt=='.acf':
                print 'acf'
            #curr_run=int(metadata['run'][-1])
            #curr_run=int(metadata['run'][curr_run-1])
            
            
            if curr_run<run_range[0]:
                continue
            if curr_run>run_range[1]:
                myFlag=False
                break
        else:
        '''
        # TODO BEGIN: get back to this with Mon_[] and add name/comment to metadata
        i=0
        while i < len(tokenized)-1:
            if tokenized[i].find('=')>=0:
                if tokenized[i].split('=')[0][-1]==']':
                    #metadata[tokenized[i-2]]=tokenized[i+1] #parsing the monitor line is a pain!!!!
                    i=i+1
                else:
                    if fileExt=='.aof':
                        metawrapper(metadata,tokenized[i].split('=')[0],tokenized[i+1])
                    i=i+2
            else:
                i=i+1    
                

        
        if tokenized[0]=='reserved':
            continue
        if tokenized[0]=='use' and tokenized[1]=='name':
            continue
        if tokenized[0]=='use' and tokenized[1]=='comment':
            #NOTE: skipping the next two lines to be safe...
            #add to metadata.comment
            get_tokenized_line(myfile,returnline=returnline)
            if fileExt=='.aof':
                get_tokenized_line(myfile,returnline=returnline)
            continue
        
        # END TODO
        if tokenized[0]=='mode':
            if fileExt=='.aof':
                metadata['scantype'] = tokenized[1] # Mode
                metadata['arm'] = tokenized[3] # Arm
                metadata['npts'] = tokenized[5] # Npts
            continue
        
        if tokenized[0]=='monox':
            if fileExt=='.acf':
                #WARNING: if "[value]" has value large enough to take up space allotted between
                # the braces [], the indices will be incorrect!!!
                # Currently values have a space between "[" and first value. e.g. "[ 3.12345]#"
                metadata[tokenized[0].lower()] = tokenized[1]
                metadata[tokenized[5].lower()] = tokenized[6]
                metadata['analyzer_dspacing'] = tokenized[3].split(']')[0]  #dspace_monox
                metadata['monochromator_dspacing'] = tokenized[8].split(']')[0] #dspace_anax
            continue
            
        if tokenized[0].lower()=="#Date".lower():
            pass
        if returnline[0].find('=')<0 and not tokenized[0]=='point':
            for i in range(0, len(tokenized)-1, 2):             
                if tokenized[i] == 'date':
                    date_info = tokenized[i+1].split('-')
                    metadata['day'] = date_info[0]
                    metadata['month'] = date_info[1]
                    metadata['year'] = date_info[2]
                    metadata['start_time'] = tokenized[-1]
                else:
                    metadata[tokenized[i].lower()] = tokenized[i+1]
            
        #if metadata.has_key('run'):
        
                  
        if returnline[0].lower().find('point')>=0:
            columndict1={}; columnlist1=[]; columnlist2=[]; columndict2={}
            #if fileExt=='.aof':
            
            #TODO: employ translate_dict in get_column_meta_data to translate headers
            columndict1, columnlist1 = get_column_meta_data(tokenized, columndict1, columnlist1)
            tokenized = get_tokenized_line(myfile,returnline=returnline)
            columndict2, columnlist2 = get_column_meta_data(tokenized,columndict2,columnlist2)
                
            #elif fileExt=='.acf':
            #    columndict2,columnlist2=get_column_meta_data(tokenized,columndict2,columnlist2)

            if data.angles=={}:
                data.angles=copy.deepcopy(columndict1)
                data.pp=copy.deepcopy(columndict2)
                data.pm=copy.deepcopy(columndict2)
                data.mp=copy.deepcopy(columndict2)
                data.mm=copy.deepcopy(columndict2)
                
            #TODO: pickup testing here <---------------------------------------------
            #start reading points
            myFlag2=True
            currpoint=1
            prevpoint=None
            overshot=False  #to deal with when we've reached the next point...
            while myFlag2:
                if not overshot:
                    tokenized=get_tokenized_line(myfile,returnline=returnline)
                overshot=False
                if tokenized==[] or tokenized==None:
                    myFlag2=False
                    continue
                else:
                    if fileExt=='.aof':
                        #read in the angles
                        for i in range(len(columnlist1)):
                            field=columnlist1[i]
                            if not data.angles.has_key(field):
                                data.angles[field]=[]
                            data.angles[field].append(float(tokenized[i]))                                
                    currpoint=tokenized[0]
                    prevpoint=tokenized[0]
                    #read in polarized beam channels
                    if fileExt=='.acf':
                        print 'acf'                    
                    polarized_flag=True
                    while polarized_flag:
                        #read in the polarized beam data
                        tokenized=get_tokenized_line(myfile,returnline=returnline)
                        if tokenized==[] or tokenized==None:
                            break
                        currpoint=tokenized[0]
                        if currpoint==prevpoint:
                            if fileExt=='.acf':
                                print 'acf'
                            for i in range(len(columnlist2)):
                                field=columnlist2[i]
                                #DB SB
                                if float(tokenized[-2])==0 and float(tokenized[-1])==0:
                                    channel='pp'
                                if float(tokenized[-2])==0 and float(tokenized[-1])>0:
                                    channel='pm'
                                if float(tokenized[-2])>0 and float(tokenized[-1])==0:
                                    channel='mp'
                                if float(tokenized[-2])>0 and float(tokenized[-1])>0:
                                    channel='mm'
                                
                                datachannel=getattr(data,channel)  
                                if not datachannel.has_key(field):
                                    datachannel[field]=[]
                                datachannel[field].append(float(tokenized[i]))
                                    
                        else:
                            polarized_flag=False
                            overshot=True
                    
                    #read in the second polarized beam channel
                    #tokenized=get_tokenized_line(myfile,returnline=returnline)  
                    #for i in range(len(columnlist2)):
                    #    field=columnlist2[i]
                    #    data.pm[field].append(float(tokenized[i]))
                    ##print data.angles
                        
                    
            # FIX BELOW
            if len(data.angles['point'])==0:
                columndict={}
                columnlist=[]
                data.pp={}
                data.angles={}
                data.pm={}
                data.mm={}
                data.mp={}
                        #This is a drastic step, but if the file is empty, then no point in even recording the placeholders
                #print self.columndict['Qx']
                #print self.columnlist
                
    return data,metadata



            


def num2string(num):
        numstr=None
        if num<10:
                numstr='00'+str(num)
        elif (num>=10 & num <100):
                numstr='0'+str(num)
        elif (num>100):
                numstr=str(num)
        return numstr
    
    
def rearrange(source, primary, order=True):
    """
    given a source array and a list of primary values, put the primary values first and sort the remaining values
    alphabetically
    """
    #target=copy.copy(primary)
    target=[]
    #if not inserted:
    #    inserted=[]
    nsource=np.array(source)
    for val in source: 
        #pos=np.where(nsource==val)[0][0]
        #if pos>=0:
        if not val in primary:
            target.append(val)
    target.sort()
    target=np.concatenate((primary,target))
    return target.tolist()

def insert(source,idx,inserted):
    """
    inserts the inserted list into the source at position idx, inplace.
    """
    i=0
    for insertee in inserted:
        source.insert(idx+i,insertee)
        i=i+1
    return 


def readruns(aof_file, acf_file=None):
    """
    Reads data from a .aof file (and possibly a .acf file for polarized beam).
    Stores the data in format similar to that of other readers by producing a
    Data object.
    """
    
    ''' Do we need this?
    fileName, fileExt = os.path.splitext(myfilestr)
    fileName = fileName.lower()
    fileExt = fileExt.lower()
    '''
    
    myfilestr = aof_file
    mydata, metadata = readacf(myfilestr, run_range=[1,1])

    
    myfilestr = acf_file
    mydata,metadata=readacf(myfilestr, run_range=[1,1],data=mydata,metadata=metadata)
    
    channels=['pp','pm','mp','mm']
    keys=np.concatenate((metadata.keys(),mydata.angles.keys()))
    for channel in channels:
        print 'channel', channel
        keys=np.concatenate((keys,getattr(mydata,channel).keys()))
    keys=list(set(keys))
    
    #print keys
    inserted=['database id','sha1']
    primary=['run','point','sig','ihfa','ihfb','ihfc','dbhf','dbvf','sbvf','sbhf']
    new_keys=rearrange(keys,primary)
    insert(new_keys,1,inserted)
    
    #print new_keys
    output=[]
    output.append(new_keys)
    metadata['database id']=['id123']
    metadata['sha1']=['sha123']
    for key in metadata:
        metadata[key]=metadata[key]*len(mydata.angles['point'])
    maxvals=[]
    minvals=[]
    vals=[]
    channel='pp'
    
                                         
    for key in new_keys:
        currvals=[]
        if metadata.has_key(key):
            try:
                maxval=max(np.array(metadata[key],'Float64'))
            except:
                maxval='NaN'
            try:
                minval=min(np.array(metadata[key],'Float64'))
            except:
                minval='NaN'
            currvals.append(metadata[key])
        if mydata.angles.has_key(key):
            try:
                maxval=max(np.array(mydata.angles[key],'Float64'))
            except:
                maxval='NaN'
            try:
                minval=min(np.array(mydata.angles[key],'Float64'))
            except:
                minval='NaN'                     
            currvals.append(mydata.angles[key])
        dchannel=getattr(mydata,channel)
        if dchannel.has_key(key):
            try:
                minval=min(np.array(dchannel[key],'Float64'))
            except:
                minval='NaN'                
            currvals.append(dchannel[key])
        minvals.append(minval)
        maxvals.append(maxval)
        vals.append(currvals)
    output.append(maxvals)
    output.append(minvals)
    output.append(vals)
    
    return output
    


if __name__=='__main__':
    if 1:
        output = readruns(r'WRBFOB.AOF', r'WRBFOB.ACF')
        print output
