"""
Normalize Monitors (not blocked beam file)
"""
import reduction.sans.filters as red

from ... import config
from ...core import Module

from ..datatypes import SANS_DATA, xtype

def monitor_normalize_module(id=None, datatype=None, action=None,
                 version='0.0', fields={}, **kwargs):
    """Normalize Monitors"""

    icon = {
        'URI': config.IMAGES + "monitor_normalize.png",
        'terminals': {
            'input': (0, 10, -1, 0),
            'output': (20, 10, 1, 0),
        }
    }
    
    terminals = [
        dict(id='input',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=True,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='monitor normalized',
             ),
    ]

    # Combine everything into a module.
    module = Module(id=id,
                  name='monitor_normalize',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  **kwargs
                  )

    return module

def monitor_normalize_action(input=None):

#np.set_printoptions(edgeitems = 128)
#print "input",input
##flat = []

#file = open("/home/elakian/sansdata2.dat","w")

#x = monitor_normalize(input[0][0])
#file.write(repr(x.data.x))

#file.close()

#for bundle in input:
#flat.extend(bundle)
    x = 0
    #print "size: ", len(input[0])
    #result = []
    #for f in input:
    #result= [monitor_normalize(input[0][x])]
    #x+=1
    result = [red.monitor_normalize(f) for f in input[0]]
    print "result: ", result
    return dict(output=result)
monitor_normalize = monitor_normalize_module(id='sans.monitor_normalize', datatype=SANS_DATA, version='1.0', action=monitor_normalize_action, xtype=xtype)

