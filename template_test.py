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

diag = wireit.template_to_wireit_diagram(core.Template('testy','Template Testing', [joinMod_d1, joinMod_d2, joinMod_d3], [wire1, wire2], 'tas'))
format_diag = ''
def diag_to_WireIt_str(diagram):
	underlying_module = core.lookup_module('joinMod')
	print underlying_module.icon	
	diag_str = ''
	
diag_to_WireIt_str(diag)

print diag
	

#wire_it diagram
f = open('wireit_diagram.txt', 'w')
for i in diag:
	format_diag += str(i).replace("'", '') + ": " + str(diag[i]) + ',\n \t'
#print format_diag
f.write(format_diag)
f.close()

