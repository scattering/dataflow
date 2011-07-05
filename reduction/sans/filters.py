#!/usr/bin/env python

import struct
import sys,os
import vaxutils
import data
from copy import deepcopy,copy
import numpy as np
from numpy import array
import math
from matplotlib import pyplot as plt
from uncertainty import Measurement
import json
from draw_annulus_aa import annular_mask_antialiased
import datetime as date
import time 
#I will have a general philosophy that filters do not have side effects. That is,
#they do not change the state of their inputs. So, we will always work on copies
#internally

#TODO:
# Add copy statements and deepcopy statement (for dictionaries) where appropriate. The deepcopy on the dictionary is
# becaue if the value is a list, a simple copy will still reference the original list. Thus, we are not as decoupled as we would like to be.

# Create __div__, __truediv__, etc. methods so we only have to do the above in one place
# Make a constants.py in sans from where we import constants related to the sans instrument
# for example, pixel_size_x_cm, pixel_size_y_cm
#Capital letters will denote constants
#put into wire-it framework
#write tests
#
#Ask Steve Kline where they use attenuation outside of absolute scaling
#implement two absolute scaling methods
#implement annular average
#implement conversion to q
#implement line cut
#ask andrew about reading mask files

PIXEL_SIZE_X_CM=.508
PIXEL_SIZE_Y_CM=.508

class SansData(object):
    def __init__(self,data=None,metadata=None,q=None,qx=None,qy=None,theta=None):
        self.data=Measurement(data,data)
        self.metadata=metadata
        self.q=q #There are many places where q was not set, i think i fixed most, but there might be more; be wary
        self.qx=qx
        self.qy=qy
        self.theta=theta
    # Note that I have not defined an inplace subtraction
    def __sub__(self,other):
        if isinstance(other,SansData):
            return SansData(self.data-other.data,deepcopy(self.metadata),q=copy(self.qx),qx=copy(self.qx),qy=copy(self.qy),theta=copy(self.theta))
        else:
            return SansData(data=self.data-other,metadata=deepcopy(self.metadata),q=copy(self.qx),qx=copy(self.qx),qy=copy(self.qy),theta=copy(self.theta))
    #Actual subtraction
    def __sub1__(self,other):
        if isinstance(other,SansData):
            return SansData(self.data.x-other.data.x,deepcopy(self.metadata),q=copy(self.qx),qx=copy(self.qx),qy=copy(self.qy),theta=copy(self.theta))
        else:
            return SansData(data=self.data.x-other.data.x,metadata=deepcopy(self.metadata),q=copy(self.qx),qx=copy(self.qx),qy=copy(self.qy),theta=copy(self.theta))
    def __add__(self,other):
        if isinstance(other,SansData):
            return SansData(self.data.x+other.data.x,deepcopy(self.metadata),q=copy(self.qx),qx=copy(self.qx),qy=copy(self.qy),theta=copy(self.theta))
        else:
            return SansData(data=self.data.x+other.data.x,metadata=deepcopy(self.metadata),q=copy(self.qx),qx=copy(self.qx),qy=copy(self.qy),theta=copy(self.theta))
    def __rsub__(self, other):
        return SansData(data=other-self.data, metadata=deepcopy(self.metadata),q=copy(self.qx),qx=copy(self.qx),qy=copy(self.qy),theta=copy(self.theta))
    def __truediv__(self,other):
        if isinstance(other,SansData):
            return SansData(Measurement(*err1d.div(self.data.x,self.data.variance,other.data.x,other.data.variance)).x,deepcopy(self.metadata),q=copy(self.qx),qx=copy(self.qx),qy=copy(self.qy),theta=copy(self.theta))
        else:
            return SansData(data=Measurement(self.data.x/other, self.data.variance/other**2).x,metadata=deepcopy(self.metadata),q=copy(self.qx),qx=copy(self.qx),qy=copy(self.qy),theta=copy(self.theta))
    def __mul__(self,other):
        if isinstance(other,SansData):
            return SansData(Measurement(*err1d.mul(self.data.x,self.data.variance,other.data.x,other.data.variance)).x,deepcopy(self.metadata),q=copy(self.qx),qx=copy(self.qx),qy=copy(self.qy),theta=copy(self.theta))
        else:
            return SansData(data = self.data.__mul__(other).x,metadata=deepcopy(self.metadata),q=copy(self.qx),qx=copy(self.qx),qy=copy(self.qy),theta=copy(self.theta))
    #def __str__(self):
        #return self.data.x.__str__()
    #def __repr__(self):
        #return self.__str__()
        
def read_sample(myfilestr="MAY06001.SA3_CM_D545"):
    """Reads in a raw SANS datafile and returns a SansData
"""
    detdata,meta=data.readNCNRData(myfilestr) #note that it should be None for the default

    return SansData(data = detdata, metadata = meta)

def read_div(myfilestr="test.div"):
    sensitivity = data.readNCNRSensitivity(myfilestr)
    return sensitivity

def monitor_normalize(sansdata,mon0=1e8):
    """"
Given a SansData object, normalize the data to the provided monitor
"""
    
    monitor=sansdata.metadata['run.moncnt']
    result=sansdata.data*mon0/monitor
    res=SansData()
    res.data=result
    res.metadata=deepcopy(sansdata.metadata)
    #added res.q
    res.q=copy(sansdata.q)
    res.qx=copy(sansdata.qx)
    res.qy=copy(sansdata.qy)
    res.theta=copy(sansdata.theta)
    return res

def correct_solid_angle(sansdata):
    """
given a SansData with q,qx,qy,and theta images defined,
correct for the fact that the detector is flat and the eswald sphere is curved.
"""
    #need to calculate theta here...
    L2=sansdata.metadata['det.dis']
    x0=sansdata.metadata['det.beamx'] #should be close to 64
    y0=sansdata.metadata['det.beamy'] #should be close to 64
    wavelength=sansdata.metadata['resolution.lmda']
    shape=sansdata.data.x.shape
# theta=np.empty(shape,'Float64')
# q=np.empty(shape,'Float64')
    qx=np.empty(shape,'Float64')
    qy=np.empty(shape,'Float64')
    #vectorize this loop, it will be slow at 128x128
    #test against this simpleminded implentation
    
    ### switching to vectorized form - bbm
# for x in range(0,shape[0]):
# for y in range(0,shape[1]):
# X=PIXEL_SIZE_X_CM*(x-x0)
# Y=PIXEL_SIZE_Y_CM*(y-y0)
# r=np.sqrt(X**2+Y**2)
# theta[x,y]=np.arctan2(r,L2)/2
# q[x,y]=(4*np.pi/wavelength)*np.sin(theta[x,y])
# alpha=np.arctan2(Y,X)
# qx[x,y]=q[x,y]*np.cos(alpha)
# qy[x,y]=q[x,y]*np.sin(alpha)
    x,y = np.indices(shape)
    X = PIXEL_SIZE_X_CM*(x-x0)
    Y=PIXEL_SIZE_Y_CM*(y-y0)
    r=np.sqrt(X**2+Y**2)
    theta=np.arctan2(r,L2*100)/2  #remember to convert L2 to cm from meters
 
    
    result=sansdata.data*(np.cos(theta)**3)
    res=SansData()
    res.data=result
    res.metadata=deepcopy(sansdata.metadata)
    #adding res.q
    res.q = copy(sansdata.q)
    res.qx=copy(sansdata.qx)
    res.qy=copy(sansdata.qy)
    res.theta=theta
    return res
##Theta needs to be set, since now the q conversion is done at the end
#def set_theta(sansdata):
    #L2=sansdata.metadata['det.dis']
    #x0=sansdata.metadata['det.beamx'] #should be close to 64
    #y0=sansdata.metadata['det.beamy'] #should be close to 64
    #wavelength=sansdata.metadata['resolution.lmda']
    #shape=sansdata.data.x.shape
    #x,y = np.indices(shape)
    #X = PIXEL_SIZE_X_CM*(x-x0)
    #Y=PIXEL_SIZE_Y_CM*(y-y0)
    #r=np.sqrt(X**2+Y**2)
    #theta=np.arctan2(r,L2)/2
    #res=SansData()
    #res.data=copy(sansdata.data)
    #res.metadata=deepcopy(sansdata.metadata)
    #res.theta=theta
    #return res

def correct_detector_efficiency(sansdata):
    """
    Given a SansData object, corrects for the efficiency of the detection process
    """
    L2=sansdata.metadata['det.dis']
    lambd = sansdata.metadata["resolution.lmda"]
    
    shape=sansdata.data.x.shape
    (x0,y0) = np.shape(sansdata.data)
    x,y = np.indices(shape)
    X = PIXEL_SIZE_X_CM*(x-x0/2)
    Y = PIXEL_SIZE_Y_CM*(y-y0/2)
    r=np.sqrt(X**2+Y**2)
    theta=np.arctan2(r,L2*100)/2   
    
    stAl = 0.00967*lambd*0.8		#dimensionless, constants from JGB memo
    stHe = 0.146*lambd*2.5
    
    ff = np.exp(-stAl/np.cos(theta))*(1-np.exp(-stHe/np.cos(theta))) / ( np.exp(-stAl)*(1-np.exp(-stHe)) )

    res=SansData()
    res.data=sansdata.data/ff
    res.metadata=deepcopy(sansdata.metadata)
    #added res.q
    res.q = copy(sansdata.q)
    res.qx=copy(sansdata.qx)
    res.qy=copy(sansdata.qy)
    #note that the theta calculated for this correction is based on the center of the 
    #detector and NOT the center of the beam. Thus leave the q-relevant theta alone.
    res.theta=copy(sansdata.theta)

    return res

def correct_large_angle_transmission(sansdata):
    """
    Correct for large angle transmission effects - Brulet et al
    """
    #Needs implementing
    #Uses transmission from the data, so not sure how this can be done on load....
    #AJJ - don't do this correction when calculating transmissions....
    

def correct_detector_sensitivity(sansdata,sensitivity):
    """"
Given a SansData object and an sensitivity map generated from a div,
correct for the efficiency of the detector. Recall that sensitivities are
generated by taking a measurement of plexiglass and dividing by the mean value
"""
    #result=sansdata.data/sensitivity #Could be done more elegantly by defining a division method on SansData
    #res=SansData()
    #res.data=result
    #res.metadata=deepcopy(sansdata.metadata)
    ##added res.q
    #res.q=copy(sansdata.q)
    #res.qx=copy(sansdata.qx)
    #res.qy=copy(sansdata.qy)
    #res.theta=copy(sansdata.theta)
    
    #Used SansData operation to make more efficient
    result  = sansdata.__truediv__(sensitivity)
    
    return result

def correct_blocked_beam(sample,blocked_beam,transmission):
    """"
Given a SansData object, the transmissions and blocked beam, correct for the
blocked beam.
"""
    #it would probably be more pleasant to have keyword arguments and to check
    #for their presence so that a user of the class doesn't have to know the
    #function signature. The advantage of the current method is that an error is
    #automatically raised if the user doesn't pass a required parameter and there should
    #be no question of whether a parameter is actually required or not. Here, I am letting
    #the clarity trump convenience.
    result=(sample.data-blocked_beam.data)/transmission
    res=SansData()
    res.data=result
    res.metadata=deepcopy(sample.metadata)
    #added res.q
    res.q = copy(sample.q)
    res.qx=copy(sample.qx)
    res.qy=copy(sample.qy)
    res.theta=copy(sample.theta)
    return res

#Correction needed eventually 
def correct_dead_time(sansdata,deadtime=3.4e-6):
    
    dscale = 1/(1-deadtime*(np.sum(sansdata.data)/sansdata.metadata["run.rtime"]))
    
    result = SansData()
    result.data = sansdata.data*dscale
    result.metadata=deepcopy(sansdata.metadata)
    result.q = copy(sansdata.q)
    result.qx = copy(sansdata.qx)
    result.qy = copy(sansdata.qy)
    result.theta = copy(sansdata.theta)
    
    return result
    
def correct_background(sample,empty_cell):
    """"
Given a SansData of sample and empty cell that have been corrected, subtract them
"""
    #result=sample-empty_cell
    result = sample.__sub1__(empty_cell)
    return result
    
def generate_transmission(in_beam,empty_beam,coords_bottom_left,coords_upper_right):
    """
To calculate the transmission, we integrate the intensity in a box for a measurement
with the substance in the beam and with the substance out of the beam and take their ratio.
The box is definied by its bottom left and upper right corner. These are registered to pixel coordinates
the coords are assumed to be tuple or a list in the order of (x,y). I start counting at (0,0).

Coords are taken with reference to bottom left of the image.
"""
    I_in_beam=0.0
    I_empty_beam=0.0
    (xmax,ymax) = np.shape(in_beam.data)
    print xmax,ymax
    #Vectorize this loop, it's quick, but could be quicker
    #test against this simple minded implementation
    print ymax-coords_bottom_left[1],ymax-coords_upper_right[1]
    for x in range(coords_bottom_left[0],coords_upper_right[0]):
        for y in range(ymax-coords_upper_right[1],ymax-coords_bottom_left[1]):
            I_in_beam=I_in_beam+in_beam.data[x,y]
            I_empty_beam=I_empty_beam+empty_beam.data[x,y]
    result=I_in_beam/I_empty_beam
    return result

def initial_correction(SAM,BGD,EMP,Trans):
    #SAM-BGD
    FIR = correct_background(SAM,BGD)
    #(EMP-BGD)*(tsam/temp)
    SEC = (EMP.__sub1__(BGD)).__mul__(Trans)
    FINAL = FIR.__sub1__(SEC)
    return FINAL
    
    

    
def convert_q(sansdata):
    """
generate a q_map for sansdata. Each pixel will have 4 values: (qx,qy,q,theta)
"""
    L2=sansdata.metadata['det.dis']
    x0=sansdata.metadata['det.beamx'] #should be close to 64
    y0=sansdata.metadata['det.beamy'] #should be close to 64
    wavelength=sansdata.metadata['resolution.lmda']
    shape=sansdata.data.x.shape
# theta=np.empty(shape,'Float64')
# q=np.empty(shape,'Float64')
    qx=np.empty(shape,'Float64')
    qy=np.empty(shape,'Float64')
    #vectorize this loop, it will be slow at 128x128
    #test against this simpleminded implentation
    
    ### switching to vectorized form - bbm
# for x in range(0,shape[0]):
# for y in range(0,shape[1]):
# X=PIXEL_SIZE_X_CM*(x-x0)
# Y=PIXEL_SIZE_Y_CM*(y-y0)
# r=np.sqrt(X**2+Y**2)
# theta[x,y]=np.arctan2(r,L2)/2
# q[x,y]=(4*np.pi/wavelength)*np.sin(theta[x,y])
# alpha=np.arctan2(Y,X)
# qx[x,y]=q[x,y]*np.cos(alpha)
# qy[x,y]=q[x,y]*np.sin(alpha)
    x,y = np.indices(shape)
    X = PIXEL_SIZE_X_CM*(x-x0)
    Y=PIXEL_SIZE_Y_CM*(y-y0)
    r=np.sqrt(X**2+Y**2)
    theta=np.arctan2(r,L2*100)/2  #remember to convert L2 to cm from meters
    q=(4*np.pi/wavelength)*np.sin(theta)
    alpha=np.arctan2(Y,X)
    qx=q*np.cos(alpha)
    qy=q*np.sin(alpha)
    res=SansData()
    res.data=copy(sansdata.data)
    res.metadata=deepcopy(sansdata.metadata)
    #Adding res.q
    res.q = q
    res.qx=qx
    res.qy=qy
    res.theta=theta
    return res
#converts qx and qy values of a Sansdata obj into javascript format for plotting
def convert_qxqy(sansdata):
    
    qx = sansdata.qx
    x = qx[0].tolist()
    plottable_x= {
    'z': x,
    'title': 'Qx',
    'dims': {
      'xmax': qx.shape[0],
      'xmin': 0.0, 
      'ymin': 0.0, 
      'ymax': qx.shape[1],
      'xdim': 128,
      'ydim': 128,
    },
    'xlabel': 'x-axis',
    'ylabel': 'y-axis',
    'zlabel': 'Intensity',
};
    qy = sansdata.qx
    y = qx[0].tolist()
    plottable_y= {
    'z': y,
    'title': 'Qx',
    'dims': {
      'xmax': qy.shape[0],
      'xmin': 0.0, 
      'ymin': 0.0, 
      'ymax': qy.shape[1],
      'xdim': 128,
      'ydim': 128,
    },
    'xlabel': 'x-axis',
    'ylabel': 'y-axis',
    'zlabel': 'Intensity',
};
    #res=SansData()
    #res.data=copy(sansdata.data)
    #res.metadata=deepcopy(sansdata.metadata)
    ##Adding res.q
    #res.q = sansdata.q
    #res.qx=json.dumps(plottable_x)
    #res.qy=json.dumps(plottable_y)
    #res.theta=sansdata.theta
    #return res 
    res=SansData()
    res.data=copy(sansdata.data)
    res.metadata=deepcopy(sansdata.metadata)
    #Adding res.q
    res.q = sansdata.q
    res.qx= sansdata.qx 
    res.qy = sansdata.qy
    res.theta=sansdata.theta
    x = json.dumps(plottable_x)
    y = json.dumps(plottable_y)
    return res,x,y
    
def annular_av(sansdata):
    #annular_mask_antialiased(shape, center, inner_radius, outer_radius, background_value=0.0, mask_value=1.0, oversampling=8)    
    
    #x0=sansdata.metadata['det.beamx'] #should be close to 64
    #y0=sansdata.metadata['det.beamy'] #should be close to 64
    #shape=sansdata.data.x.shape
    #x,y = np.indices(shape)
    #X = PIXEL_SIZE_X_CM*(x-x0)
    #Y=PIXEL_SIZE_Y_CM*(y-y0)
    #alpha=np.arctan2(Y,X)
  
    #q = sansdata.q
    #qx=q*np.cos(alpha)
    print sansdata.q
    # calculate the change in q that corresponds to a change in pixel of 1
    q_per_pixel = sansdata.qx[1,0]-sansdata.qx[0,0] / 1.0
   
    # for now, we'll make the q-bins have the same width as a single pixel
    step = q_per_pixel
    print "Step: ", step 
    shape1 = (128,128)
    center = (sansdata.metadata['det.beamx'],sansdata.metadata['det.beamy'])
    Qmax = sansdata.q.max()
    print "QMax: ",Qmax
    Q = np.arange(0,Qmax,step)
    #print "Q=",Q
    I = []
    for i in Q:
        # inner radius is the q we're at right now, converted to pixel dimensions:
        inner_r = i * (1.0/q_per_pixel)
        # outer radius is the q of the next bin, also converted to pixel dimensions:
        outer_r = (i + step) * (1.0/q_per_pixel)
        mask = annular_mask_antialiased(shape1,center,inner_r,outer_r)
        #print "Mask: ",mask
        norm_integrated_intensity = np.sum(mask*sansdata.data.x)
        if (norm_integrated_intensity !=  0.0):
            norm_integrated_intensity/=np.sum(mask)
        I.append(norm_integrated_intensity*step)
    Q = Q.tolist()
    I = (np.array(I)).tolist()
    print "Q is : ", Q
    print "I is : ", I
    Qlog = np.log10(Q).tolist()
    Ilog = np.log10(I).tolist()
    print "Qlog: ", Qlog
    print "Ilog: ", Ilog
    plottable_1D = {
    'x': {'linear': {'data':Q, 'label':'q (A^-1))'}},
    'y': [{
        'linear': {'data': I, 'label':'Intensity-I(q)'},
        'log10': {'data': Ilog, 'label':'Intensity-I(q)'},
        }],
    'title': '1D Sans Data',
    'clear_existing': False,
    'color': 'Red',
    'style': 'line',
    };
    plottable_1D = json.dumps(plottable_1D)
    plt.plot(Q,I,'ro')
    plt.title('1D')
    plt.xlabel('q(A^-1)')
    plt.ylabel('I(q)')
    plt.show()
    #sys.exit()
    return plottable_1D
    
def absolute_scaling(sample,empty,DIV,Tsam,instrument):  #data (that is going through reduction),empty beam, div, Transmission of the sample,instrument(NG3.NG5,NG7)
   #Variable detCnt,countTime,attenTrans,monCnt,sdd,pixel
    detCnt = empty.metadata['run.detcnt']
    countTime = empty.metadata['run.ctime']
    monCnt = empty.metadata['run.moncnt']
    sdd = empty.metadata['det.dis'] *100
    pixel = PIXEL_SIZE_X_CM
    lambd = wavelength  = empty.metadata['resolution.lmda']
    attenNo = empty.metadata['run.atten']
    print "Attetno: ",attenNo
    print "Countime: ",countTime
    print "monCnt: ", monCnt
    print "sdd:", sdd
    print "Lambda: ",lambd
    print "detCount: ", detCnt
    
    #Need attenTrans - AttenuationFactor - need to know whether NG3, NG5 or NG7 (acctStr)
    
    
    #-----------------Reading in array from NG7 and NG5 .dat files (can be changed to .txt) which contain attenuation factors----------
    #file = open("NG7.txt", "w") #w = write
    #file.write(repr(a))
    #file.close()
    
    file = open("NG7.dat","r") # r = read
    f = eval(file.read())
    file.close()
    NG7 = f
    
    
    file = open("NG3.dat","r") # r = read
    g = eval(file.read())
    file.close()
    NG3 = g
   

    #-----Creating Dictionary-----
   
    attenFact = {
        
        'NG7': NG7.copy(),
        'NG5': NG7.copy(),
        'NG3': NG3.copy(),
        
        }
    #-----------------------------
    #AJJ - array indexing issue here. But this is a hack anyway - need to interpolate wavelength values
    attenTrans = attenFact[instrument][attenNo][wavelength-1]
    print "attenFact: ", attenTrans
    
    
    #-------------------------------------------------------------------------------------#
    
    #correct empty beam by the sensitivity
    data = empty.__truediv__(DIV)
    #Then take the sum in XY box
    coord_bottom_left=(62,60)
    coord_top_right=(72,68)
    summ = 0
    sumlist = []
    #-----Something wrong Here------
    #print range(coord_right[0]-coord_left[0])
    
    (xmax,ymax) = np.shape(data.data)
    
    for x in range(coord_bottom_left[0],coord_top_right[0]):
        for y in range(ymax-coord_top_right[1],ymax-coord_bottom_left[1]):
            summ = summ + data.data[x,y]
            sumlist.append(data.data[x,y])
    detCnt = summ
    print "DETCNT: ",detCnt

   
    #------End Result-------#
    #This assumes that the data has *not* been normalized at all.
    #Thus either fix this or pass un-normalized data.
    kappa = detCnt/countTime/attenTrans*1.0e8/(monCnt/countTime)*(pixel/sdd)**2 #Correct Value: 6617.1
    print "Kappa: ", kappa
                                                 
    utc_datetime = date.datetime.utcnow()
    print utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
    
    #-----Using Kappa to Scale data-----#
    Dsam =  sample.metadata['sample.thk']
    ABS = sample.__mul__(1/(kappa*Dsam*Tsam))
    #------------------------------------
    return ABS

def chain_corrections():
    """a sample chain of corrections"""
    
    #read the files
    sample_4m=read_sample(map_files('sample_4m'))
    empty_cell_4m=read_sample(map_files('empty_cell_4m'))
    empty_4m=read_sample(map_files('empty_4m'))
    transmission_sample_cell_4m=read_sample(map_files('trans_sample_4m'))
    transmission_empty_cell_4m=read_sample(map_files('trans_empty_cell_4m'))
    blocked_beam_4m=read_sample(map_files('blocked_4m'))
    sensitivity=read_div(map_files('div'))
    #mask=read_sample(map_files('mask'))
    
    #correct solid angle
    sample_4m_solid=correct_solid_angle(sample_4m)
    empty_cell_4m_solid=correct_solid_angle(empty_cell_4m)
    blocked_beam_4m_solid=correct_solid_angle(blocked_beam_4m)
    empty_4m_solid=correct_solid_angle(empty_4m)
 
    #correct for efficiency
    sample_4m_eff=correct_detector_efficiency(sample_4m_solid)
    empty_cell_4m_eff=correct_detector_efficiency(empty_cell_4m_solid)
    blocked_beam_4m_eff=correct_detector_efficiency(blocked_beam_4m_solid)
    empty_4m_eff=correct_detector_efficiency(empty_4m_solid)

    #correct for deadtime
    sample_4m_dtc=correct_dead_time(sample_4m_eff)
    empty_cell_4m_dtc=correct_dead_time(empty_cell_4m_eff)
    blocked_beam_4m_dtc=correct_dead_time(blocked_beam_4m_eff)
    empty_4m_dtc=correct_dead_time(empty_4m_eff)
    
    #normalize the monitors
    sample_4m_norm=monitor_normalize(sample_4m_eff)
    empty_cell_4m_norm=monitor_normalize(empty_cell_4m_eff)
    transmission_sample_cell_4m_norm=monitor_normalize(transmission_sample_cell_4m)
    transmission_empty_cell_4m_norm=monitor_normalize(transmission_empty_cell_4m)
    empty_4m_norm=monitor_normalize(empty_4m_eff)

    #calculate transmission
    coord_left=(60,60)
    coord_right=(70,70)
 
    transmission_sample_cell_4m_rat=generate_transmission(transmission_sample_cell_4m_norm,empty_4m_norm,
                                                      coord_left,coord_right)
    transmission_empty_cell_4m_rat=generate_transmission(transmission_empty_cell_4m_norm,empty_4m_norm,
                                                      coord_left,coord_right)
    print 'Sample transmission= {0} (IGOR Value = 0.724): '.format(transmission_sample_cell_4m_rat) #works now
    print 'Empty Cell transmission= {0} (IGOR Value = 0.929): '.format(transmission_empty_cell_4m_rat)
    
    #Initial Correction
    SAM = sample_4m_norm
    print SAM.data.x
    EMP = empty_cell_4m_norm
    print "EMP: "
    print EMP.data.x
    BGD = blocked_beam_4m
    print "BGD"
    print BGD.data.x
    Tsam = transmission_sample_cell_4m_rat
    Temp = transmission_empty_cell_4m_rat
    COR1 = SAM.__sub1__(BGD)
    print COR1.data.x
    COR2 = (EMP.__sub1__(BGD))
    COR3 = COR2.__mul__(Tsam/Temp)
    print COR2.data.x
    print COR3.data.x
    COR = COR1.__sub1__(COR3)
    print "after initial correction: "
    
    print COR.data.x
    
    ##Test initial correction
    #plt.figure()
    #plt.imshow(COR.data.x)
    #plt.show()
    #-------------Initial Correction Ends------------------------
    
    ##Detector Sensitivity Corrections (.DIV)
    CAL = correct_detector_sensitivity(COR,sensitivity) #Replaced With function instead of merely operations
    #CAL = COR
    #print "After DIV: "
    #print CAL.data.x
    
    #-------------Absolute Scaling----------------
    
    #The Following values are needed for absolute scaling
    #-TSTAND      value: 1
    #-DSTAND      value: 1
    #-IZERO - the value for this set of data: 6617.1 - this is Kappa also, i believe
    #-XSEC        value: 1 
    #-Tsam - already have this value from above 
    #-Dsam - sample thickness
    # Equation : ABS = (1/Kappa*Dsam*Tsam)*CAL
    #kappa = detCnt/countTime/attenTrans*1.0e8/(monCnt/countTime)*(pixel/sdd)^2
    #Dsam =  CAL.metadata['sample.thk']
    
    #Have to pass un-normalized, as loaded, data file here for empty.
    ABS = absolute_scaling(CAL,empty_4m,sensitivity,Tsam,'NG3')
    print "ABS: "
    print ABS
    
    #x,y = q_is_zero_at(CAL)
    #IZERO = CAL.data.x[x,y]
    #print IZERO
    
    #ABS = CAL.__mul__.(1/IZERO*Dsam*Tsam)
    
    #-------------END of Absolute Scaling-------------

    #Now converting to q
    ABSQ = convert_q(ABS)
    
    ABSQ,x,y = convert_qxqy(ABSQ)
    # convert_qxqy shouldn't be used as a filter that returns data... 
    # it puts data into an output form different than sansdata (Changed I think)
    #ar_av(CAL)

    #-------------------Plot--------------------------

    #fig = plt.figure()
    #ax1 = fig.add_subplot(331, aspect='equal')
    #plt.title("SAM")
    #ax2 = fig.add_subplot(332, aspect='equal')
    #plt.title("EMP")
    #ax3 = fig.add_subplot(333, aspect='equal')
    #plt.title("BGD")
    #ax4 = fig.add_subplot(334, aspect='equal')
    #plt.title("COR")
    #ax5 = fig.add_subplot(335, aspect='equal')
    #plt.title("CAL")
    #ax6 = fig.add_subplot(336, aspect='equal')
    #plt.title("ABS")

    #ax1.imshow(SAM.data.x)
    #ax2.imshow(EMP.data.x)
    #ax3.imshow(BGD.data.x)
    #ax4.imshow(COR.data.x)
    #ax5.imshow(CAL.data.x)
    #ax6.imshow(ABS.data.x)
    #plt.show()
    
    
    AVG = annular_av(ABS)
    print AVG
    

def map_files(key):
    """
Generate the mapping between files and their roles
"""
    
    datadir=os.path.join(os.path.dirname(__file__),'ncnr_sample_data')
    filedict={'empty_1m':os.path.join(datadir,'SILIC001.SA3_SRK_S101'),
              'empty_4m':os.path.join(datadir,'SILIC002.SA3_SRK_S102'),
              'empty_cell_1m':os.path.join(datadir,'SILIC003.SA3_SRK_S103'),
              'blocked_1m':os.path.join(datadir,'SILIC004.SA3_SRK_S104'),
              'trans_empty_cell_4m':os.path.join(datadir,'SILIC005.SA3_SRK_S105'),
              'trans_sample_4m':os.path.join(datadir,'SILIC006.SA3_SRK_S106'),
              'blocked_4m':os.path.join(datadir,'SILIC007.SA3_SRK_S107'),
              'empty_cell_4m':os.path.join(datadir,'SILIC008.SA3_SRK_S108'),
              'sample_1m':os.path.join(datadir,'SILIC009.SA3_SRK_S109'),
              'sample_4m':os.path.join(datadir,'SILIC010.SA3_SRK_S110'),
              'mask':os.path.join(datadir,'DEFAULT.MASK'),
              'div':os.path.join(datadir,'PLEX_2NOV2007_NG3.DIV'),
              }
    return filedict[key]
              
    
    


if __name__ == '__main__':
    chain_corrections()
    if 0:
        for key, value in metadata.iteritems():
            print key,value
        print metadata
        
      
        attenuation=metadata['run.atten 7.0']
        
    
    
    
    
