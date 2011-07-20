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
        z = [arr[:, 0].tolist() for arr in self]
        axis = ['x', 'y']
        dims = {}
        for index, label in enumerate(axis):
            arr = self._info[index]['values']
            dims[axis[index] + 'min'] = amin(arr)
            dims[axis[index] + 'max'] = amax(arr)
            dims[axis[index] + 'dim'] = alen(arr)
        xlabel = self._info[0]['name']
        ylabel = self._info[1]['name']
        zlabel = self._info[2]['cols'][0]['name']
        title = 'AND/R data' # That's creative enough, right?
        type = '2d'
        dump = dict(type=type, z=z, title=title, dims=dims, xlabel=xlabel, ylabel=ylabel, zlabel=zlabel)
        res = simplejson.dumps(dump, sort_keys=True, indent=2)
        return res
