from ..core import Data
import reduction.sans.filters as red

# Datatype
SANS_DATA = 'data2d.sans'
data2d = Data(SANS_DATA, red.SansData)
data1d = Data(SANS_DATA, red.plot1D)
datadiv = Data(SANS_DATA, red.div)
#Datatype(id=SANS_DATA,
#name='SANS Data',
#plot='sansplot')
#dictionary = Datatype(id='dictionary',
#name = 'dictionary',
#plot = None)

xtype="AutosizeImageContainer"


