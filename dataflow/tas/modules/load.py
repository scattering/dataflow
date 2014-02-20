"""
Load a TripleAxis object from a datafile.
"""
import os.path
import types

from reduction.tas import data_abstraction

from ... import config
from ...core import Module
from ..datatypes import TAS_DATA

def load_module(id=None, datatype=None, action=None,
                version='0.0', fields={}, **kwargs):
    """Module for loading a TripleAxis object"""

    icon = {
        'URI': config.IMAGES + "load.png",
        'terminals': {
            'output': (20, 10, 1, 0),
        }
    }
    
    terminals = [
        dict(id='output',
             datatype=datatype,
             use='out',
             description='TripleAxis Object',
             ),
    ]

    fields['files'] = {
        "type":"files",
        "label": "Files",
        "name": "files",
        "value": '',
    }
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Load',
                  version=version,
                  description=action.__doc__,
                  #icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  **kwargs
                  )

    return module



# === Component binding ===
def get_friendly_name(fh):
    from apps.tracks.models import ResultFile
    return ResultFile.objects.get(name=str(fh)).friendly_name

def _load_data(name):
    #(dirName, fileName) = os.path.split(name)
    #friendlyName = get_friendly_name(fileName)
    return data_abstraction.filereader(name, friendly_name=os.path.basename(name))

def load_action(files=[], intent=None, position=None, xtype=None, **kwargs):
    """ was set up to load ONLY 1 file... might work for bundles now """
    #print "loading", files
    if not files: raise ValueError("No TAS files to load")
    result = []
    for i, f in enumerate(files):
        subresult = _load_data(f)
        if type(subresult) == types.ListType:
            result.extend(subresult)
        else:
            result.append(subresult)
    return dict(output=result)

################################################################################
# NOTE: 02/03/2012 bbm
# this is what was in "load_action" before
# it would clearly not work - the directory was hardcoded,
# and relied on a directory structure
# that will not exist on a typical machine (i.e. /home/brendan...)
#
# the replacement above is an adaptation of the loader code in
# dataflow.offspecular.instruments
################################################################################

load = load_module(id='tas.load', datatype=TAS_DATA, version='1.0',
                   action=load_action)
