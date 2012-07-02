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
    #translate_dict['database id'] = 
    #translate_dict['sha1'] = 
    #translate_dict['point'] = 
    translate_dict['sig'] = 'detector' # signal counts

    #translate_dict['dbhf'] = 'diffracted_beam_horizontal_field'
    #translate_dict['dbvf'] = 'diffracted_beam_vertical_field'
    #translate_dict['sbvf'] = 'scattering_beam_vertical_field'
    #translate_dict['sbhf'] = 'scattering_beam_horizontal_field'

    translate_dict['2tm'] = 'a2' # two theta monochromator
    translate_dict['psi'] = 'a3' # theta sample 
    translate_dict['phi'] = 'a4' # two theta sample
    translate_dict['2ta'] = 'a6' # two theta analyzer
    #translate_dict['a'] = 
    #translate_dict['anax'] = 
    translate_dict['arm'] = 'arm'    
    
    #translate_dict['ctemp']
    #translate_dict['date']
    translate_dict['db'] = 'monitor'
    translate_dict['det'] = 'eta_step'
    translate_dict['dze'] = 'zeta_step'
    translate_dict['dnu'] = 'energy_step'
    #translate_dict['dspace_anax'] = 'analyzer_dspacing' #hardcoding in this name already
    #translate_dict['dspace_monox'] = 'monochromator_dspacing' #hardcoding in this name already
    translate_dict['eprim'] = 'e' #Energy of the incident beam (THz)--> should convert to meV
    
    translate_dict['eta'] = 'eta'
    translate_dict['zeta'] = 'zeta'        
    translate_dict['etm'] = 'eta_scan_center'
    translate_dict['zem'] = 'zeta_scan_center'
    
    #translate_dict['field']
    #translate_dict['file']
    #translate_dict['hhconst']
    #translate_dict['hhihf']
    #translate_dict['ihfa'] = 'current_horizontal_coil_a'
    #translate_dict['ihfb'] = 'current_horizontal_coil_b'
    #translate_dict['ihfc'] = 'current_horizontal_coil_c'
    #translate_dict['ivfb'] = 'current_vertical_coil_bottom' 
    #translate_dict['ivft'] = 'current_vertical_coil_top' 
    
    #translate_dict['kprim'] 
    translate_dict['mfield'] = 'magnetic_field'
    translate_dict['mode'] = 'scan_type'
    #translate_dict['monox']
    #translate_dict['npts']
    #translate_dict['nu']
    #translate_dict['num']
    

    #translate_dict['r']
    #translate_dict['rbc']
    #translate_dict['rec']
    #translate_dict['rtemp']
    
    #translate_dict['seq']
    translate_dict['stemp'] = 'temp'
    #translate_dict['time']

def translate_fields(metadata, data):
    """
    given dictionaries of metadata and data, translates the keys based on
    the translate_dict to give them the name used in data_abstraciton's
    TripleAxis object translations.
    """
    if translate_dict == {}:
        construct_translate_dict()
    for key in translate_dict.keys():
        if metadata.has_key(key):
            metadata[translate_dict[key]] = metadata[key]
            del metadata[key]
        if data.has_key(key):
            data[translate_dict[key]] = data[key]
            del data[key]
    

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
        '''
        self.pp={}
        self.pm={}
        self.mm={}
        self.mp={}
        self.angles={}
        '''


def get_column_headings(tokenized):
    """
    Appends the headers in tokenized as keys in the data dictionary
    """
    columns = []
    for i in np.arange(len(tokenized)):
        field = tokenized[i].lower()
        if field == 'mon=':
            continue
        if field =='sig=':
            continue
        #if not data.has_key(field):
        #    data[field] = []
        columns.append(field)
    return columns

def metawrapper(metadata,key,value):
    if metadata.has_key(key):
        metadata[key].append(value)
    else:
        metadata[key]=[]
        metadata[key].append(value)

def readacf(myfilestr, orient1, orient2, preread_data_list):
    """
    Reads in a .acf file. See readaof(...). Requires a .aof file to be read in first,
    hence required preread_data_list.
    """
    return readaof(myfilestr, orient1, orient2, preread_data_list=preread_data_list)

def readaof(myfilestr, orient1, orient2, preread_data_list=None):
    """
    Reads data from a chalk river .acf or .aof file.
    Returns data_list, a list of dictionaries: [metadata, data]
    
    myfilestr --> provided .aof or .acf file
    orient1 --> first basis vector (list/array/tuple) with [h,k,l] indices
    orient2 --> second basis vector (list/array/tuple) with [h,k,l] indices
    preread_data_list --> if readaof was previously called on a file, its data 
                          can be passed back in here and myfilestr's data will
                          be appended to it. (e.g. load a .aof then a .acf)
    """    
    myfile = open(myfilestr,'r')
    fileName, fileExt = os.path.splitext(os.path.basename(myfilestr))
    fileExt = fileExt.lower()
    
    myFlag=True
    data_list = [] # list of lists of [metadata, data] for each run to be translated  
                   # into Data objects then intoTripleAxis objects
    #point_lines = 0
    #curr_run = 0
    
    data={}
    metadata={}

    # myFlag is going to always be true unless we rewrite to specify a # of reads
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
                        label = tokenized[i].split('=')[0]
                        metadata[label] = tokenized[i+1]
                        #metawrapper(metadata,tokenized[i].split('=')[0],tokenized[i+1])
                    i=i+2
            else:
                i=i+1
                

        
        if tokenized[0]=='reserved':
            continue
        if tokenized[0]=='use' and tokenized[1]=='name':
            continue
        if tokenized[0]=='use' and tokenized[1]=='comment':
            #NOTE: skipping the next two lines to be safe...
            #find a way to isolate the comment and add to metadata['comment']
            #I would imagine that 'use comment...' would be replaced...
            get_tokenized_line(myfile,returnline=returnline)
            if fileExt=='.aof':
                get_tokenized_line(myfile,returnline=returnline)
            continue
        # TODO END
        
        if tokenized[0]=='mode':
            if fileExt=='.aof':
                metadata['scantype'] = tokenized[1] # Mode
                metadata['arm'] = tokenized[3] # Arm
                metadata['npts'] = tokenized[5] # Npts
            continue
        
        if tokenized[0]=='monox':
            if fileExt=='.aof':
                #WARNING: if "[value]" has value large enough to take up space allotted between
                # the braces [], the indices will be incorrect!!!
                # Currently values have a space between "[" and first value. e.g. "[ 3.12345]#"
                metadata[tokenized[0].lower()] = tokenized[1]
                metadata[tokenized[5].lower()] = tokenized[6]
                metadata['monochromator_dspacing'] = tokenized[3].split(']')[0]  #dspace_monox
                metadata['analyzer_dspacing'] = tokenized[8].split(']')[0] #dspace_anax
            continue
            
        # For the first line in a run
        if returnline[0].find('=')<0 and not tokenized[0]=='point':
            for i in range(0, len(tokenized)-1, 2):
                field = tokenized[i].lower()
                if field == 'run':
                    if fileExt == '.acf':
                        # load in preivous .aof data_list
                        run_num = int(tokenized[i + 1])
                        metadata = preread_data_list[run_num - 1][0]
                        data = preread_data_list[run_num - 1][1] 
                    else:
                        data={}
                        metadata={}
                        filestring = fileName + "_run" + repr(int(tokenized[i+1])) # creating filename - still need to append channel
                        metadata['temperature_units'] = 'K' # setting temperature to Kelvin by default.
                        metadata['orient1'] = {'h': orient1[0], 'k': orient1[1], 'l': orient1[2]}
                        metadata['orient2'] = {'h': orient2[0], 'k': orient2[1], 'l': orient2[2]}
                        metadata[field] = int(tokenized[i+1])
                elif field == 'date':
                    date_info = tokenized[i+1].split('-')
                    metadata['day'] = date_info[0]
                    metadata['month'] = date_info[1]
                    metadata['year'] = date_info[2]
                    metadata['start_time'] = tokenized[-1]
                else:
                    metadata[field] = tokenized[i+1]
           
        if returnline[0].lower().find('point')>=0:
            if fileExt == '.aof': # .aof files have two lines of headers
                first_headers = get_column_headings(tokenized)
                tokenized = get_tokenized_line(myfile,returnline=returnline)
                
            # both .aof and .acf files have the "second" header line
            second_headers = get_column_headings(tokenized)
            
            #start reading points
            myFlag2 = True
            currpoint = 1
            prevpoint = None
            overshot = False  #to deal with when we've reached the next point...
            
            #loop through all data points in the run
            while myFlag2:
                if not overshot:
                    tokenized = get_tokenized_line(myfile,returnline=returnline)
                overshot=False
                if tokenized==[] or tokenized==None: # at end of this data run; break 
                    myFlag2=False
                    #continue
                    break 
                else:
                    # read in polarized beam channels
                    # only .aof files will have (first_headers)
                    if fileExt == '.aof':
                        for i in range(len(first_headers)):
                            field = first_headers[i]
                            if data.has_key(field):
                                data[field].append(float(tokenized[i]))
                            else:
                                data[field] = [float(tokenized[i])]
                    
                    currpoint = tokenized[0]
                    prevpoint = tokenized[0]
                    polarized_flag = True
                    
                    # if data is on one line, this loop should always go ONE time only
                    while polarized_flag:
                        tokenized = get_tokenized_line(myfile, returnline=returnline)
                        if tokenized == [] or tokenized == None:
                            break
                        
                        currpoint = tokenized[0]
                        
                        if currpoint == prevpoint:
                            if int(currpoint) == 1:
                                #first time through, determine channel
                                #WARNING: assumes that the channel will NOT change during a run
                                '''
                                #NOT USED --> .aof file missing dbvf and sbvf
                                if fileExt == '.aof':
                                    # .aof code to check tokenized[-2 through -1]: dbhf, sbhf
                                    dbhf = float(tokenized[-2])
                                    sbhf = float(tokenized[-1])
                                    if dbhf == 0 and sbhf == 0:
                                        channel = 'pp'
                                    elif dbhf == 0 and sbhf > 0:
                                        channel = 'pm'
                                    elif dbhf > 0 and sbhf == 0:
                                        channel = 'mp'
                                    elif dbhf > 0 and sbhf > 0:
                                        channel = 'mm'
                                  '''                                
                                if fileExt == '.acf':
                                    # .acf code to check tokenized[1 through 4]: DBHF, DBVF, SBHF, SBVF
                                    is_db_mfield_on = (float(tokenized[1]) or float(tokenized[2]))
                                    is_sb_mfield_on = (float(tokenized[3]) or float(tokenized[4]))
                                    
                                    if not is_db_mfield_on and not is_sb_mfield_on:
                                        channel = 'pp'
                                    elif not is_db_mfield_on and is_sb_mfield_on:
                                        channel = 'pm'
                                    elif is_db_mfield_on and not is_sb_mfield_on:
                                        channel = 'mp'
                                    elif is_db_mfield_on and is_sb_mfield_on:
                                        channel = 'mm'
                                        
                                    filestring += "_" + channel # completing the filename
                                metadata['filename'] = filestring                                

                            for i in range(len(second_headers)):
                                field = second_headers[i]
                                if not (i == 1 and  i == 3 and fileExt == '.acf'):
                                    # don't recopy dbhf (i=1) and sbhf (i=3) --> already there from .aof
                                    try:
                                        data[field].append(float(tokenized[i]))
                                    except:
                                        data[field] = [float(tokenized[i])]

                                            
                        else:
                            polarized_flag=False
                            overshot=True

                #currpoint = tokenized[0]
                #prevpoint = tokenized[0]                    
            
        data_list.append([metadata, data])
            
    return data_list



            


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
    target=[]
    nsource=np.array(source)
    for val in source: 
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


def readruns(aof_file, orient1, orient2, acf_file=None):
    """
    Reads data from a .aof file (and possibly a .acf file for polarized beam).
    Stores the data in format similar to that of other readers by producing a
    Data object.
    """

    myfilestr = aof_file
    data_list = readaof(myfilestr, orient1, orient2)
    
    if acf_file:
        myfilestr = acf_file
        data_list = readaof(myfilestr, orient1, orient2, preread_data_list=data_list)
    
    #metadata['sha1']=['sha123']

    mydata = []
    for i in range(len(data_list)):
        translate_fields(data_list[i][0], data_list[i][1])
        mydata.append(Data(data_list[i][0], data_list[i][1]))
    
    return mydata
    


if __name__=='__main__':
    if 1:
        output = readruns(r'chalk_data/WRBFOB.AOF', r'chalk_data/WRBFOB.ACF')
        print output
