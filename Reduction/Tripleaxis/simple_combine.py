import numpy as N
import pylab
import copy
import scipy.interpolate as interpolate
pi=N.pi

def gauss(x,p):
    #Area center width Bak
    area=p[0]/N.sqrt(2*pi)/p[2]
    x0=p[1]
    width=p[2]
    background=p[3]
    y=background+area*N.exp(-(0.5*(x-x0)*(x-x0)/width/width))
    return y

def monitor_normalize(ylist,yerrlist,monlist,monitor=None):
    """"This function takes as input a list of intensities, errors, and monitor values and returns these
        intensities and errors placed on a common monitor.  The default is to use the monitor value of the first
        element in the monitor list.  This can be overided by selecting a value with the monitor keyword
        ylist:  a list of numpy arrays
        yerrlist:a list of numpy arrays
        monlist: a list of monitors corresponding to the list of inputted y values
        monitor: a keyword argument which gives a monitor value to normalize to
    """
    mon0=monlist[0]
    if monitor!=None:
        mon0=N.float64(monitor)
    y_in=N.array([],'float64')
    yerr_in=N.array([],'float64')
    mon_in=N.array(monlist,'float64')
    correction=mon0/mon_in #assumes that none of the monitor rates given is 0
    #make sure that we're not changing the original data
    y_out=copy.deepcopy(ylist)
    yerr_out=copy.deepcopy(yerrlist)
    for i in range(len(ylist)):
        y_out[i]=y_out[i]*correction[i]
        yerr_out[i]=yerr_out[i]*correction[i]
    return y_out,yerr_out


def simple_combine(xlist,ylist,yerrlist,monlist,monitor=None,method=None,eps=None,step=None):
    mon0=monlist[0]
    if monitor!=None:
        mon0=N.float64(monitor)
    x_in=N.array([],'float64')
    y_in=N.array([],'float64')
    yerr_in=N.array([],'float64')
    ylist_corrected,yerrlist_corrected=monitor_normalize(ylist,yerrlist,monlist,monitor=monitor)
    #assumes that xlist,ylist,yerrlist,monlist are all the same size)
    i2=0
    for i in range(len(ylist)):
        x_in=N.concatenate((x_in,N.array(xlist[i],'float64')))
        y_in=N.concatenate((y_in,N.array(ylist_corrected[i],'float64')))
        yerr_in=N.concatenate((yerr_in,N.array(yerrlist_corrected[i],'float64')))

        #While it would be convenient to check for zero steps, I think predictability is better than convenience
        #So, in that case, the user should specify the stepsize that they want!!!
        #As a convenience, we do only determine the minimum stepsize for arrays in which there are more than one element
        #of course, the problem this runs is that it may not truly be the minimum step size, but if we use the
        #total concatenated array, then if there are some identical ones, then we're also screwed...

        currmin=xlist[i].min()
        currmax=xlist[i].max()
        if xlist[i].shape[0]>1:
            diffs=N.diff(xlist[i])
            currmin_step=N.absolute(diffs.min())
            if i2==0:
                min_step=currmin_step
                i2=i2+1
            min_step=min(currmin_step,min_step)
        if i==0:
            xmax=currmax
            xmin=currmin
        xmin=min(currmin,xmin)
        xmax=max(currmax,xmax)


    #I think this is the correct way to determine the minimum step size
    if x_in.shape[0]>1:
        diffs=N.diff(x_in)
        currmin_step=N.absolute(diffs)
        min_step=currmin_step[currmin_step>0]
        min_step=currmin_step.min()
    #print 'min_step',min_step
    #print xmin
    #print xmax

    if method==None:
        #default behavior, sum points when they overlap to within either a reasonable or user defined epsilon
        if eps==None:
            eps=min_step*1e-4
        #start by sorting the values in ascending x order
        ind=x_in.argsort()
        x_in=x_in[ind]
        y_in=y_in[ind]
        yerr_in=yerr_in[ind]

        x_out=[]#N.array([],'float64')
        y_out=[]#N.array([],'float64')
        yerr_out=[]#N.array([],'float64')

        i=0; iright=1
        curr_y=y_in[0]
        curr_yerrsq=yerr_in[0]*yerr_in[0]
        xlen=N.shape(x_in)[0]
        count=1
        while i<xlen:
            curr_x=x_in[i]
            if i+1<xlen:
                if (x_in[i+1]-x_in[i])<eps:
                        curr_yerrsq=curr_yerrsq+yerr_in[i+1]*yerr_in[i+1]
                        curr_y=curr_y+y_in[i+1]
                        count=count+1.0
                else:
                    x_out.append(curr_x) #ok, we've reached the end of a run
                    y_out.append(curr_y/count)
                    yerr_out.append(N.sqrt(curr_yerrsq)/count) #normalize back to original monitor
                    curr_y=y_in[i+1]
                    curr_yerrsq=yerr_in[i+1]*yerr_in[i+1]
                    count=1.0
            else:
                x_out.append(curr_x) #deal with the endpoint
                y_out.append(curr_y/count)
                print 'count',count
                yerr_out.append(N.sqrt(curr_yerrsq)/count) #normalize back to original monitor
                count=1.0

            i=i+1
    if method=='interpolate':
        if step==None:
            step=min_step
        print 'xmin ',xmin
        print 'xmax ',xmax
        print 'step ',step
        x_out=N.arange(xmin,xmax,step,'float64')
        y_out=N.zeros(x_out.shape,'float64')
        yerr_out=N.zeros(x_out.shape,'float64')
        count=0
        for i in range(len(ylist)):
            yinterpolater=interpolate.interp1d(xlist[i],ylist_corrected[i],fill_value=0.0,kind='linear',copy=True,bounds_error=False)
            y_interpolated=yinterpolater(x_out)
            yerrinterpolater=interpolate.interp1d(xlist[i],yerrlist_corrected[i]*yerrlist_corrected[i],fill_value=0.0,kind='linear',copy=True,bounds_error=False)
            yerr_interpolatedsq=yerrinterpolater(x_out)
            y_out=y_out+y_interpolated
            yerr_outsq=yerr_out+yerr_interpolatedsq
            count=count+1
        yerr_out=N.sqrt(yerr_outsq)/count
        y_out=y_out/count
    x_out=N.array(x_out,'float64')
    y_out=N.array(y_out,'float64')
    yerr_out=N.array(yerr_out,'float64')
    return x_out,y_out,yerr_out

def print_arr(arrlist):
    for i in range((arrlist[0].shape[0])):
        s=''
        for j in range(len(arrlist)):
            s=s+'%3.2f'%(arrlist[j][i])+' '
        print s
    return

if __name__=='__main__':
    step=0.1
    x1=N.arange(-2,2+step,step)
    center=0
    width=1.0
    area=1.0e3*N.sqrt(2*pi)/width
    background=0.0
    monlist=[200,200]
    p1=[area,center,width,background]
    y1=gauss(x1,p1)
    y1err=N.sqrt(y1)
    step=2*step/4
    x2=N.arange(-2,2+step,step)
    p2=[area*monlist[1]/monlist[0],center,width,background]
    y2=gauss(x2,p2)
    y2err=N.sqrt(y2)
    #print 'orig'
    #print 'one'
    #print_arr([x1,y1])
    #print 'two'
    #print_arr([x2,y2])
    xlist=[x1,x2]
    ylist=[y1,y2]
    yerrlist=[y1err,y2err]
    monitor=400
    if 0:
        y1interpolater=interpolate.interp1d(x1,y1,fill_value=0.0,kind='linear',copy=True)
        y1_interpolated=y1interpolater(x2)
        y1errinterpolater=interpolate.interp1d(x1,y1err*y1err,fill_value=0.0,kind='linear',copy=True)
        y1err_interpolated=N.sqrt(y1errinterpolater(x2))
        print y1err_interpolated
        fig=pylab.figure(figsize=(8,8))
        fig.add_subplot(1,2,1)
        pylab.errorbar(x1,y1,y1err,marker='s',linestyle='None',mfc='blue')
        fig.add_subplot(1,2,2)
        pylab.errorbar(x2,y1_interpolated,y1err_interpolated,marker='s',linestyle='None',mfc='red')
        pylab.show()
        #print_arr([x2,y2,y1_interpolated])


        exit()
##    print 'in'
##    ylist_norm,yerrlist_norm=monitor_normalize(ylist,yerrlist,monlist)
##    #print ylist_norm
##    print 'one'
##    print_arr([x1,y1,y1err,ylist_norm[0],yerrlist_norm[0]])
##    print 'two'
##    print_arr([x2,y2,y2err,ylist_norm[1],yerrlist_norm[1]])
##    #exit()
##    print 'out'
    xout,yout,yerrout=simple_combine(xlist,ylist,yerrlist,monlist,method='interpolate')
#    print_arr([xout,yout,yerrout])
    #print yout
    #print yerrout
    if 1:
        fig=pylab.figure(figsize=(8,8))
        ylim=(y1.min(),y1.max())
        xlim=(x1.min(),x1.max())
        #ax.set_ylabel(ylabel)
        #ax.set_xlabel(xlabel)
        ax=fig.add_subplot(1,2,1)
        ax.errorbar(x1,y1,y1err,marker='s',mfc='blue',linestyle='None')
        ax.errorbar(x2,y2,y2err,marker='s',mfc='red',linestyle='None')
        ax.set_ylim(ylim); ax.set_xlim(xlim)
        ax3=fig.add_subplot(1,2,2)
        ax3.errorbar(xout,yout,yerrout,marker='s',mfc='blue',linestyle='None')
        ax3.set_ylim(ylim); ax3.set_xlim(xlim)
        pylab.show()