from MetaArray import MetaArray
from numpy import ndarray, amin, amax, alen, array, fromstring
import copy, simplejson, datetime
from ...dataflow.core import Data
from cStringIO import StringIO

class FilterableMetaArray(Data, MetaArray):
    def __new__(*args, **kwargs):
        subarr = MetaArray.__new__(*args, **kwargs)
        return subarr
    
    def filter(self, filtername, *args, **kwargs):
        import filters
        return filters.__getattribute__(filtername)().apply(self, *args, **kwargs)

    
    def __deepcopy__(self, memo):
        return FilterableMetaArray(self.view(ndarray).copy(), info=self.infoCopy())

    def dumps(self):
        meta = { 'shape': self.shape, 'type': str(self.dtype), 'info': self.infoCopy()}
        assert isinstance(meta['info'], list)
        axstrs = []
        for ax in meta['info']:
            if ax.has_key('values'):
                axstrs.append(ax['values'].tostring())
                ax['values_len'] = len(axstrs[-1])
                ax['values_type'] = str(ax['values'].dtype)
                del ax['values']
        fd = StringIO()
        fd.write(str(meta) + '\n\n')
        for ax in axstrs:
            fd.write(ax)
        fd.write(self.tostring())
        ans = fd.getvalue()
        fd.close()
        return ans
    
    @classmethod
    def loads(cls, str):
        fd = StringIO(str)
        meta = ''
        while True:
            line = fd.readline().strip()
            if line == '':
                break
            meta += line
        meta = eval(meta)
        
        ## read in axis values
        for ax in meta['info']:
            if ax.has_key('values_len'):
                ax['values'] = fromstring(fd.read(ax['values_len']), dtype=ax['values_type'])
                del ax['values_len']
                del ax['values_type']
        
        subarr = fromstring(fd.read(), dtype=meta['type'])
        subarr = subarr.view(FilterableMetaArray)
        subarr.shape = meta['shape']
        subarr._info = meta['info']
        return subarr

    def get_plottable(self):
        array_out = self['Measurements':'counts']
        z = [array_out.tolist()]
        #zbin_base64 = base64.b64encode(array_out.tostring())
        #z = [arr[:, 0].tolist() for arr in self]
        dims = {}
        # can't display zeros effectively in log... set zmin to smallest non-zero
        zmin = array_out[array_out > 1e-10].min()
        dims['zmin'] = zmin
        dims['zmax'] = array_out.max()
        axis = ['x', 'y']
        for index, label in enumerate(axis):
            arr = self._info[index]['values']
            dims[axis[index] + 'min'] = amin(arr)
            dims[axis[index] + 'max'] = amax(arr)
            dims[axis[index] + 'dim'] = alen(arr)
            dims['d' + axis[index]] = arr[1] - arr[0]
        xlabel = self._info[0]['name']
        ylabel = self._info[1]['name']
        zlabel = self._info[2]['cols'][0]['name']
        title = 'AND/R data' # That's creative enough, right?
        type = '2d_image'
        transform = 'log' # this is nice by default
        dump = dict(type=type, z=z, title=title, dims=dims, xlabel=xlabel, ylabel=ylabel, zlabel=zlabel, transform=transform)
        res = simplejson.dumps(dump, sort_keys=True)
        return res
        
#    def get_plottable_new(self):
#        array_out = self['Measurements':'counts']
#        z = {'png': base64.b64encode(array_to_png(array_out, colormap='jet')), 
#             'data': array_out.tolist()}
#        dims = {}
#        dims['zmin'] = array_out.min()
#        dims['zmax'] = array_out.max()
#        axis = ['x', 'y']
#        for index, label in enumerate(axis):
#            arr = self._info[index]['values']
#            dims[axis[index] + 'min'] = amin(arr)
#            dims[axis[index] + 'max'] = amax(arr)
#            dims[axis[index] + 'dim'] = alen(arr)
#            dims['d' + axis[index]] = arr[1] - arr[0]
#        xlabel = self._info[0]['name']
#        ylabel = self._info[1]['name']
#        zlabel = self._info[2]['cols'][0]['name']
#        title = 'AND/R data' # That's creative enough, right?
#        type = '2d_image'
#        dump = dict(type=type, z=z, title=title, dims=dims, xlabel=xlabel, ylabel=ylabel, zlabel=zlabel)
#        res = simplejson.dumps(dump, sort_keys=True)
#        return res
