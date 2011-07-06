"""
Run a reduction workflow.

The function run_template
"""

from pprint import pprint
from inspect import getsource
from .core import lookup_module
import hashlib

TEMP_DATABASE = {} # Fake database
def run_template(template, config):
    """
    Evaluate the template using the configured values.

    *template* is a :class:`dataflow.core.Template` structure representing 
    the computation.
    
    *config* is a dictionary, with config[node] containing the values for
    the fields and input terminals at each node in the template.  
    Note: this version keeps all intermediates, and so isn't suitable for
    large data sets.
    """
    all_results = {}
    fingerprints = {}
    for nodenum, wires in template:
        # Find the modules
        node = template.modules[nodenum]
        module_id = node['module'] #template.modules[node]
        module = lookup_module(module_id)
        inputs = _map_inputs(module, wires)
        # substitute values for inputs
        kwargs = dict((k, _lookup_results(all_results, v)) 
                      for k, v in inputs.items())
        
        # Include configuration information
        kwargs.update(node.get('config', {}))
        kwargs.update(config[nodenum])
        
        # ===== Fingerprinting ======
        fp = finger_print(module, kwargs.copy(), nodenum, inputs.get('input', []), fingerprints)
        print "Fingerprint:", fp
        fingerprints[nodenum] = fp
        # Primary    test (hash of save module): 27382ab541bb982f763f05c7fc96056bf93acce7 initial test
        # Secondary  test (hash of save module): 27382ab541bb982f763f05c7fc96056bf93acce7 correct; identical
        # Tertiary   test (hash of save module): 838b609198c1183aefa05fdb359abea8faad08f2 correct; offset was changed from 0.1 to 0.2
        # Quaternary test (hash of save module): 838b609198c1183aefa05fdb359abea8faad08f2 correct; identical
        # ======= End fingerprinting =========
        
        if TEMP_DATABASE.get(nodenum, "") == fp:
            result = TEMP_DATABASE[fp]
        else:
            result = module.action(**kwargs)
        TEMP_DATABASE[nodenum] = fp
        TEMP_DATABASE[fp] = result

        #print result
        all_results[nodenum] = result
    return all_results
# FIXXXXXXXXXXXXXXXXXXXXXX ***********************
 #   from .offspecular.instruments import convert_to_plottable
 #   return [convert_to_plottable(value['output'])  if 'output' in value else {} for key, value in all_results.items()]


def _lookup_results(result, s):
    # Hack to figure out if we have a bundle.  Fix this!
    try:
        return [result[n][t] for n, t in s]
    except:
        try:
            return result[s[0]][s[1]]
        except:
            return None


def _map_inputs(module, wires):
    """
    Figure out which wires go to which input terminals.

    *module* : Module

    *wires* : [TemplateWire]

    Returns { id : None | source | [source, ...] }.

    id will range over the set of input terminals.

    source is a pair (int, string) giving the node number of the
    connecting terminal and its terminal name.
    """
    kwargs = {}
    for terminal in module.terminals:
        if terminal['use'] != "in": continue

        collect = [w['source'] for w in wires if w['target'][1] == terminal['id']]
        if len(collect) == 0:
            if terminal['required']:
                raise TypeError("Missing input for %s.%s"
                                % (module.id, terminal['id']))
            elif terminal['multiple']:
                kwargs[terminal['id']] = collect
            else:
                kwargs[terminal['id']] = None
        elif terminal['multiple']:
            kwargs[terminal['id']] = collect
        elif len(collect) > 1:
            raise TypeError("Excess input for %s.%s"
                            % (module.id, terminal['id']))
        else:
            kwargs[terminal['id']] = collect[0]
    return kwargs


def finger_print(module, args, nodenum, input_arr, fingerprints):
    d = module.__dict__.copy() # get all attributes
    d['action'] = getsource(d['action']) # because it is a python module (must convert it)
    fp = str(d) # source code (not 100% due to helper methods)
    # if load module or not is needed
    #fp += "\nLoad module" if len(module.terminals) == 1 and module.terminals[0]['id'] != 'input' else "Not a load module"
    if 'input' in args:
        del args['input'] # holds the MetaArray (don't want all that data)
    fp += str(args) # shortened arguments
    fp += str(nodenum) # node number
    if len(input_arr) > 0: # bundle correction
        if type(input_arr[0]) == type([]):
            fp += str([fingerprints[input[0]] for input in input_arr if 'output' == input[1]])
        elif type(input_arr[0]) == type(0) and input_arr[1] == 'output':
            fp += str([fingerprints[input_arr[0]]]) # might as well keep the list format
        else:
            raise TypeError("Input array should either be a bundle of modules or just one module")
    else:
        fp += str(input_arr) # '[]'
    fp = hashlib.sha1(fp).hexdigest()
    return fp
