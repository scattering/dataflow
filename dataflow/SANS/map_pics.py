import struct
import sys,os


def map_pics(key):
    """
Generate the mapping between files and their roles
"""
    
    datadir=os.path.join(os.path.dirname(__file__),'Sans_icons')
    filedict={'initial':os.path.join(datadir,'initial_correction.png'),
	      'abs':os.path.join(datadir,'abs.png'),
	      'div':os.path.join(datadir,'div.png'),	
	      'ann1':os.path.join(datadir,'annular1.png'),
	      'ann2':os.path.join(datadir,'annular2.png'),
     
              }
    return filedict[key]
