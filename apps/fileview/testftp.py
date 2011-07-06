from ftplib import FTP
import sys


##need to think about how to do this recursion (probably first create some sort of 
## a straightforward python object and then convert it into json, rather than trying to
## make a json like string
ftp=FTP('ftp.ncnr.nist.gov')
ftp.login()
directory_structure = '['
def getChildren(curr_dir): 
	ftp.cwd(curr_dir)
	for i in ftp.dir():
		ftp.cwd(i)
		if ftp.dir():
			directory_structure += '{"text":"%(nam)s","id":"%(path)s","children":['
		else:
			directory_structure += '
			
	
	
print ftp.pwd()
ftp.cwd('pub')

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
