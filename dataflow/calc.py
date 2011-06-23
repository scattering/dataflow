"""
Run a reduction workflow.

The function run_template
"""

from pprint import pprint

from .core import lookup_module


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
        result = module.action(**kwargs)
        print result
        all_results[nodenum] = result
        
    return all_results

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

