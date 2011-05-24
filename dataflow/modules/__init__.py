"""
Common modules.

Module definition functions look like:

:Parameters:

*id* : string
    module identifier

*datatype* : string
    in/out data
    
*action* : f(input,scale,...) -> { 'output': data }
    function to scale the data
    
*version* : string
    major.minor version number of the action function
    
*fields* : [{'type': string, 'label': string, 'name': string, ...}, ...]
    additional fields required for the action.  These will be supplied
    to action as name=value items.  See http://neyric.github.com/inputex/
    for details on the form specification of the field.
    
:Returns: 

*module* | Module
    module definition
"""
