from dataflow import core, modules, config, calc, wireit
from dataflow.modules import join


joinMod = join.join_module()
joinMod.id = 'joinMod'
core.register_module(joinMod)

# 3 join mods
joinMod_d1 = dict(module='joinMod',version='0.0', config=[], position=[20,40])
joinMod_d2 = dict(module='joinMod',version='0.0', config=[], position=[20,60])
joinMod_d3 = dict(module='joinMod',version='0.0', config=[], position=[40,50])

# 2 wires
wire1 = dict(source=[0,'output'], target=[2,'input'])
wire2 = dict(source=[1,'output'], target=[2,'input'])

a = core.Template('testy','Template Testing', [joinMod_d1, joinMod_d2, joinMod_d3], [wire1, wire2], 'tas')


#wire_it diagram
f = open('wireit_diagram.txt', 'w')

f.write(str(wireit.template_to_wireit_diagram(a)))
f.close()

