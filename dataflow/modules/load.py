"""
Load data sets.
"""

import tarfile
import os

#from apps.tracks.models import File

from .. import config
from ..core import Module
from ..core import lookup_datatype

def load_action(files=[], **kwargs):
    print "loading files", files, kwargs
    result = []
    for filename in files:
        fileobj = File.objects.get(name=os.path.basename(filename))
        cls = lookup_datatype(fileobj.datatype).cls

        path = os.path.join(fileobj.location, fileobj.name)
        fid = tarfile.open(path, 'r:gz')
        result_objs = [fid.extractfile(member) for member in fid.getmembers()]
        result.extend([cls.loads(robj.read()) for robj in result_objs])        
        #result = [cls.loads(str) for str in server.lrange(terminal_fp, 0, -1)]
        #fp = fileobj.location
        #read_here = os.path.join(fp, fn)
        #result_str = gzip.open(read_here, 'rb').read()
        #result.append(cls.loads(result_str))
    #result = [FilterableMetaArray.loads(robj.read()) for robj in result_objs]
    return dict(output=result)

def load_module(id=None, datatype=None, action=load_action,
                version='0.0', fields={}, xtype='WireIt.Container', **kwargs):
    """Module for loading data from a raw datafile"""

    icon = {
        'URI': config.IMAGES + "load.png",
        'terminals': {
            'output': (20, 10, 1, 0),
        }
    }
   
    terminals = [
        #dict(id='input',
        #     datatype=datatype,
        #     use='in',
        #     description='data',
        #     required=False,
        #     multiple=True,
        #     ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='data',
             ),
    ]

    files_field = {
        "type":"files",
        "label": "Files",
        "name": "files",
        "value": [],
    }
    intent_field = {
        "type":"string",
        "label":"Intent",
        "name": "intent",
        "value": '',
    }
    
    fields.update({'files': files_field, 'intent': intent_field})
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Load Raw',
                  version=version,
                  description=action.__doc__,
                  #icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  xtype=xtype,
                  **kwargs
                  )

    return module
