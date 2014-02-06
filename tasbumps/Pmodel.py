import sys

import numpy as np

from bumps.fitters import FIT_OPTIONS, FitDriver, DreamFit, StepMonitor, ConsoleMonitor
from bumps.names import Parameter, FitProblem
from bumps import pmath

from . import readncnr5
from . import scriptutil as SU
from .Ppeaks import Peaks, Gaussian, Background, Data

def read_data(mydirectory,myfilebase,myend):
    myfilebaseglob=myfilebase+'*.'+myend
    print myfilebaseglob
    flist = SU.ffind(mydirectory, shellglobs=(myfilebaseglob,))
    #SU.printr(flist)
    mydatareader=readncnr5.datareader()
    datasets = []
    for currfile in sorted(flist):
        print currfile
        mydata=mydatareader.readbuffer(currfile)
        mon=mydata.metadata['monitor']*mydata.metadata['monitor_prefactor']
        H,K,L = [np.array(mydata.data[s]) for s in 'h','k','l']
        I = np.array(mydata.data['counts'],'int32')
        datasets.append( (H,K,I,np.ones_like(I)*mon) )

    return Data(*[np.concatenate(V) for V in zip(*datasets)])

def build_problem(mydirectory,myfilebase,myend,cost="poisson"):

    monitor_efficiency = 0.1
    resolution = 0.001
    scale = resolution**2/monitor_efficiency
    scale = 1e-6
    M = Peaks([Gaussian(name="G1-"),
               Gaussian(name="G2-"),
               #Gaussian(name="G3-"),
               #Gaussian(name="G4-"),
               Background()],
               scale,
               data=read_data(mydirectory,myfilebase,myend),
               #cost='poisson',
               cost=cost,
               )

    # Peak intensity and background
    background = 1
    M.parts[-1].C.value = background
    M.parts[-1].C.range(0,1000)
    for peak in M.parts[:-1]:
        peak.A.value = 1./(len(M.parts)-1)  # Equal size peaks
        peak.A.range(0,1)

    peak1 = M.parts[0]
    if 0:
        # Peak centers are independent
        for peak in M.parts[:-1]:
            peak.xc.range(0.45,0.55)
            peak.yc.range(-0.55,-0.4)
    else:
        # Peak centers lie on a line
        alpha=Parameter(45.0, name="alpha")
        alpha.range(-90.,90.)
        peak1.xc.range(0.40,0.55)
        peak1.yc.range(0.40,0.55)
        #peak1.yc.range(-0.55,-0.4)
        for i,peak in enumerate(M.parts[1:-1]):
            delta=Parameter(.0045, name="delta-%d"%(i+1))
            delta.range(0.00,0.03)
            peak.xc = peak1.xc + delta*pmath.cosd(alpha)
            peak.yc = peak1.yc + delta*pmath.sind(alpha)

        # Initial values
        cx, cy = 0.4996-0.4957, -0.4849+0.4917
        alpha.value = np.degrees(np.arctan2(cy,cx))
        delta.value = np.sqrt(cx**2+cy**2)
        peak1.xc.value,peak1.yc.value = 0.4957,0.4917

    # Peak location and shape
    dx, dy = 0.4997-0.4903, -0.4969+0.4851
    dxm, dym = 0.4951-0.4960, -0.4941+0.4879
    peak1.s1.value = np.sqrt(dx**2+dy**2)/2.35/2
    peak1.s2.value = np.sqrt(dxm**2+dym**2)/2.35/2
    peak1.theta.value = np.degrees(np.arctan2(dy,dx))



    # Peak shape is the same across all peaks
    peak1.s1.range(0.001,0.010)
    peak1.s2.range(0.001,0.010)
    peak1.theta.range(-90, 90)
    for peak in M.parts[1:-1]:
        peak.s1 = peak1.s1
        peak.s2 = peak1.s2
        peak.theta = peak1.theta

    if 1:
        print "shape",peak1.s1.value,peak1.s2.value,peak1.theta.value
        print "centers alpha,delta",alpha.value,delta.value
        print "centers",(peak1.xc.value,peak1.yc.value),\
            (M.parts[1].xc.value,M.parts[1].yc.value)
    return FitProblem(M)




if 1:
    from bumps.mapper import MPMapper
    from bumps.cli import remember_best
    import pylab
    #mydirectory=r'D:\BiFeO3film\Mar27_2011'
    mydirectory=r'/net/charlotte/var/ftp/pub/ncnrdata/bt9/201102/ylem/BiFeO3film/Mar27_2011'
    myend='bt9'
    dataset = "mesh" +  (sys.argv[1] if len(sys.argv) > 1 else "g")
    cost = sys.argv[2] if len(sys.argv) > 2 else "poisson"
    problem=build_problem(mydirectory,dataset,myend,cost)
    peak1 = problem.fitness.parts[0]
    if dataset[4] in 'tu':
        peak1.xc.value = -0.49
        peak1.xc.range(-0.55,-0.4)
    if dataset[4] in 't': 
        peak1.yc.value = -0.49
        peak1.yc.range(-0.55,-0.4)

if __name__ == "__main__":
    fitdriver = FitDriver(DreamFit, problem=problem, burn=50000)
    #mapper = MPMapper
    #fitdriver.mapper = mapper.start_mapper(problem, ())    
    
    #make_store(problem,opts,exists_handler=store_overwrite_query)
    problem.output_path=r'/tmp/TestBumpDir'
    best, fbest = fitdriver.fit()
    print best,fbest
    remember_best(fitdriver, problem, best)
    pylab.show()
    print 'done'    
