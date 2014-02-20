import types

from reduction.offspecular import filters

from ...modules.load import load_module

from ..datatypes import OSPEC_DATA, get_friendly_name

# Load module
def load_action(input=[], files=[], intent='', auto_PolState=False, PolStates=[], **kwargs):
    print "loading", files

    result = []
    for i, f in enumerate(files):
        subresult = _load_data(f, auto_PolState, (PolStates[i] if i<len(PolStates) else ""))
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

def _load_data(name, auto_PolState, PolState):
    (dirName, fileName) = os.path.split(name)
    friendly_name = get_friendly_name(fileName)
    return filters.LoadICPData(fileName, friendly_name=friendly_name, path=dirName, auto_PolState=auto_PolState, PolState=PolState)

auto_PolState_field = {
    "type":"boolean",
    "label": "Auto-polstate",
    "name": "auto_PolState",
    "value": False,
    }
autochain_loader_field = {
    "type":"boolean",
    "label": "Cache individual files",
    "name": "autochain-loader",
    "value": False,
    }

PolStates_field = {
    "type":"string",
    "label": "PolStates",
    "name": "PolStates",
    "value": "",
    }

load = load_module(id='ospec.load', datatype=OSPEC_DATA,
                   version='1.0',
                   #action=load_action,
                   #fields=OrderedDict({'files': {}, 'autochain-loader':autochain_loader_field, 'auto_PolState': auto_PolState_field, 'PolStates': PolStates_field}),
                   filterModule=filters.LoadICPData)


