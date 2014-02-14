import ast
import tempfile
from ftplib import FTP

from django.utils import simplejson

from apps.fileview.FTPfileclass import FTPfile

##need to think about how to do this recursion (probably first create some sort of 
## a straightforward python object and then convert it into json, rather than trying to
## make a json like string
#ftp=FTP('ftp.ncnr.nist.gov')
#ftp.login()
#ftp.cwd('pub')		

id_counter = 0
ftp = None #default initialization. ftp initialized in runMe()

finalString = '['

def getChildren(directory):
    global id_counter;
    
    try: 
        ftp.cwd(directory)
    except Exception:
        pass
    
    if directory == '/':
        #if the directory is the root, set it to nothing so two '/' are not appended
        directory = ''
        
    childList=[]
    data = []
    ftp.dir(data.append)
    for i in data:
        name = i.split()[-1]
        if i.lower().startswith('d'):
            childList.append(FTPfile(id_counter, directory+'/'+name,[], False))
        else:
            childList.append(FTPfile(id_counter, directory+'/'+name,[], True))
            
    '''for i in ftp.nlst():
        id_counter+=1
        childList.append(FTPfile(id_counter, directory+'/'+i,[], False))
    '''
    return childList

def setupTree(rootnode):
    """
    Given the root, constructs a full tree using depth-first recursion
    """
    children = getChildren(rootnode.path)
    if children:
        rootnode.setChildren(children)
        setupTreeAux(rootnode)
    else:
        rootnode.isLeaf()

def setupTreeAux(file_object): 
    for i in file_object.children:
        children = getChildren(i.path)
        if children:
            i.setChildren(children)
            setupTree(i)
        else:
            i.isLeaf()

def toJson(file_object, isexpanded=False): 
    """
    pass the node as ``file_object`` and whether it should be expanded
    as a directory as ``isexpanded``. Will not expand by default. 
    
    NOTE: ``isexpanded`` will only be set true if file_object is a directory
    """
    global finalString;
    finalString += '{"id":%s,' %file_object.id
    finalString += '"text":"%s",' %file_object.path.split('/')[-1]
    finalString += '"path":"%s",' %file_object.path
    if file_object.leaf:
        finalString += '"leaf":True},'
    else:
        if isexpanded:
            finalString += '"expanded":True,'
        finalString += '"children": ['
        for i in file_object.children:
            toJson(i) # does not expand children directories.
        finalString += ']},'

def getFiles(address, filepaths, username='', password=''):
    """
    Fetches a set of binary files whose paths are given by ``filepaths``.
    Returns: a dictionary ``file_descriptors`` where each element has:
             'filename': path to file
             'friendly_name': file's friendly name
             NOTE: this is the current setup used to upload files. 8/17/2012
    """
    ftp = FTP(address)
    ftp.login(user=username, passwd=password)
    file_descriptors = []
    for filepath in filepaths:
        tmp_file, tmp_path = tempfile.mkstemp()
        outfile = open(tmp_path, 'wb') #.write(file_contents)
        ftp.retrbinary("RETR " + filepath, outfile.write)
        dirs = filepath.split('/')
        if len(dirs[-1]) > 0:
            fname = dirs[-1]
        else:
            fname = dirs[-2]
        file_descriptors.append({'filename': tmp_path, 'friendly_name': fname})
    ftp.quit()
    return file_descriptors



def runFTP(address, directory,  username='', password=''):
    """
    FTP into a given ``address`` and change into the directory ``directory``.
    This will provide the set of files and directories within ``directory``.
    """
    global finalString;
    global ftp;
    
    finalString = '['
    ftp = FTP(address)
    ftp.login(user=username, passwd=password)
    ftp.cwd(directory)
    
    root = FTPfile(id_counter, ftp.pwd(), [], False)
    
    children = getChildren(root.path)
    if children:
        root.setChildren(children)
    else:
        root.isLeaf() #sets root as a leaf
    
    ftp.quit()
    toJson(root, isexpanded=True)
    finalString += ']'
    return ast.literal_eval(finalString)


def runFullRecursionFTP(address):
    """
    FTP into a given ``address`` and gets the full directory structure
    NOTE: for larger trees, setupTree will usually time-out.
    """
    global finalString;
    global ftp;
    
    finalString = '['
    ftp = FTP(address)
    ftp.login()
    
    root = FTPfile(id_counter, ftp.pwd(), [], False)
    
    setupTree(root) #full depth-first recursion takes too long
    
    ftp.quit()
    toJson(root)
    finalString += ']'
    return ast.literal_eval(finalString)

#Old method; Not being used currently 8/17/2012
def runMe():
    global finalString;
    global ftp;
    
    finalString = '['
    ftp=FTP('ftp.ncnr.nist.gov')
    ftp.login()
    ftp.cwd('pub')
    
    root = FTPfile(id_counter,ftp.pwd(),[],False)
    children = getChildren(root.path)

    ftp.quit()

    if children:
        root.setChildren(children)
    else:
        root.isLeaf() #isLeaf sets to leaf
    #print root
    #for i in root.children:
    #	print i.id, i
    #print root.children
    #print ftp.nlst()
    #setupTree(root)
    toJson(root)
    finalString += ']'
    #write=open('ftpDir.txt','w')
    #write.write(finalString)
    #write.close()
    #print finalString
    #return finalString
    return ast.literal_eval(finalString)


if 0:
    test = runFTP('ncnr.nist.gov', 'pub/')
    print test

while 0:
    ftp.cwd('ncnrdata')
    ftp.cwd('bt7')
    print ftp.pwd()
    ftp.cwd('/pub/ncnrdata/bt7')
    ftp.cwd(ftp.nlst()[0])
    ftp.cwd(ftp.nlst()[1]) # Looking at user1's files

    filey = ftp.nlst()[0]
    ftp.retrlines('LIST')

    file_to_write = open('file_receptacle','w')
    def write_line_to_file(line):
        file_to_write.write(line)
        print 'processing...'


    ftp.retrlines('RETR ' + filey, write_line_to_file)

    file_to_write.close()
#open(filey,'r')