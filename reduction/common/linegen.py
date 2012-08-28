import pylab
import numpy as N
#import scipy.sandbox.delaunay as D
import matplotlib.delaunay as D

class locator:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        return
    def inside(self,xt,yt):
        inds=N.array([])
        for i in range(xt.shape[0]):
            indx=N.where(self.x==xt[i])[0]
            indy=N.where(self.y==yt[i])[0]
            ind=N.intersect1d(indx,indy)
            inds=N.concatenate((inds,ind))
        return N.ravel(inds)


class linegen:
    def __init__(self,point1,point2):
        self.point1=point1
        self.point2=point2 
        self.x1=N.float(self.point1[0])
        self.y1=N.float(self.point1[1])
        self.x2=N.float(self.point2[0])
        self.y2=N.float(self.point2[1])
        self.calc_slope()
        return
    
    def calc_slope(self):
        if self.x2==self.x1:
            self.slope=N.inf
            self.intercept=N.nan
        else:
            self.slope=(self.y2-self.y1)/(self.x2-self.x1)
            self.intercept=self.y1-self.slope*self.x1
        return

    def vertical_line(self,step=.1):
        y=N.arange(min(self.y2,self.y1),max(self.y1,self.y2)+step,step)
        x=self.x1*N.ones(y.shape)
        return x,y
    
    def gen_line(self,divisions=10):
        if self.slope==N.inf:
            step=N.absolute(self.y2-self.y1)/divisions
            x,y=self.vertical_line(step)
        else:
            step=N.absolute(self.x2-self.x1)/divisions
            x=N.arange(min(self.x2,self.x1),max(self.x1,self.x2)+step,step)
            y=self.slope*x+self.intercept
        return x,y

class line_interp:
    def __init__(self,point1,point2,divisions=50):
        self.myline=linegen(point1,point2)
        self.line_x,self.line_y=self.myline.gen_line(divisions=50)
        self.slope=self.myline.slope
        self.intercept=self.myline.intercept
        return
    def set_divisions(self,divisions=50):
        self.line_x,self.line_y=myline.gen_line(divisions=50)
        return
    def interp(self,xt,yt,zorigt):
        x=xt[:,zorigt>=0.0]
        y=yt[:,zorigt>=0.0]
        z=zorigt[:,zorigt>=0.0]
        cens,edg,tri,neig = D.delaunay(x,y)
        if 0:
            #plot triangulation
            for t in tri:
                # t[0], t[1], t[2] are the points indexes of the triangle
                t_i = [t[0], t[1], t[2], t[0]]
                pylab.plot(x[t_i],y[t_i])
        
        #pylab.plot(x,y,'o')
        #pylab.show()        
        
        
        tri = D.Triangulation(x,y)
        interp = tri.nn_interpolator(z)
        xi=N.copy(x)
        yi=N.copy(y)
        xi=N.concatenate((xi,self.line_x))
        yi=N.concatenate((yi,self.line_y))
        zi = interp(xi,yi)
        mylocator=locator(xi,yi)
        inds=mylocator.inside(self.line_x,self.line_y)
        outxi=xi[inds.astype(int)]
        outyi=yi[inds.astype(int)]
        outzi=zi[inds.astype(int)]
        return outxi,outyi,outzi

if __name__=="__main__":
    point1=(-2,-2)
    point2=(2,2)
    step=0.01
    xi,yi=N.mgrid[-2:2+step:step,-2:2+step:step]
    zi=N.exp(-xi*xi-yi*yi)
    x=N.reshape(xi,(1,xi.shape[0]*xi.shape[1])).ravel()
    y=N.reshape(yi,(1,yi.shape[0]*yi.shape[1])).ravel()
    z=N.reshape(zi,(1,zi.shape[0]*zi.shape[1])).ravel()
    pylab.pcolormesh(xi,yi,zi,shading='interp',cmap=pylab.cm.jet)
    myline=line_interp(point1,point2,divisions=50)
    xout,yout,zout=myline.interp(x,y,z)
    line_x=myline.line_x; line_y=myline.line_y 
    pylab.plot(line_x,line_y,'red',linewidth=3.0)  
    fig2=pylab.figure(figsize=(8,8))
    pylab.plot(xout,zout,'s')
    pylab.show()
    
