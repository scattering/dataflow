from ftplib import FTP
import sys



ftp=FTP('ftp.ncnr.nist.gov')
ftp.login()
ftp.cwd('pub')
ftp.cwd('ncnrdata')
ftp.cwd('bt7')
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
