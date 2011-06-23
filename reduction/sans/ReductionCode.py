import numpy as N
from matplotlib import pyplot as plt
from data import readNCNRData
from data import readNCNRSensitivity
from uncertainty import Measurement

#globals
#global data 
#global metadata 
#global newdata 
global transSC
global transEM
global transCO

#Function not needed with adjusted format
def setFile(inputFile):
    #global data 
    #global metadata 
    #global newdata
    data,metadata = readNCNRData(inputFile)
    return data,metadata

def convertMonitor(data,metadata):
    #global data 
    #global metadata 
    #global newdata
    newdata = Measurement(data)
    mon = 1e8
    newdata = (data*metadata["run.moncnt"])/mon
    return newdata
   
def trans_s_c(transSCFile,transEMFile,transCOFile):
    global tramsSC,transEM,transCO
    tramsSC,metadataSC = readNCNRData(transSCFile)
    transEM,metadataEM = readNCNRData(transEMFile)
    transCO,metadataCO = readNCNRData(transCOFile)
    #Make them Measurements Here:
    
    
    
    #------------------------------
    tramsSC = convertMonitor(tramsSC,metadataSC)
    transEM = convertMonitor(transEM,metadataEM)
    transCO = convertMonitor(transCO,metadataCO)
    #Just Model, right now, need to add x/y coordinates
    transSC = sum(transSC) / sum(transEM)
    transCO = sum(transCO) / sum(transEM)

if __name__ == '__main__':
    
    data,metadata = setFile("MAY06001.SA3_CM_D545")
    newdata = convertMonitor()
    plt.figure()
    plt.imshow(newdata)
    plt.show()
    
    
    