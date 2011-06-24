"""
Sample data from NCNR-AND/R.

This is area detector data with all frames preserved.

from reflectometry.model1d.examples.cg1area import data

TODO: Document contents of this data file.
"""

import numpy, os, sys, pylab
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from formats import load

PATH = os.path.dirname(os.path.realpath(__file__))
print PATH
#data = load(os.path.join(PATH, 'psdca022.cg1.gz'))
#data = load(os.path.join(PATH, 'Ipsdca022.cg1'))
data = load(os.path.join(PATH, 'small.cg1'))
if __name__ == '__main__':
    print "shape=", data.detector.counts.shape
    pylab.imshow(numpy.log(data.detector.counts[1] + 1).T)
    #pylab.pcolor(numpy.log(data.detector.counts+1))
    pylab.show()
