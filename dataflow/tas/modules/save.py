
from ...modules.save import save_module
from ..datatypes import TAS_DATA


def save_action(input, ext=None, xtype=None, position=None, **kwargs):
    # Note that save does not accept inputs from multiple components, so
    # we only need to deal with the bundle, not the list of bundles.
    # This is specified by terminal['multiple'] = False in modules/save.py
    for f in input: _save_one(f, ext)
    return {}

def _save_one(input, ext):
    #TODO - make a real save... this is a dummy
    outname = input.meta_data.filename
    # TODO: if ext is None, then infile will be overwritten
    if ext is not None:
        outname = ".".join([os.path.splitext(outname)[0], ext])
    print "saving", input.meta_data.filename, 'as', outname
    #save_data(input, name=outname)

fields = {'ext': {
    "type":"string",
    "label": "Save extension",
    "name": "ext",
    "value": ""
    }
}
save = save_module(id='tas.save', datatype=TAS_DATA,
                   version='1.0', action=save_action,
                   fields=fields)
save.xtype = 'SaveContainer'

