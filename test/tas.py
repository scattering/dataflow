import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json

from dataflow.tas.instruments import BT7
from dataflow.wireit import (instrument_to_wireit_language, 
                           instrument_to_wireit_menu,
                           template_to_wireit_diagram,
                           wireit_diagram_to_template,
                           template_list,
                           )
from dataflow.core import Template, register_instrument

register_instrument(BT7)
modules = [
    dict(module="tas.load", position=(5,20), 
         config={'files': [], 'intent': 'signal'}),
    dict(module="tas.join", position=(160,20), 
         config={'align': ['A3']}),
    dict(module="tas.scale", position=(280,40), config={'scale': 2.5}),
    dict(module="tas.save", position=(340,40)),
    ]
wires = [
    dict(source=[0,'output'], target=[1,'input']),
    dict(source=[1,'output'], target=[2,'input']),
    dict(source=[2,'output'], target=[3,'input']),
    ]

template = Template(name='test tas',
                    description='example TAS diagram',
                    modules=modules,
                    wires=wires,
                    instrument=BT7.id,
                    )

print "== instrument\n",json.dumps(instrument_to_wireit_language(BT7))
print "== menu\n",instrument_to_wireit_menu(BT7)


tjson = json.dumps(template_to_wireit_diagram(template))
print "== diagram\n",tjson
t = wireit_diagram_to_template(json.loads(tjson),instrument=BT7)
print "== template\n",t.name, ":", t.description
print t.modules
print t.wires

open("../www/instrument/BT7definition.json",'w').write(json.dumps(instrument_to_wireit_language(BT7)))
open("../www/instrument/BT7menu.json","w").write(json.dumps(instrument_to_wireit_menu(BT7)))
open("../www/diagram/BT7example.json","w").write(json.dumps(template_to_wireit_diagram(template)))
open("../www/listWirings","w").write(json.dumps(template_list([template])))

