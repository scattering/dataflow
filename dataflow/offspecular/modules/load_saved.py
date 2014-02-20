import os

from reduction.offspecular.FilterableMetaArray import FilterableMetaArray

# load saved result:
def load_saved_action(results=[], intent='', **kwargs):
    print "loading saved results"
    import tarfile
    from apps.tracks.models import ResultFile
    Fileobj = ResultFile.objects.get(name=results[0])
    fn = Fileobj.name
    fp = Fileobj.location
    tf = tarfile.open(os.path.join(fp, fn), 'r:gz')
    result_objs = [tf.extractfile(member) for member in tf.getmembers()]
    result = [FilterableMetaArray.loads(robj.read()) for robj in result_objs]
    return dict(output=result)

