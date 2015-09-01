import numpy as np

def identify_duplicates(x,y,z):
    mylist=np.array(zip(x,y))
    unique,idx,idy=np.unique(mylist, return_index='True', return_inverse='True')
    mydict={}
    for i in range(0,len(idy),2):
        key=str(idy[i]/2)
        if mydict.has_key(key):
            mydict[key]['num']=mydict[key]['num']+1
            mydict[key]['val']=mydict[key]['val']+z[i/2]
        else:
            mydict[key]={'num':1,
                         'val':z[i/2],
                         'x':unique[idy[i]],
                         'y':unique[idy[i+1]]
                         }
    xo=np.zeros(len(unique)/2)                   
    yo=np.zeros(len(unique)/2)
    zo=np.zeros(len(unique)/2)
    for key in mydict.keys():
        zo[int(key)]=mydict[key]['val']/mydict[key]['num']
        xo[int(key)]=mydict[key]['x']
        yo[int(key)]=mydict[key]['y']
        
        
    return xo,yo,zo

if __name__=="__main__":
    x=[1, 3, 5, 1, 5, 7]
    y=[2, 4, 6, 2, 6, 8]
    z=[1.,2.,3.,4.,5.,6.]  
    xo,yo,zo=identify_duplicates(x,y,z)
    print zip(xo,yo,zo)
