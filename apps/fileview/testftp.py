from ftplib import FTP
from FTPfileclass import FTPfile
import sys


##need to think about how to do this recursion (probably first create some sort of 
## a straightforward python object and then convert it into json, rather than trying to
## make a json like string
ftp=FTP('ftp.ncnr.nist.gov')
ftp.login()
ftp.cwd('pub')		

id_counter=0;

def getChildren(directory):
	global id_counter
	ftp.cwd(directory)
	childList=[]
	for i in ftp.nlst():
		id_counter+=1
		childList.append(FTPfile(id_counter, directory+i,[], False))
	return childList


## trying without an actual list of files first (just using references)

root = FTPfile(id_counter,ftp.pwd(),[],False)
children=getChildren(root.path)
if children:
	root.setChildren(children)
else:
	root.isLeaf()
#print root
for i in root.children:
	print i.id, i
#print root.children
#print ftp.nlst()


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
