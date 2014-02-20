import os

from reduction.common.annotate_exception import annotate_exception
import reduction.sans.filters as red
from ...modules.load import load_module
from ..datatypes import SANS_DATA

# Load module
def load_action(files=[], intent='', **kwargs):
    #print "loading", files
    result = [_load_data(f) for f in files]  # not bundles
    #print "Result: ", result
    return dict(output=result)
def _load_data(name):
    #print name
    #friendly_name = ResultFile.objects.get(name=name.split('/')[-1]).friendly_name
    try:
        if name.upper().endswith(".DIV"):
            return red.read_div(myfilestr=name)
        else:
            return red.read_sample(myfilestr=name)
    except:
        annotate_exception("when opening %r"%name)
        raise

load = load_module(id='sans.load', datatype=SANS_DATA, version='1.0',
                   action=load_action)
