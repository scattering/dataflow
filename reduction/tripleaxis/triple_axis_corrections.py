# TEST CLASS --> NOT IN USE (7/7/2011)

from . import data_abstraction as D
from . import readncnr3 as R

class Struct:
    "for converting dict into object for the setup_data_structure method"
    def __init__(self, **entries): 
        self.__dict__.update(entries)


def setup_data_structure(mydata):
    mydata.data = Struct(**mydata.data)
    #print mydata.metadata.keys()
    #mydata.metadata['monohorizfocus']=None
    #mydata.metadata['monovertifocus']=None
    #mydata.metadata['monochromator_dspacing']=None
    #mydata.metadata = Struct(**mydata.metadata)

    myTripleAxis = D.TripleAxis()
    myTripleAxis.translate_monochromator(mydata)
    myTripleAxis.translate_analyzer(mydata)
    myTripleAxis.translate_collimator(mydata)
    myTripleAxis.translate_apertures(mydata)
    myTripleAxis.translate_polarized_beam(mydata)
    myTripleAxis.translate_primary_motors(mydata)
    myTripleAxis.translate_physical_motors(mydata)
    myTripleAxis.translate_filters(mydata)
    myTripleAxis.translate_timestamp(mydata)
    myTripleAxis.translate_temperature(mydata)
    myTripleAxis.translate_slits(mydata)
    myTripleAxis.translate_sample(mydata)
    myTripleAxis.translate_metadata(mydata)
    myTripleAxis.translate_detectors(mydata)

    #mylattice = D.Lattice(a=d.get('a'), b=d.get('b'), c=d.get('c'), alpha=d.get('alpha'), beta=d.get('beta'), gamma=d.get('gamma'))


def harmonic_monitor_correction(data):
    # Use for constant-Q scans with fixed scattering energy, Ef
    # Multiplies the montior correction through all of the detectors in the Detector_Sets

    def establish_correction_coefficients(filename):
        "Obtains the instrument-dependent correction coefficients from a given file and \
         returns them in the dictionary called coefficients"
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


    M = establish_correction_coefficients("monitor_correction_coordinates.txt")
    #for i in len(data.get(Ei)):
    #    Eii = data.get(Ei)[i]
    #    data.get('Detector')[i] *= (M[0] + M[1]*Eii + M[2]*Eii^2 + M[3]*Eii^3 + M[4]*Eii^4)
        
    



def normalize_monochromator(data, targetmonitor):
    # 
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
    #print mydata.data.keys()
    #print mydata.data.get('lattice')
    setup_data_structure(mydata)
    #print mydata.data
    #print mydata.metadata
