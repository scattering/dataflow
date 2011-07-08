from ftplib import FTP
from FTPfileclass import FTPfile
from django.utils import simplejson
import sys
import ast


##need to think about how to do this recursion (probably first create some sort of 
## a straightforward python object and then convert it into json, rather than trying to
## make a json like string
ftp=FTP('ftp.ncnr.nist.gov')
ftp.login()
ftp.cwd('pub')		

id_counter=0;

finalString = '['
error_log = open('errorLog.txt','w')
def getChildren(directory):
	global id_counter;
	error_log.write(directory)
	try: 
		ftp.cwd(directory)
	except Exception:
		pass
	childList=[]
	for i in ftp.nlst():
		id_counter+=1
		childList.append(FTPfile(id_counter, directory+'/'+i,[], False))
	return childList
	
def setupTree(file_object): #should just need to pass in root to this, and then
			    #the whole tree will be constructed
	for i in file_object.children:
		#print i.path
		children = getChildren(i.path)
		if children:
			i.setChildren(children)
			setupTree(i)
		else:
			i.isLeaf()
	
def toJson(file_object): #should just need to pass in root to this, and then
			 #the whole tree will be constructed
	global finalString;
	finalString += '{"id":%s,' %file_object.id
	finalString += '"text":"%s",' %file_object.path.split('/')[-1]
	if file_object.leaf:
		finalString += '"leaf":True},'
	else:
		finalString += '"children": ['
		for i in file_object.children:
			toJson(i)
		finalString += ']},'
		

def runMe():
	global finalString;
	root = FTPfile(id_counter,ftp.pwd(),[],False)
	children=getChildren(root.path)
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
	return ast.literal_eval(finalString)


#runMe()

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
