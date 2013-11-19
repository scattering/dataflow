import sys
import h5py
import os
from numpy import savetxt, max, min
import zipfile
import tempfile
import simplejson
import copy

DEBUG = False

file_in = sys.argv[1]
file_out = file_in + '.zip'

def make_dir(path):
    os.mkdir(path)

join_path = os.path.join

def make_metadata(obj, path=''):
    metadata = {}
    for key in obj.keys():
        new_path = join_path(path, key)
        newitem = dict(obj[key].attrs)
        if isinstance(obj[key], h5py.Group):
            newitem['members'] = make_metadata(obj[key], new_path)
        else:
            fname = join_path(path, key+'.dat')
            if max(obj[key].shape) <= 1:
                newitem['value'] = obj[key].value.tolist()
        metadata[key] = newitem
    return metadata

def to_zipfile(obj, zipfile, path=''):
    for key in obj.keys():
        new_path = join_path(path, key)
        if isinstance(obj[key], h5py.Group):
            to_zipfile(obj[key], zipfile, new_path)
        else:
            fname = join_path(path, key+'.dat')
            # some members are empty... skip them.
            if sum(obj[key].shape) == 0:
                continue
            value = obj[key].value
            formats = {
                'S': '%s', 
                'f': '%.8g',
                'i': '%d',
                'u': '%d' }
            if value.dtype.kind in formats:
                fd, fn = tempfile.mkstemp()
                os.close(fd) # to be opened by name
                if DEBUG: print fname, value.dtype.kind
                if len(value.shape) > 2:
                    with open(fn, 'w') as f:
                        simplejson.dump(value.tolist(), f)
                else:
                    savetxt(fn, value, delimiter='\t', fmt=formats[value.dtype.kind])
                zipfile.write(fn, fname)
                os.remove(fn)
            else:
                print "unknown type of array: ", fname, value.dtype

def to_zip(hdfname, zipname='data.zip'):
    obj = h5py.File(hdfname)
    z = zipfile.ZipFile(zipname, 'w', compression=zipfile.ZIP_DEFLATED)
    to_zipfile(obj, z)
    metadata = make_metadata(obj)
    fd, fn = tempfile.mkstemp()
    os.close(fd) # to be opened by name
    with open(fn, 'w') as f:
        simplejson.dump(metadata, f, indent='  ')
    z.write(fn, '.metadata')
    os.remove(fn)
    z.close()

if __name__ == '__main__':
    import sys
    file_in = sys.argv[1]
    file_out = file_in + '.zip'
    to_zip(file_in, file_out)

