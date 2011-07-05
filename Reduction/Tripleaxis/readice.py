import numpy as N
#import pylab
import datetime,time
from time import mktime
#import mx.DateTime
import writebt7
import re
import scanparser
import os


months={'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}

def num2string(num):
        numstr=None
        if num<10:
                numstr='00'+str(num)
        elif (num>=10 & num <100):
                numstr='0'+str(num)
        elif (num>100):
                numstr=str(num)
        return numstr

def get_tokenized_line(myfile,returnline=['']):
        lineStr=myfile.readline()
        returnline[0]=lineStr.rstrip()
        strippedLine=lineStr.lower().rstrip()
        tokenized=strippedLine.split()

        return tokenized


                
class Orientation(object):
        def __init__(self,orient1=None,orient2=None):
                self.orient1=orient1
                self.orient2=orient2
        
class Lattice(object):
        def __init__(self,a,b,c,alpha,beta,gamma):
                self.a=a
                self.b=b
                self.c=c
                self.alpha=alpha
                self.beta=beta
                self.gamma=gamma


class MetaData(object):
        def __init__(self):
                pass
        
        
class Data(object):
        def __init__(self):
                pass
        def __getitem__(self, key): return self.__dict__[key]
        def __setitem__(self, key, item): self.__dict__[key] = item
        



class datareader(object):
        def __init__(self,myfilestr=None):
                self.myfilestr=myfilestr
                #define Data Abstraction Layer
                #self.data_abstraction_layer()
                self.metadata=MetaData()
                self.data=Data()
                return

        
        def get_columnmetadatas_bt7(self,tokenized):
                self.timestamp_flag=True
                self.columnlist=[]
                #originally set the timestamp flag to True, if it turns out that there is not timestamp in the file, then create one using the time field
                for field in tokenized:
                        if field=='QX':
                                field='Qx'.lower()
                        if field=='QY':
                                field='Qy'.lower()
                        if field=='QZ':
                                field='Qz'.lower()
                        if field=='T-act':
                                field='Temp'.lower()
                        if field=='#columns':
                                pass
                        else:
                                setattr(self.data,field,[])
                                self.columnlist.append(field)
                #In old bt7 files, there was no timestamp, so add one for those, otherwise use the one in the file
                if hasattr(self.data,'timestamp')==False:
                        self.timestamp_flag=False
                        setattr(self.data,'timestamp',[])
                        self.columnlist.append('timestamp')
                return

        def range_parser(self,rangestr,scan_description):
                #print rangestr
                range_split=rangestr.split('range=')
                fields=range_split[1].split('=')
                #print fields
                if fields[0]=='e':
                        toks=fields[1].split()
                        if len(toks)==3:
                                scan_description['range']['e']['start']=float(toks[0])
                                scan_description['range']['e']['stop']=float(toks[1])
                        else:
                                scan_description['range']['e']['center']=float(toks[0])
                                scan_description['range']['e']['step']=float(toks[1])

                if fields[0]=='q':
                        toks=fields[1].split()
                        #print 'toks',toks
                        if len(toks)==3:
                                start=toks[0].split('~')
                                scan_description['range']['q']['start']={}
                                scan_description['range']['q']['stop']={}
                                scan_description['range']['q']['start']['h']=float(start[0])
                                scan_description['range']['q']['start']['k']=float(start[1])
                                scan_description['range']['q']['start']['l']=float(start[2])
                                stop=toks[0].split('~')
                                scan_description['range']['q']['stop']['h']=float(stop[0])
                                scan_description['range']['q']['stop']['k']=float(stop[1])
                                scan_description['range']['q']['stop']['l']=float(stop[2])
                        else:
                                start=toks[0].split('~')
                                scan_description['range']['q']['center']={}
                                scan_description['range']['q']['step']={}
                                scan_description['range']['q']['center']['h']=float(start[0])
                                scan_description['range']['q']['center']['k']=float(start[1])
                                scan_description['range']['q']['center']['l']=float(start[2])
                                stop=toks[0].split('~')
                                scan_description['range']['q']['step']['h']=float(stop[0])
                                scan_description['range']['q']['step']['k']=float(stop[1])
                                scan_description['range']['q']['step']['l']=float(stop[2])

                #print 'Range', scan_description['range']
                return


        def parse_scan(self,scanstr):
                scan_description={}
                scan_description['scan_string']=scanstr
                scan_description['range']={}
                scan_description['range']['e']={}
                scan_description['range']['q']={}

                toks=scanstr.split(':')
                for i in range(1,len(toks)):
                        if toks[i][0]=='r':
                                self.range_parser(toks[i],scan_description)
                        else:
                                fields=toks[i].split('=')
                                try:
                                        scan_description[fields[0]]=float(fields[1])
                                except ValueError:
                                        scan_description[fields[0]]=(fields[1])
                return scan_description

        def readbt7(self,myfile):
        #get first line
                myFlag=True
                #self.metadata={}
                self.header=[]
                returnline=['']
                while myFlag:
                        tokenized=get_tokenized_line(myfile,returnline=returnline)
                        #print tokenized
                        if tokenized==[]:
                                tokenized=['']
                        if tokenized[0].lower()=="#Date".lower():
                                pass
                        elif tokenized[0].lower()=="#Date".lower():
                                #time.strptime("2007-11-03 22:33:22 EDT", "%Y-%m-%d %H:%M:%S %Z")
                                date_tokens=tokenized[1].split('-')
                                self.metadata['timestamp']={}
                                month=int(date_tokens[1].strip("\'"))
                                day=int(date_tokens[2].strip("\'"))
                                year=int(date_tokens[0].strip("\'"))
                                stime=tokenized[2].strip("\'")
                                stimetok=stime.split(':')
                                hour=int(stimetok[0])
                                minute=int(stimetok[1])
                                second=int(stimetok[2])
                                self.metadata['timestamp']['month']=int(date_tokens[1].strip("\'"))
                                self.metadata['timestamp']['day']=int(date_tokens[2].strip("\'"))
                                self.metadata['timestamp']['year']=int(date_tokens[0].strip("\'"))
                                self.metadata['timestamp']['time']=tokenized[2].strip("\'")
                        elif tokenized[0].lower()=="#Epoch".lower():
                                #timeobj=date.datatetime(year,month,day,hour,minute,second)
                                Epoch=float(tokenized[1])
                                #timeobj=mx.DateTime.DateTimeFromTicks(ticks=Epoch) #what I originally used
                                timeobj=datetime.datetime.fromtimestamp(Epoch)
                                #print 'timeobj ',timeobj
                                #print 'Epoch ', Epoch
                                self.metadata.epoch=Epoch#timeobj
                                #print self.metadata['timestamp']
                        elif tokenized[0].lower()=="#InstrName".lower():
                                self.metadata.instrument=tokenized[1].lower()
                        elif tokenized[0].lower()=="#ExptID".lower():
                                self.metadata.experiment_id=tokenized[1].lower()
                        elif tokenized[0].lower()=="#Fixed".lower():
                                self.metadata.fixed_devices=tokenized[1:]
                        elif tokenized[0].lower()=="#Filename".lower():
                                self.metadata.filename=tokenized[1]
                                #print 'filename ', tokenized[1]
                                pattern = re.compile('^(?P<base>[^.]*?)(?P<seq>[0-9]*)(?P<ext>[.].*)?$')
                                match = pattern.match(tokenized[1]+'.bt7')
                                dict((a,match.group(a)+"") for a in ['base','seq','ext'])
                                #print 'filebase ',match.group('base')
                                self.metadata.filebase=match.group('base')
                                self.metadata.fileseq_number=match.group('seq')
                        elif tokenized[0].lower()=="#Comment".lower():
                                mycomment=''
                                for i in range(1,len(tokenized)):
                                        mycomment=mycomment+' '+tokenized[i]
                                self.metadata.comment=mycomment
                        elif tokenized[0].lower()=="#MonoSpacing".lower():
                                self.metadata.monochromator_dspacing=float(tokenized[1])
                        elif tokenized[0].lower()=="#AnaSpacing".lower():
                                self.metadata.analyzer_dspacing=float(tokenized[1])
                        elif tokenized[0].lower()=="#TemperatureUnits".lower():
                                self.metadata.temperature_units=tokenized[1]
                        elif tokenized[0].lower()=="#Orient".lower():
                                h1=float(tokenized[1])
                                k1=float(tokenized[2])
                                l1=float(tokenized[3])
                                h2=float(tokenized[4])
                                k2=float(tokenized[5])
                                l2=float(tokenized[6])
                                self.metadata.orientation=Orientation([h1,k1,l1],[h2,k2,l2])
                        elif tokenized[0].lower()=="#Lattice".lower():
                                a=float(tokenized[1])
                                b=float(tokenized[2])
                                c=float(tokenized[3])
                                alpha=float(tokenized[4])
                                beta=float(tokenized[5])
                                gamma=float(tokenized[6])
                                self.metadata.lattice=Lattice(a,b,c,alpha,beta,gamma)
                        elif tokenized[0].lower()=="#AnalyzerDetectorMode".lower():
                                self.metadata.analyzerdetectormode=tokenized[2].lower()
                        elif tokenized[0].lower()=="#Reference".lower():
                                self.metadata.count_type=tokenized[2].lower()
                        elif tokenized[0].lower()=="#Signal".lower():
                                self.metadata.signal=tokenized[2].lower()
                        elif tokenized[0].lower()=="#AnalyzerDetectorDevicesOfInterest".lower():
                                self.metadata.analyzerdetectordevicesofinterest=tokenized[1:]
                        elif tokenized[0].lower()=="#AnalyzerDDGroup".lower():
                                self.metadata.analyzerddgroup=tokenized[1:]
                        elif tokenized[0].lower()=="#AnalyzerDoorDetectorGroup".lower():
                                self.metadata.analyzerdoordetectorgroup=tokenized[1:]
                        elif tokenized[0].lower()=="#AnalyzerSDGroup".lower():
                                self.metadata.analyzersdgroup=tokenized[1:]
                        elif tokenized[0].lower()=="#AnalyzerPSDGroup".lower():
                                self.metadata.analyzerpsdgroup=tokenized[1:]
                        elif tokenized[0].lower()=="#AnalyzerFocusMode".lower():
                                self.metadata.analyzerfocusmode=tokenized[1]
                        elif tokenized[0].lower()=="#MonoVertiFocus".lower():
                                self.metadata.monovertifocus=tokenized[1]
                        elif tokenized[0].lower()=="#MonoHorizFocus".lower():
                                self.metadata.monohorizfocus=tokenized[1]
                        elif tokenized[0].lower()=="#FixedE".lower():
                                try:
                                        self.metadata.efixed=tokenized[1]
                                except IndexError:
                                        pass
                                try:
                                        self.metadata.ef=float(tokenized[2])
                                except IndexError:
                                        pass
                        elif tokenized[0].lower()=="#ScanDescr".lower():
                                scanstr=''
                                for i in range(1,len(tokenized)):
                                        scanstr=scanstr+tokenized[i]+' '
                                self.metadata.scan_description=scanstr
                                #print 'scanstr',scanstr
                                myparser=scanparser.scanparser(scanstr)
                                self.metadata.varying=myparser.get_varying()
                                self.metadata.ranges=myparser.ranges
                                #print 'parsed'
                                #if self.metadata['file_info']['filebase']!='fpx':
                                #    self.additional_metadata['parsed_scandescription']=self.parse_scan(scanstr)

                                        #CAN'T SEEM TO PARSE fpx files, but if the filename is broken as in the last cycle, then how do I know?
                                        #Better soln is to fix parser
                                #print self.metadata['scan_description']['range']
                        else:
                                currfield=tokenized[0].lower().lower().strip('#')
                                setattr(self.metadata,currfield,tokenized[1:])
                        if tokenized[0]!='#Columns'.lower():
                                self.header.append(returnline[0])
                        if tokenized[0]=='#Columns'.lower():
                                self.get_columnmetadatas_bt7(tokenized)
                                count =  0
                                try:
                                        lines=int(self.lines)
                                except:
                                        lines=N.Inf
                                while 1:
                                        lineStr = myfile.readline()
                                        if not(lineStr):
                                                break
                                        if lineStr[0] != "#":
                                                if count>=lines:
                                                        break
                                                strippedLine=lineStr.rstrip()
                                                tokenized=strippedLine.split()
                                                #for field in self.data.__dict__.keys():
                                                for i in range(len(tokenized)):
                                                        field=self.columnlist[i]
                                                        try:
                                                                if field.lower()=='time' and self.timestamp_flag==False:
                                                                        #timedelta=mx.DateTime.DateTimeDelta(0,0,0,float(tokenized[i])) #orig
                                                                        #self.columndict['timestamp'].append((timeobj+timedelta).ticks()) #orig
                                                                        #timestamp_flag is True if the timestamp is already given in the file
                                                                        timedelta=datetime.timedelta(seconds=float(tokenized[i]))
                                                                        self.data.timestamp.append(mktime((timeobj+timedelta).timetuple()))
                                                                        timeobj=timeobj+timedelta
                                                                self.data[field].append(float(tokenized[i]))
                                                        except ValueError:
                                                                self.data[field].append((tokenized[i]))
                                                count=count+1
                                myFlag=False
                return

        def numpyize(self):
                for field in self.data.__dict__.keys():
                        if type(self.data[field][0])==type(float):
                                self.data[field]=N.array(self.data[field],'Float64')
                        else:
                                self.data[field]=N.array(self.data[field])

        def readbuffer(self,myfilestr,lines=N.Inf):
                self.myfilestr=myfilestr
                self.lines=lines
                myfile = open(myfilestr, 'r')
                self.instrument=os.path.splitext(myfilestr)[-1]
                if self.instrument in ['.bt7']:
                        #instrument is bt7
                        self.readbt7(myfile)
                        #self.readbt7columns(myfile)
                        myfile.close()
                        if self.header==None:
                                self.header=[]
                        mydata=DataSet(self.data,self.metadata,self.header)
                        #repair ice files with missing file names
                        if hasattr(self.metadata,'filename')==False:
                                filename=os.path.split(myfilestr)[-1]
                                self.metadata['file_info']['filename']=filename
                                #print 'filename ', tokenized[1]
                                pattern = re.compile('^(?P<base>[^.]*?)(?P<seq>[0-9]*)(?P<ext>[.].*)?$')
                                match = pattern.match(filename)
                                dict((a,match.group(a)+"") for a in ['base','seq','ext'])
                                #print 'filebase ',match.group('base')
                                self.metadata.filebase=match.group('base')
                                self.metadata.fileseq_number=match.group('seq')
                        self.numpyize()
                        mydata=DataSet(self.data,self.metadata,self.header) 
                return mydata


class DataSet(object):
        def __init__(self,data,metadata,header):
                self.metadata=metadata
                self.header=header
                self.data=data





if __name__=='__main__':

        if 0:
                #ibuff
                myfilestr=r'c:\summerschool2007\\qCdCr014.ng5'
        if 1:
                #myfilestr=r'c:\bifeo3xtal\jan8_2008\9175\meshbefieldneg1p3plusminus53470.bt7'
                #myfilestr=r'c:\12436\data\LaOFeAs56413.bt7'
                myfilestr=r'c:\bifeo3xtal\jan8_2008\9175\mesh53439.bt7'
                #myfilestr=r'c:\bifeo3xtal\jan8_2008\9175\fpx53418.bt7'
                #myfilestr=r'c:\13165\13165\data\MagHigh56784.bt7'
                #myfilestr=r'c:\13176\data\CeOFeAs57255.bt7.out'
                mydatareader=datareader()
                #mydata=mydatareader.readbuffer(myfilestr,lines=91)
                mydata=mydatareader.readbuffer(myfilestr)
                #myoutfilestr=r'c:\bifeo3xtal\jan8_2008\9175\meshbefieldneg1p3plusminus53470.bt7.out'
                #mywriter=writebt7.datawriter()
                #mywriter.write(myoutfilestr=myoutfilestr,mydata=mydata)
                print mydata.data.timestamp
                #print mydata.data['magfield']
                #print mydata.data.keys()
                print 'done'
                print mydata.metadata.varying
                #mydataout=mydata=mydatareader.readbuffer(myoutfilestr,lines=91)
                #print N.array(mydata.data['qy'])-N.array(mydataout.data['qy'])
                #print len(mydata.data['timestamp'])
                #print mydata.data['Qy']
                #print mydata.data

        if 0:
                mydatareader=datareader()
                mydata=mydatareader.readbuffer(myfilestr,lines=91)

 


