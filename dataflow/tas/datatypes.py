from ..core import Data
from reduction.tas import data_abstraction

TAS_DATA = 'data1d.tas'
xtype = 'AutosizeImageContainer'
data1d = Data(TAS_DATA, data_abstraction.TripleAxis,
              loaders=[{'function':data_abstraction.autoloader, 'id':'loadTAS'},
                       {'function':data_abstraction.chalk_autoloader, 'id':'loadChalkRiver'}])
