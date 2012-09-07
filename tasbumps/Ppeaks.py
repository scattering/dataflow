from __future__ import division
import sys
from math import degrees, radians, sin, cos, log, pi


import numpy as np
#np.seterr(all='raise')

from bumps.parameter import Parameter, varying
from reduction.tripleaxis import rebin2

class Data(object):
    def __init__(self, X, Y, counts, monitor, display_monitor=50000):
        self.X, self.Y = X, Y
        self.counts, self.monitor = counts, monitor
        self.display_monitor = display_monitor

    def plot1d(self, theory, nllf):
        import pylab
        X,Y = self.X, self.Y
        data, monitor = self.counts, self.monitor

        idx = np.arange(data.shape[0])
        #idx = Y
        mon0 = self.display_monitor
        err = np.sqrt(data+1)*mon0/monitor
        theory, data = theory*mon0/monitor, data*mon0/monitor
        pylab.subplot(211)
        pylab.plot(idx,theory,'-')
        pylab.errorbar(idx,data,yerr=err,fmt='.', hold=True)
        pylab.subplot(212)
        pylab.plot(idx,np.sqrt(nllf),'.')
        pylab.plot(idx,abs(-(theory-data)/err),'.',hold=True)
 

    def plot2d(self, theory, nllf):
        import pylab
        X,Y = self.X, self.Y
        data, monitor = self.counts, self.monitor
          
        if len(data.shape) == 1:
            #print "rebinning"
            bins=20
        
            xmesh, ymesh, nllf = rebin2.rebin_2D(X, Y, nllf, num_bins=bins)
            data,monitor,theory = [rebin2.rebin_2D(X,Y,Z, num_bins=bins)[2] 
                                   for Z in data, monitor, theory]
            X,Y = xmesh,ymesh
        err = np.sqrt(data+(data==0))/(monitor+(monitor==0))
        theory, data = theory/(monitor+(monitor==0)), data/(monitor+(monitor==0))
        resid = (theory-data)/err
    
        vmin, vmax = 0, np.max(data)*1.1
        pylab.subplot(131)
        pylab.pcolormesh(X,Y, data, vmin=vmin, vmax=vmax)
        pylab.subplot(132)
        pylab.pcolormesh(X,Y, theory, vmin=vmin, vmax=vmax)
        pylab.subplot(133)
        pylab.subplot(233)
        pylab.pcolormesh(X,Y, nllf, vmin=0)
        pylab.colorbar()
        pylab.subplot(236)
        vmax = np.max(np.abs(resid))
        pylab.pcolormesh(X,Y, resid, vmin=-vmax, vmax=vmax)
        pylab.colorbar()

    #plot = plot1d
    plot = plot2d

_LOGFACTORIAL = np.array([log(np.prod(np.arange(1.,k+1))) for k in range(21)])
def logfactorial(n):
    result = np.empty(n.shape, dtype='double')
    idx = (n<=20)
    result[idx] = _LOGFACTORIAL[n[idx]]
    n = n[~idx]
    result[~idx] = n*np.log(n) - n + np.log(n*(1+4*n*(1+2*n)))/6 + log(pi)/2
    return result


class Gaussian(object):
    def __init__(self, A=1, xc=0, yc=0, s1=1, s2=1, theta=0, name=""):
        self.A = Parameter(A,name=name+"A")
        self.xc = Parameter(xc,name=name+"xc")
        self.yc = Parameter(yc,name=name+"yc")
        self.s1 = Parameter(s1,name=name+"s1")
        self.s2 = Parameter(s2,name=name+"s2")
        self.theta = Parameter(theta,name=name+"theta")

    def parameters(self):
        return dict(A=self.A,
                    xc=self.xc, yc=self.yc,
                    s1=self.s1, s2=self.s2,
                    theta=self.theta)

    def __call__(self, x, y):
        # dx,dy is related to resolution.  What we really want is a convolution of the resolution function and
        # the theory function for a given point x,y.  With a well defined resolution function, sample broadening
        # of the peaks can be separated from instrumental broadening.
        dx = dy = 1 
        height = self.A.value
        s1 = self.s1.value
        s2 = self.s2.value
        t  = -radians(self.theta.value)
        xc = self.xc.value
        yc = self.yc.value
        if s1==0 or s2==0: return np.zeros_like(x)
        a =  cos(t)**2/s1**2 + sin(t)**2/s2**2
        b = sin(2*t)*(-1/s1**2 + 1/s2**2)
        c =  sin(t)**2/s1**2 + cos(t)**2/s2**2
        xbar,ybar = x-xc,y-yc
        Zf = np.exp( -0.5*(a*xbar**2 + b*xbar*ybar + c*ybar**2) ) / (2*np.pi*s1*s2)
        return Zf*abs(height)/(dx*dy) 

class Background(object):
    def __init__(self, C=0, name=""):
        self.C = Parameter(C,name=name+"background")
    def parameters(self):
        return dict(C=self.C)
    def __call__(self, x, y):
        dx = dy = 1
        return self.C.value/(dx*dy)

class Peaks(object):
    def __init__(self, parts, scale, data, cost='poisson'):
        self.data = data
        self.scale = scale
        self.parts = parts
        self._poisson_constant = logfactorial(self.data.counts)
        self._gaussian_constant = -0.5*np.log(2*pi*(self.data.counts + (self.data.counts==0)))
        if cost == 'poisson':
            self.point_nllf = self.poisson_nllf
        elif cost == 'gaussian':
            self.point_nllf = self.gaussian_nllf
        else:
            raise ValueError("expected cost to be poisson or gaussian")

    def numpoints(self):
        return np.prod(self.data.counts.shape)

    def parameters(self):
        return [p.parameters() for p in self.parts]

    def simulate_data(self, noise=None):
        self.data.counts = np.random.poisson(self.theory())

    def theory(self):
        return sum(M(self.data.X,self.data.Y) for M in self.parts)*self.data.monitor*self.scale

    def poisson_nllf(self):
        measured = self.data.counts
        expected = self.theory()
        return -(measured*np.log(expected) - expected - self._poisson_constant)

    def gaussian_nllf(self):
        measured = self.data.counts
        expected = self.theory()
        return 0.5*(measured - expected)**2/(measured + (measured==0))  - self._gaussian_constant

    def residuals(self):
        measured = self.data.counts
        expected = self.theory()
        return (measured - expected)/np.sqrt(measured + (measured==0))
        #return np.sqrt(2*self.point_nllf())

    def nllf(self):
        return sum(self.point_nllf())

    def __call__(self):
        """
        normalized chisq equivalent value
        """
        print "called"
        return self.nllf()/self.dof

    def plot(self, view='linear'):
        self.data.plot(self.theory(), self.point_nllf())

    def save(self, basename):
        import json
        pars = [(p.name,p.value) for p in varying(self.parameters())]
        out = json.dumps(dict(theory=self.theory().tolist(),
                              data=self.data.counts.tolist(),
                              monitor=self.data.monitor.tolist(),
                              X = self.data.X.tolist(),
                              Y = self.data.Y.tolist(),
                              pars = pars))
        open(basename+".json","w").write(out)

    def update(self):
        pass
