"""
Run a reduction workflow.

The function run_template
"""

from pprint import pprint
from inspect import getsource
from .core import lookup_module, lookup_datatype
import hashlib, redis, types, os

os.system("redis-server") # ensure redis is running
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
        module_id = node['module'] # template.modules[node]
        module = lookup_module(module_id)
        inputs = _map_inputs(module, wires)
        
        # substitute values for inputs
        kwargs = dict((k, _lookup_results(all_results, v)) 
                      for k, v in inputs.items())
        
        # Include configuration information
        configuration = {}
        configuration.update(node.get('config', {}))
        configuration.update(config[nodenum])
        kwargs.update(configuration)
        
        # Fingerprinting
        fp = finger_print(module, configuration, nodenum, inputs, fingerprints) # terminals included
        fingerprints[nodenum] = fp
        fp = name_fingerprint(fp)
        print fp
        
        # Overwrite even if there was already the same reduction?
        if server.exists(fp):# or module.name == 'Save': 
            result = {}
            for terminal in module.terminals:
                if terminal['use'] == 'out':
                    cls = lookup_datatype(terminal['datatype']).cls
                    terminal_fp = name_terminal(fp, terminal['id'])
                    result[terminal['id']] = [cls.loads(str) for str in server.lrange(terminal_fp, 0, -1)]
        else:
            result = module.action(**kwargs)
            for terminal_id, res in result.items():
                terminal_fp = name_terminal(fp, terminal_id)
                for data in res:
                    server.rpush(terminal_fp, data.dumps())
            server.set(fp, fp) # used for checking if the calculation exists; could wrap this whole thing with loop of output terminals
        all_results[nodenum] = result
    # retrieve plottable results
    ans = {}
    for nodenum, result in all_results.items():
        fp = name_plottable(fingerprints[nodenum])
        plottable = {}
        for terminal_id, arr in result.items():
            terminal_fp = name_terminal(fp, terminal_id)
            if server.exists(terminal_fp):
                plottable[terminal_id] = server.lrange(terminal_fp, 0, -1)
            else:
                plottable[terminal_id] = convert_to_plottable(arr)
                for str in plottable[terminal_id]:
                    server.rpush(terminal_fp, str)
        ans[nodenum] = plottable
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

def finger_print(module, args, nodenum, inputs, fingerprints):
    """
    Create a unique sha1 hash for a module based on its attributes and inputs.
    """
    d = module.__dict__.copy() # get all attributes
    # need access to Combine() and CoordinateOffset() source (e.g.)
    d['action'] = getsource(d['action']) # because it is a python method object (must convert it)
    fp = str(d) # source code (not 100% due to helper methods)
    fp += str(args) # all arguments for the given module
    fp += str(nodenum) # node number
    for terminal_id, input_arr in inputs.items():
        fp += terminal_id
        if input_arr != None and isinstance(input_arr, list) and len(input_arr) > 0: # default value checking for non-required terminals
            if isinstance(input_arr[0], list): # Multiple = True; bundle
                fp += str([fingerprints[input[0]] for input in input_arr])
            elif isinstance(input_arr[0], int):  # Multiple = False; single input
                fp += str(fingerprints[input_arr[0]])
            else:
                raise TypeError("Input array should either be a bundle of inputs or just one input")
        else:
            fp += str(input_arr) # whatever the default value was
    fp = hashlib.sha1(fp).hexdigest()
    return fp

def convert_to_plottable(result):
    print "Starting new converter"
    return [data.get_plottable() for data in result]
def name_fingerprint(fp):
    return "Fingerprint:" + fp
def name_plottable(fp):
    return "Plottable:" + fp
def name_terminal(fp, terminal_id):
    return fp + ":" + terminal_id
