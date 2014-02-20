import os
import types

from reduction.offspecular import filters

from ...modules.load import load_module

from ..datatypes import OSPEC_DATA, get_friendly_name

# Load UXD module
def load_uxd_action(input=[], files=[], intent='', **kwargs):
    print "loading", files

    result = []
    for i, f in enumerate(files):
        subresult = _load_uxd_data(f)
        if type(subresult) == types.ListType:
            result.extend(subresult)
        else:
            result.append(subresult)
    for subresult in input:
        if type(subresult) == types.ListType:
            result.extend(subresult)
        else:
            result.append(subresult)
        #result = [_load_data(f, auto_PolState, PolStates.get(get_friendly_name(os.path.split(f)[-1]), '')) for f in files] # not bundles
    return dict(output=result)

def _load_uxd_data(name):
    (dirName, fileName) = os.path.split(name)
    friendly_name = get_friendly_name(fileName)
    return filters.LoadUXDData(fileName, friendly_name=friendly_name, path=dirName)

load_uxd = load_module(id='ospec.uxd.load', datatype=OSPEC_DATA, version='1.0', action=load_uxd_action, filterModule = filters.LoadUXDData)
