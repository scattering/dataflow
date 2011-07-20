import struct
import sys,os

def map_pics(key):
    """
Generate the mapping between files and their roles
"""
    
    datadir=os.path.join(os.path.dirname(os.path.abspath(__file__)),'static/img/SANS')
    filedict={'initial':os.path.join(datadir,'initial_correction_image.png'),
              'deadtime':os.path.join(datadir,'deadtime.png'),
              'trans':os.path.join(datadir,'gen_trans_image.png'),
              'div':os.path.join(datadir,'div_image.png'),
              'abs':os.path.join(datadir,'abs_image.png'),
              'oned':os.path.join(datadir,'annular1.png'),

              }
    return filedict[key]
#def map_pics(key):
    #"""
#Generate the mapping between files and their roles
#"""
    
    #datadir=os.path.join(os.path.dirname(__file__),'Sans_icons')
    #filedict={'initial':'SANS/initial_correction.png',
	      #'abs':'SANS/abs.png',
	      #'div':'SANS/div.png',	
	      #'ann1':'SANS/annular1.png',
	      #'ann2':'SANS/annular2.png',
     
              #}
    #return filedict[key]
#if __name__ == '__main__':

    
    
    