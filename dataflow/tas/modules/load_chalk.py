"""
Load Chalk River TripleAxis data sets.
"""
import os

from reduction.tas import data_abstraction

from ... import config
from ...core import Module

from ..datatypes import TAS_DATA

def load_chalk_module(id=None, datatype=None, action=None,
                version='0.0', fields={}, xtype='WireIt.Container', **kwargs):
    """Module for loading a dataset for Chalk River: .aof and .acf files"""

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
             description='data',
             ),
    ]

    fields = { 
        'h1': {
            "type": "float",
            "label":"orient1 h",
            "name": "h1",
            "value": None,
        },
        'k1': {
            "type": "float",
            "label":"orient1 k",
            "name": "k1",
            "value": None,
        },
        'l1': {
            "type": "float",
            "label":"orient1 l",
            "name": "l1",
            "value": None,
        },
        'h2': {
            "type": "float",
            "label":"orient2 h",
            "name": "h2",
            "value": None,
        },
        'k2': {
            "type": "float",
            "label":"orient2 k",
            "name": "k2",
            "value": None,
        },
        'l2': {
            "type": "float",
            "label":"orient2 l",
            "name": "l2",
            "value": None,
        },
        'chalk_files': {
            "type": "files",
            "label": "Add your .AOF file and corresponding .ACF file and/or .LOG file.",
            "name": "chalk_files",
            "value": [],
        }      
    }
    
   
    # Combine everything into a module.
    module = Module(id=id,
                  name='Chalk River Load',
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


def _load_chalk_data(aof_filename, orient1, orient2, acf_filename=None):
    #(dirName, fileName) = os.path.split(name)
    #friendlyName = get_friendly_name(fileName)

    return data_abstraction.chalk_filereader(aof_filename, orient1, orient2, acf_filename=acf_filename)

def load_chalk_action(chalk_files=[], h1=None, k1=None, l1=None, h2=None, k2=None, l2=None, **kwargs):

    print "loading chalk river"
    result = []
    orient1 = []
    orient2 = []
    aof_filename = None
    aof_file = None
    acf_filename = None
    acf_file = None
    log_filename = None
    log_file = None

    try:
        h1 = kwargs['fields']['h1']['value']
        k1 = kwargs['fields']['k1']['value']
        l1 = kwargs['fields']['l1']['value']
        h2 = kwargs['fields']['h2']['value']
        k2 = kwargs['fields']['k2']['value']
        l2 = kwargs['fields']['l2']['value']
        orient1 = [h1, k1, l1]
        orient2 = [h2, k2, l2]
    except:
        #TODO Throw error! orient1 and orient2 MUST be given!
        pass
    # The .AOF file may be linked with a .ACF file and a .LOG file.
    # ASSUMPTION: the filename of these files are the same!!!
    # The first .AOF, .ACF, or .LOG found will determine this shared filename.
    for i, f in enumerate(chalk_files):
        if aof_filename and acf_filename and log_filename:
            #if the datafiles were already found, break loop
            break

        fileName, fileExt = os.path.splitext(f) # capitalization matters for the filename!
        fileExt = fileExt.lower()
        if not aof_filename and fileExt == '.aof':

            if (not acf_filename and not log_filename) or \
               (acf_filename and acf_filename == fileName) or \
               (log_filename and log_filename == fileName):
                aof_filename = fileName
                aof_file = f

        elif not acf_filename and fileExt == '.acf':

            if (not aof_filename and not log_filename) or \
               (aof_filename and aof_filename == fileName) or \
               (log_filename and log_filename == fileName):
                acf_filename = fileName
                acf_file = f

        elif not log_filename and fileExt == '.log':

            if (not aof_filename and not acf_filename) or \
               (aof_filename and aof_filename == fileName) or \
               (acf_filename and acf_filename == fileName):
                log_filename = fileName
                log_file = f


    #improve reader so it will include .log files!
    #result should be a list of TripleAxis objects
    result = _load_chalk_data(aof_file, orient1, orient2, acf_filename=acf_file)

    return dict(output=result)

load_chalk = load_chalk_module(id='tas.loadchalk', datatype=TAS_DATA,
                   version='1.0', action=load_chalk_action,)


