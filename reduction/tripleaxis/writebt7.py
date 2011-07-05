class datawriter:
    def __init__(self,mydata=None,myoutfilestr=None):
        self.mydata=mydata
        self.myoutfilestr=myoutfilestr
        #print 'called with ',myoutfilestr,' self ',self.myoutfilestr
        return

    def write(self,mydata=None,myoutfilestr=None):
#        myoutfilestr=r'c:\bifeo3xtal\jan8_2008\9175\meshbefieldneg1p3plusminus53470.bt7.out'
        if mydata==None:
            mydata=self.mydata
        if myoutfilestr==None:
            myoutfilestr=self.myoutfilestr
        #print 'called with ',myoutfilestr,' self ',self.myoutfilestr
        count=1
        #mydata.additional_metadata['parsed_scandescription'] #TODO choose correct field based on this
        for key in mydata.data.keys():
            if key=='detector_corrected':
                detectorpos=count
                #print 'detectorpos ',detectorpos
            #print 'writing key',key,'varying',mydata.metadata['count_info']['varying']
            if key==mydata.metadata['count_info']['varying'][0]:
                scanpos=count
            count=count+1
        myoutfile=open(myoutfilestr,'wt')
        for i in range(len(mydata.header)):
            s=mydata.header[i]+'\n'
            tokenized=s.rstrip().lower().split()
            if tokenized[0]=='#signal'.lower():
                s='#signal'+' '+str(detectorpos)+' '+'detector\n'
            if tokenized[0]=='#scan'.lower():
                s='#scan'+' '+str(scanpos)+' '+mydata.metadata['count_info']['varying'][0]+'\n'




            myoutfile.write(s.lower())
        s='#Columns '
        for key in mydata.data.keys():
            s=s+key+' '
        s=s+'\n'
        myoutfile.write(s)
        s=''
        #print 'writing'
        #print 'write key ',key,' len ',len(mydata.data[key])
        for i in range(len(mydata.data[key])):
            #s=s+' '+str(i)+' '
            for ckey in mydata.data:
                s=s+str(mydata.data[ckey][i])+' '
            s=s+'\n'
            #print i
            myoutfile.write(s)
            s=''
        myoutfile.close()
