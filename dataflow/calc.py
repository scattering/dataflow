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

def calc_single(template, config, nodenum, terminal_id):
    """ Calculate fingerprint of terminal in question - if it exists in the cache,
    get it.  Otherwise, calculate from scratch (retrieving parent values recursively) """
    # Find the modules
    node = template.modules[nodenum]
    module_id = node['module'] # template.modules[node]
    module = lookup_module(module_id)
    terminal = module.get_terminal_by_id(terminal_id)
    
    if terminal['use'] != 'out':
        # then this is an input terminal... can't get it!
        return {}
    
    all_fp = fingerprint_template(template, config)
    fp = name_fingerprint(all_fp[nodenum])
    terminal_fp = name_terminal(fp, terminal_id)

    if server.exists(terminal_fp):
        print "retrieving cached value: " + terminal_fp
        cls = lookup_datatype(terminal['datatype']).cls
        result = [cls.loads(str) for str in server.lrange(terminal_fp, 0, -1)]
    else:
        # get inputs from parents
        parents = template.get_parents(nodenum)
        # this is a list of wires that terminate on this module
        kwargs = {}
        for wire in parents:
            source_nodenum, source_terminal_id = wire['source']
            source_data = calc_single(template, config, source_nodenum, source_terminal_id)
            target_id = wire['target'][1]
            if target_id in kwargs:
                # this explicitly assumes all data is a list
                # so that we can concatenate multiple inputs
                kwargs[target_id].append(source_data)
            else:
                kwargs[target_id] = source_data
        
        # Include configuration information
        configuration = {}
        configuration.update(node.get('config', {}))
        configuration.update(config[nodenum])
        kwargs.update(configuration)
        
        calc_value = module.action(**kwargs)
        # pushing the value of all the outputs for this node to cache, 
        # even though only one was asked for
        for terminal_id, arr in calc_value.items():
            terminal_fp = name_terminal(fp, terminal_id)
            for data in arr:
                server.rpush(terminal_fp, data.dumps())
        result = calc_value[terminal_id]
    return result

def get_plottable(template, config, nodenum, terminal_id):
    # Find the modules
    node = template.modules[nodenum]
    module_id = node['module'] # template.modules[node]
    module = lookup_module(module_id)
    terminal = module.get_terminal_by_id(terminal_id)
    
    all_fp = fingerprint_template(template, config)
    fp = all_fp[nodenum]
    plottable_fp = name_terminal(name_plottable(fp), terminal_id)
    
    if server.exists(plottable_fp):
        print "retrieving cached value: " + plottable_fp
        plottable = server.lrange(plottable_fp, 0, -1)
    else:
        data = calc_single(template, config, nodenum, terminal_id)
        plottable = convert_to_plottable(data)
        for item in plottable:
            server.rpush(plottable_fp, item)
            
    return plottable

def fingerprint_template(template, config):
    """ run the fingerprint operation on the whole template, returning
    the dict of fingerprints (one per output terminal) """    
    fingerprints = {}
    for nodenum, wires in template:
        # Find the modules
        node = template.modules[nodenum]
        module_id = node['module'] # template.modules[node]
        module = lookup_module(module_id)
        inputs = _map_inputs(module, wires)
        
        # Include configuration information
        configuration = {}
        configuration.update(node.get('config', {}))
        configuration.update(config[nodenum])
        
        # Fingerprinting
        fp = finger_print(module, configuration, nodenum, inputs, fingerprints) # terminals included
        fingerprints[nodenum] = fp
    return fingerprints

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
