import sys
import numpy as np
from . import readncnr5
from . import scriptutil as SU
from .Ppeaks import Data


def read_data(mydirectory,myfilebase,myend):
    myfilebaseglob=myfilebase+'*.'+myend
    print myfilebaseglob
    flist = SU.ffind(mydirectory, shellglobs=(myfilebaseglob,))
    #SU.printr(flist)
    mydatareader=readncnr5.datareader()
    datasets = []
    for currfile in sorted(flist):
        #print currfile
        mydata=mydatareader.readbuffer(currfile)
        mon=mydata.metadata['monitor']*mydata.metadata['monitor_prefactor']
        H,K,L = [np.array(mydata.data[s]) for s in 'h','k','l']
        I = np.array(mydata.data['counts'],'int32')
        datasets.append( (H,K,I,np.ones_like(I)*mon) )

    return Data(*[np.concatenate(V) for V in zip(*datasets)])

from matplotlib.colors import Colormap, colorConverter
class ColormapMask(Colormap):
    def __init__(self, name, color, N=256):
        Colormap.__init__(self, name, N)
        self.color = colorConverter.to_rgb(color)
    def _init(self):
        self._lut = np.ones((self.N+3,4))
        self._lut[:,:3] = self.color
        self._lut[:self.N,3] = np.linspace(1,0,self.N)
        self._isinit = True
        self._set_extremes()

def plot(data, sigma=0.002):
    import pylab
    step = 0.0002
    sigma = 0.0009
    #Hr = (0.48,0.52) if dataset[4] not in 'tu' else (-0.52,-0.48)
    #Kr = (0.48,0.52) if dataset[4] not in 't' else (-0.52,-0.48)
    Hr = data.X.min(),data.X.max()
    Kr = data.Y.min(),data.Y.max()
    #Hm = np.linspace(Hr[0],Hr[1],50)
    #Km = np.linspace(Kr[0],Kr[1],50)
    Hm = np.arange(np.floor(Hr[0]/step)*step, np.ceil(Hr[1]/step)*step, step)
    Km = np.arange(np.floor(Kr[0]/step)*step, np.ceil(Kr[1]/step)*step, step)
    HM,KM = np.meshgrid(Hm,Km)
    IM,MM = np.zeros_like(HM), np.zeros_like(HM)
    for i,(Hi,Ki,Ii,Mi) in enumerate(zip(data.X,data.Y,data.counts,data.monitor)):
        #print "point",i,"of",len(data.X),(Hi,Ki,Ii,Mi)
        stencil = np.exp(-((Hi-HM)**2 + (Ki-KM)**2)/(2*sigma**2))
        IM += stencil*Ii
        MM += stencil*Mi

    pylab.subplot(121, aspect='equal')
    pylab.cla()
    pylab.pcolormesh(Hm,Km,50000*IM/(MM+1),edgecolors='None')
    white_mask = ColormapMask("white_mask","white",N=64)
    pylab.pcolormesh(Hm,Km,
                     MM,vmin=0,vmax=MM.max(),
                     cmap=white_mask,hold=True,edgecolors='None')  
    pylab.axis([Hm[0],Hm[-1],Km[0],Km[-1]])
    pylab.grid()
    #pylab.colorbar()
    pylab.subplot(122, aspect='equal')
    pylab.cla()
    pylab.scatter(data.X,data.Y,c=50000.*data.counts/(data.monitor+1),
                  s=400, marker='s')
    pylab.axis([Hm[0],Hm[-1],Km[0],Km[-1]])
    pylab.grid(True)

def plot(data):
    import pylab
    pylab.cla()
    pylab.axes(aspect='equal')
    X,Y,I,M = sumequal(abs(data.X),np.abs(data.Y),data.counts,data.monitor)
    M0 = M.max()
    rate = np.ma.masked_invalid(I/M*M0)
    #pylab.contourf(Y,X,rate)
    pylab.pcolor(Y,X,rate)
    white_mask = ColormapMask("white_mask","white",N=64)
    #pylab.pcolormesh(Y,X,M,vmin=0,
    #                 cmap=white_mask,hold=True,edgecolors='None')  
    pylab.axis([0.469, 0.495, 0.479, 0.5025])
    pylab.colorbar(orientation='horizontal')

def sumequal(X,Y,counts,monitor,tol=0.0001):
    from scipy import sparse
    x,y = np.sort(X), np.sort(Y)
    dx,dy = np.diff(x), np.diff(y)
    dx = dx[dx>tol]
    dy = dy[dy>tol]
    dx,dy = dx[0],dy[0]
    
    xmin,ymin = x[0],y[0]
    xmax,ymax = x[-1],y[-1]

    #print xmin,xmax,ymin,ymax,dx,dy

    xm = np.arange(xmin-dx/2,xmax+dx/2,dx)
    ym = np.arange(ymin-dy/2,ymax+dy/2,dy)
    gridX,gridY = np.meshgrid(ym,xm)
    xidx = np.searchsorted(xm,X)-1
    yidx = np.searchsorted(ym,Y)-1
    #print xidx.min(), xidx.max(), yidx.min(), yidx.max()
    #print gridX.shape
    gridI = sparse.coo_matrix((counts,(xidx,yidx)),shape=gridX.shape)
    gridM = sparse.coo_matrix((monitor,(xidx,yidx)),shape=gridX.shape)

    return gridX,gridY,np.asarray(gridI.todense()),np.asarray(gridM.todense())
    

def main():    
    import pylab
    #mydirectory=r'D:\BiFeO3film\Mar27_2011'
    mydirectory=r'/net/charlotte/var/ftp/pub/ncnrdata/bt9/201102/ylem/BiFeO3film/Mar27_2011'
    myend='bt9'
    pylab.interactive(True)
    for dataset in sys.argv[1:]:
        data = read_data(mydirectory,"mesh"+dataset,myend)
        plot(data)
        _ = raw_input("> ") 

main()
