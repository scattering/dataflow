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

def read_file():

ftp.retrlines('RETR' + filey, read_file)
#open(filey,'r')
