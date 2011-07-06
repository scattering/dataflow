import numpy as N
threshold=1e-6
class scanparser:
    def __init__(self,scanstr):
        self.scanstr=scanstr
        self.scan_description={}
    def parse_range(self,rangestr):
        #print rangestr
        prange={}
        npts=self.scan_description['npts']
        #print 'npts',npts
        range_split=rangestr.split('range=')
        #print 'range_split',range_split
        fields=range_split[1].split('=')
        #print fields
        field=fields[0]
        if field!='q':
            prange[field]={}
            toks=fields[1].split()
            if len(toks)==3:
                if toks[-1]=='s':
                    #print 'start stop'
                    prange[field]['start']=min(float(toks[0]),float(toks[1]))
                    prange[field]['stop']=max(float(toks[0]),float(toks[1]))
                    if npts>1:
                        prange[field]['step']=float(prange[field]['stop']-prange[field]['start'])/(npts-1)
                    else:
                        prange[field]['step']=float(0)
                elif toks[-1]=='i':
                    #print 'start increment'
                    start=float(toks[0])
                    step=float(toks[1])
                    stop=start+(npts-1)*step
                    prange[field]['step']=N.absolute(step)
                    prange[field]['start']=min(start,stop)
                    prange[field]['stop']=max(start,stop)

            else:
                #print 'center step'
                step=float(toks[1])
                center=float(toks[0])
                #print 'center',center
                start=center-float(step)*(npts-1)/2
                stop=center+float(step)*(npts-1)/2
                prange[field]['step']=N.absolute(step)
                prange[field]['start']=min(start,stop)
                prange[field]['stop']=max(start,stop)
        if 1:
            if fields[0]=='q':
                toks=fields[1].split()
                prange['qx']={}
                prange['qy']={}
                prange['qz']={}
                #print 'toks',toks
                if len(toks)==3:
                    if toks[-1]=='s':
                        #print 'start stop'
                        start=toks[0].split('~')
                        start=N.array(start).astype('Float64')
                        prange['qx']['start']=start[0]
                        prange['qy']['start']=start[1]
                        prange['qz']['start']=start[2]
                        stop=toks[1].split('~')
                        stop=N.array(stop).astype('Float64')
                        prange['qx']['stop']=stop[0]
                        prange['qy']['stop']=stop[1]
                        prange['qz']['stop']=stop[2]
                        if npts>1:
                            step=(stop-start)/(npts-1)
                            prange['qx']['step']=step[0]
                            prange['qy']['step']=step[1]
                            prange['qz']['step']=step[2]
                        else:
                            prange['qx']['step']=float(0)
                            prange['qy']['step']=float(0)
                            prange['qz']['step']=float(0)
                    elif toks[-1]=='i':
                        #print 'initial step'
                        start=toks[0].split('~')
                        start=N.array(start).astype('Float64')
                        step=toks[1].split('~')
                        step=N.array(step).astype('Float64')
                        stop=start+(npts-1)*step
                        prange['qx']['start']=start[0]
                        prange['qy']['start']=start[1]
                        prange['qz']['start']=start[2]
                        prange['qx']['step']=step[0]
                        prange['qy']['step']=step[1]
                        prange['qz']['step']=step[2]
                        prange['qx']['stop']=stop[0]
                        prange['qy']['stop']=stop[1]
                        prange['qz']['stop']=stop[2]
                else:
                    center=toks[0].split('~')
                    #print 'center step'
                    #print 'center',center
                    center=N.array(center).astype('Float64')
                    step=toks[1].split('~')
                    step=N.array(step).astype('Float64')
                    start=center-(npts-1)/2*step
                    stop=center+(npts-1)/2*step
                    prange['qx']['start']=start[0]
                    prange['qy']['start']=start[1]
                    prange['qz']['start']=start[2]
                    prange['qx']['step']=step[0]
                    prange['qy']['step']=step[1]
                    prange['qz']['step']=step[2]
                    prange['qx']['stop']=stop[0]
                    prange['qy']['stop']=stop[1]
                    prange['qz']['stop']=stop[2]


        #print 'Range', scan_description['range']
        return prange


    def parse_scan(self):
        scanstr=self.scanstr
        self.scan_description={}
        scan_description=self.scan_description
        scan_description['scan_string']=scanstr
        scan_description['range_strings']=[]

        toks=scanstr.split(':')
        try:
            if toks[0].lower()!='scan':
                raise BadScanError,'Not a Valid Scan'
            toks=toks[1:]
            for tok in toks:
                field=tok.split('=')
                #print 'field',field
                if field[0]=='':
                    return self.scan_description # for fpx scans can get a '::Title'  ack!!!!!!
                else:
                    key=field[0].lower()
                    value=field[1]
                    if key.lower()=='range':
                        scan_description['range_strings'].append(tok.lower())
                    else:
                        try:
                            scan_description[key]=float(value)
                        except ValueError:
                            scan_description[key]=value
            return self.scan_description
        except BadScanError:
            print 'Not a Valid Scan'
            self.scan_description={}
            return self.scan_description

    def get_varying(self):
        scan_description=self.scan_description
        scanstr_parsed=self.parse_scan()
        if self.scan_description=={}:
            self.ranges={}
            return self.ranges
        else:
            self.ranges={}
            self.varying=[]
            for range_string in scanstr_parsed['range_strings']:
                ranges=self.parse_range(range_string)
                #print 'ranges',ranges
                for key,value in ranges.iteritems():
                    self.ranges[key]=value
                    #print 'key',key,'value',value
                    if N.absolute(value['step'])>threshold:
                        self.varying.append(key)
            return self.varying

class BadScanError(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)

if  __name__=='__main__':
#find peak, A3-A4
    if 1:
        scanstr='Scan:Title=ICEFindPeak:Type=6:Fixed=0:FixedE=1:CountType=Time:Counts=2.0:Range=A4=50.0095 0.2:Npts=21:DetectorType=Detector:Filename=fpx:Range=A3=115.113 0.1::Title=FindPeak'
#inititial final h
    if 0:
        scanstr='Scan:SubID=13176:JType=VECTOR:Fixed=1:FixedE=13.6998911684:Npts=3:Counts=1.0:Prefac=1.0:DetectorType=Detector:CountType=Time:Filename=dumb:HoldScan=0.0:Range=Q=1.0~0.0~0.0 2.0~0.0~0.0 s:Range=E=0.0 0.0 s'
#initial step h
    if 0:
        scanstr='Scan:SubID=13176:JType=VECTOR:Fixed=1:FixedE=13.6998911684:Npts=3:Counts=1.0:Prefac=1.0:DetectorType=Detector:CountType=Time:Filename=dumb:HoldScan=0.0:Range=Q=1.0~0.0~0.0 2.0~0.0~0.0 i:Range=E=0.0 0.0 i'
#center step h
    if 0:
        scanstr='Scan:SubID=13176:JType=VECTOR:Fixed=1:FixedE=13.6998911684:Npts=3:Counts=1.0:Prefac=1.0:DetectorType=Detector:CountType=Time:Filename=dumb:HoldScan=0.0:Range=Q=1.0~0.0~0.0 2.0~0.0~0.0:Range=E=0.0 0.0'

#center step e [-1,0,1]
    if 0:
        scanstr='Scan:SubID=13176:JType=VECTOR:Fixed=1:FixedE=13.6998911684:Npts=3:Counts=1.0:Prefac=1.0:DetectorType=Detector:CountType=Monitor:Filename=dumb:HoldScan=0.0:Range=Q=0.0~0.0~0.0 0.0~0.0~0.0:Range=E=0.0 1.0'
#center step e [-.5,.5]
    if 0:
        scanstr='Scan:SubID=13176:JType=VECTOR:Fixed=1:FixedE=13.6998911684:Npts=2:Counts=1.0:Prefac=1.0:DetectorType=Detector:CountType=Monitor:Filename=dumb:HoldScan=0.0:Range=Q=0.0~0.0~0.0 0.0~0.0~0.0:Range=E=0.0 1.0'
#initial step e [0,1,2]
    if 0:
        scanstr='Scan:SubID=13176:JType=VECTOR:Fixed=1:FixedE=13.6998911684:Npts=3:Counts=1.0:Prefac=1.0:DetectorType=Detector:CountType=Monitor:Filename=dumb:HoldScan=0.0:Range=Q=0.0~0.0~0.0 0.0~0.0~0.0 i:Range=E=0.0 1.0 i'
#start stop e [0,.5,1]
    if 0:
        scanstr='Scan:SubID=13176:JType=VECTOR:Fixed=1:FixedE=13.6998911684:Npts=3:Counts=1.0:Prefac=1.0:DetectorType=Detector:CountType=Monitor:Filename=dumb:HoldScan=0.0:Range=Q=0.0~0.0~0.0 0.0~0.0~0.0 s:Range=E=0.0 1.0 s'
    myparser=scanparser(scanstr)
    #scanstr_parsed=myparser.parse_scan()
    #print myparser.parse_range(scanstr_parsed['range_strings'][0])
    print myparser.get_varying()
    print myparser.ranges