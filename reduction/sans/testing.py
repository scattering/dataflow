from matplotlib import pyplot as plt
from .data import readNCNRData
from ReductionCode import convertMonitor



if __name__ == '__main__':
    
    data,metadata = readNCNRData("MAY06001.SA3_CM_D545")
    newdata = convertMonitor(data,metadata)
    print newdata
    plt.figure()
    plt.imshow(newdata)
    plt.show()