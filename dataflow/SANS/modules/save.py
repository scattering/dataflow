import os

import reduction.sans.filters as red
from ...modules.save import save_module
from ..datatypes import SANS_DATA

def save_action(input=[], ext='', **kwargs):
    for f in input: _save_one(f, ext) # not bundles
    return {}
def _save_one(input, ext):
    outname = initname = red.map_files('save')
    if ext is not None:
        outname = ".".join([os.path.splitext(outname)[0], ext])
    print "saving", initname, 'as', outname
    with open(outname, 'w') as f:
        f.write(str(input.__str__()))
save = save_module(id='sans.save', datatype=SANS_DATA,
                   version='1.0', action=save_action, xtype="SaveContainer")

