#Translation triple_axis_corrections_idl.txt into python


import data_abstraction as D
import readncnr3 as R
import numpy as N


def readFile(filename):
    "Constructs and returns a metadata dictionary and data dictionary from a given data file"
    #JUST FOR TESTING --> use readncnr3.py
    datafile = open(filename)
    
    metadata = {}
    data = {}
    data_keys = []
    while 1:
        line = datafile.readline().strip()
        # If the file is done 
        if not line:               
            break

        # If the line gives the data column headers
        if line.startswith("#Columns"):
            data_keys = line.split()
            data_keys.remove("#Columns")
            for key in data_keys:
                data[key] = []

        # If the line is commented; handling metadata
        elif line.startswith("#"):  
            line = line[1:]     #remove the '#'
            linearr = line.split()
            metadata_key = linearr.pop(0)
            if len(linearr) == 0:
                # if there is no data for a certain metadata tag, add None to its mapping value
                #   for ease when converting to the data_abstraction structure
                linearr.append(None)
            metadata[metadata_key] = linearr

        #handling data
        else:
            temp = line.split()
            i = 0
            for key in data_keys:
                data.get(key).append(temp[i])
                i += 1

    return metadata, data


def establish_correction_coefficients(filename):
    "Obtains the instrument-dependent correction coefficients from a given file and \
     returns them in a dictionary, coefficients"
    datafile = open(filename)

    coefficients = {} # Dictionary of instrument name mapping to its array of M0 through M4
    while 1:
        line = datafile.readline().strip()
        if not line:
            break
        elif len(line) != 0:
            #if it's not an empty line, thus one with data
            if not line.startswith("#"):
                #if it's not a comment/headers, i.e. actual data
                linedata = line.split()
                instrument = linedata.pop(0)
                coefficients[instrument] = linedata

    return coefficients



def harmonic_monitor_correction(data):
    # Use for constant-Q scans with fixed scattering energy, Ef  

    M = establish_correction_coefficients(monitor_correction_coordinates.txt)
    for i in len(data.get(Ei)):
        Eii = data.get(Ei)[i]
        data.get('Detector')[i] *= (M[0] + M[1]*Eii + M[2]*Eii^2 + M[3]*Eii^3 + M[4]*Eii^4)
        
    #TODO - CHECK - apply the correction to the detector counts?



def normalize_monochromator(data):
    pass


def resolution_volume_correction(data):
    # Requires constant-Q scan with fixed incident energy, Ei
    pass
    #TODO - CHECK - taken from the IDL
    # resCor = Norm/(cot(A6/2)*Ef^1.5)
    # where Norm = Ei^1.5 * cot(asin(!pi/(0.69472*dA*sqrt(Ei))))
    '''
    for i in len(data.get(Ei))
        thetaA = N.radians(data.get(a6)[i]/2.0)
        arg = asin(N.pi/(0.69472*dA*sqrt(double(data.get(Ei)[i]))))
        norm = (Ei^1.5) / tan(arg)
        cotThetaA = 1/tan(thetaA)
        resCor = norm/(cotThetaA * (Ef^1.5))
    


    N.exp((ki/kf) ** 3) * (1/N.tan(thetaM)) / (1/N.cot(thetaA))
    '''

if __name__=="__main__":
    #Currently for testing purposes only
    #coeff = establish_correction_coefficients("monitor_correction_coordinates.txt")
    #print coeff

    #metadata, data = readFile("bt7 sample data.txt")
    #print metadata
    #print data
    
    myfilestr=r'EscanQQ7HorNSF91831.bt7'
    mydatareader=R.datareader()
    mydata=mydatareader.readbuffer(myfilestr)
    print mydata.data
    print mydata.metadata
