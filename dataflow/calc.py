"""
Run a reduction workflow.

The function run_template
"""

from pprint import pprint
from inspect import getsource
from .core import lookup_module, lookup_datatype
import hashlib, redis

# temp
from ..reduction.offspecular.FilterableMetaArray import FilterableMetaArray

server = redis.Redis("localhost")
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
        
        fp = finger_print(module, kwargs.copy(), nodenum, inputs.get('input', []), fingerprints)
        fingerprints[nodenum] = fp
        fp = name_fingerprint(fp)
        print fp
        
        # Overwrite even if there was already the same reduction?
        if server.exists(fp):# or module.name == 'Save': 
            datatype = None
            for terminal in module.terminals:
                if terminal['id'] == 'output':
                    datatype = terminal['datatype']
                    break
            cls = lookup_datatype(datatype).cls
            result = dict(output=[cls.loads(str) for str in server.lrange(fp, 0, -1)])
            #result = dict(output=[FilterableMetaArray.loads(str) for str in server.lrange(fp, 0, -1)])
        else:
            result = module.action(**kwargs)
            for arr in result.get('output', []):
                server.rpush(fp, arr.dumps())
        all_results[nodenum] = result
    
    # retrieve plottable results
    ans = []
    for nodenum, result in all_results.items():
        fp = name_plottable(fingerprints[nodenum])
        plottable = {}
        if 'output' in result:
            if server.exists(fp):
                plottable = dict(output=server.lrange(fp, 0, -1))
            else:
                plottable = convert_to_plottable(result['output'])
                for str in plottable['output']:
                    server.rpush(fp, str)
        ans.append(plottable)
    return ans


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
    # need access to Combine() and CoordinateOffset() source (e.g.)
    d['action'] = getsource(d['action']) # because it is a python method object (must convert it)
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

def convert_to_plottable(result):
    print "Starting new converter"
    return dict(output=[data.get_plottable() for data in result])
def name_fingerprint(fp):
    return "Fingerprint:" + fp
def name_plottable(fp):
    return "Plottable:" + fp
