import json
import pickle

from reduction.offspecular import filters
from reduction.offspecular.he3analyzer import He3AnalyzerCollection
from reduction.offspecular.FilterableMetaArray import FilterableMetaArray

from ..core import Data

class PlottableDict(dict):
    def get_plottable(self):
        return json.dumps({})
    def dumps(self):
        return pickle.dumps(self)
    @classmethod
    def loads(cls, str):
        return pickle.loads(str)

use_File = True
def get_friendly_name(fh):
    if use_File:
        from apps.tracks.models import ResultFile
        return ResultFile.objects.get(name=str(fh)).friendly_name
    return fh

OSPEC_DATA = 'ospec.data2d'
data2d = Data(OSPEC_DATA, FilterableMetaArray, loaders=[
    {'function':filters.LoadICPMany, 'id':'LoadICPData'},
    {'function':filters.LoadAsterixMany, 'id':'LoadAsterix'},
    {'function':filters.LoadUXDMany, 'id': 'LoadUXD'}])
#ast_data2d = Data('ospec.asterix.data2d', FilterableMetaArray, loaders=[{'function':LoadAsterixMany, 'id':'LoadAsterix'}])
OSPEC_DATA_HE3 = OSPEC_DATA + '.he3'
datahe3 = Data(OSPEC_DATA_HE3, He3AnalyzerCollection, loaders=[{'function':He3AnalyzerCollection, 'id':'LoadHe3'}])
OSPEC_DATA_TIMESTAMP = OSPEC_DATA + '.timestamp'
datastamp = Data(OSPEC_DATA_TIMESTAMP, PlottableDict, loaders=[])

def LoadTimestamps(filename, friendly_name="", path=""):
    fn = os.path.join(dirName, filename)
    return PlottableDict(json.load(open(fn, 'r')))

datastamp.loaders.append({'function':LoadTimestamps, 'id':'LoadTimeStamps'})

