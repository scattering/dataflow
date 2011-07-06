import struct
import sys,os


def map_pics(key):
    """
Generate the mapping between files and their roles
"""
    
    datadir=os.path.join(os.path.dirname(__file__),'Sans_icons')
    filedict={'initial':'SANS/initial_correction.png',
	      'abs':'SANS/abs.png',
	      'div':'SANS/div.png',	
	      'ann1':'SANS/annular1.png',
	      'ann2':'SANS/annular2.png',
     
              }
    return filedict[key]
