import os

from ... import config
from ...modules.save import save_module
from ..datatypes import OSPEC_DATA

# Save module
def save_action(input=[], ext=None, **kwargs):
    for index, f in enumerate(input): _save_one(f, ext, index) # not bundles
    return {}
def _save_one(input, ext, index):
    default_filename = "default.cg1"
    # modules like autogrid return MetaArrays that don't have filenames
    outname = initname = input._info[-1]["path"] + "/" + input._info[-1].get("filename", default_filename)
    if ext is not None:
        outname = ".".join([os.path.splitext(outname)[0] + str(index), ext])
    print "saving", initname, 'as', outname
    input.write(outname)

save = save_module(id='ospec.save', datatype=OSPEC_DATA,
                   version='1.0', action=None)
save.xtype = 'SaveContainer'
save.image = config.IMAGES + config.ANDR_FOLDER + "save_image.png"

