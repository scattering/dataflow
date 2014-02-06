from struct import unpack

def R4toFloat(vaxasstring):
	"""Takes a 4 character string represention of a VAX REAL*4 from struct.unpack
           and returns a python float"""	

	if ord(vaxasstring[1]) == 0:
		ieeeasstring = vaxasstring[2]+vaxasstring[3]+vaxasstring[0]+vaxasstring[1]
		return unpack('<f',ieeeasstring)[0]
	else:
		ieeeasstring = vaxasstring[2]+vaxasstring[3]+vaxasstring[0]+chr(ord(vaxasstring[1])-1)
		return unpack('<f',ieeeasstring)[0]
