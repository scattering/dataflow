from django.utils.translation import ugettext as _T
from django.db import models
from django.contrib.auth.models import User


# SHA1 hash length for hashed values.
HASH_LENGTH = 160

# Note: hashes for JSON data need to use sorted_keys=True for reproducibility
#   import json, hashlib
#   json_data = json.dumps(sort_keys=True, separators=(',',':'), allow_nan=True)
#   hash = hashlib.sha1(json_data).hexdigest()
# This is available in javascript using the canonical-json package:
#     https://www.npmjs.org/package/canonical-json

class File(models.Model):
    """
    Files in dataflow are stored on disk according to their hash value.

    Files have a source, which is a URI indicating where they came from.
    Usually this will be a facility REST interface to the available data,
    though it may be a file uploaded by the user.

    Files have columns, indicating which fields are varying within the file,
    and what range they vary through.  This information is helpful to the
    file selector, which depending on the node, may want to display the data
    range available in the various columns.  Files also have attributes, which
    are key-value pairs extracted from the file.  Keys such as 'intent' can
    be used in the limit or group the files shown in the selector.  The
    metadata extraction and storage happens as the files are added to
    dataflow.  These operations are heavily dependent on file parsing, and
    so are very much specific to each instrument.
    """
    TYPES = (('data','Data file'),('calc','Reduced file'))
    hash = models.CharField(max_length=HASH_LENGTH, primary_key=True)
    hash.help_text = _T("Unique hash for the content of the file.")
    name = models.CharField(max_length=60)
    name.help_text = _T("Name of file shown to the user.")
    type = models.CharField(max_length=4, choices=TYPES)
    type.help_text = _T("File type")
    timestamp = models.DateTimeField(auto_now_add=False)
    timestamp.help_text = _T("Measurement time. For reduced files, this is the latest measurement time.")
    # data = FileField?

class FilePlot(models.Model):
    """
    File thumbnails can be useful for rapid data selection/display.
    """
    file = models.OneToOneField('File')
    file.help_text = _T('File that is plotted')
    #thumbnail = ImageField?
    #data = jqplot spec

class FileCache(models.Model):
    """
    File caching information.

    We can periodically go through available files and remove those that are
    large and cheap to reproduce.  The file cache object contains the
    information necessary to make such a decision.

    Cache priority is used to distinguish intermediate files (priority=0),
    from result files (priority=1).  Files that are explicitly named, such
    as slit results.
    """
    file = models.OneToOneField('File')
    file.help_text = _T('File that can be recreated')
    access_time = models.DateTimeField()
    access_time.help_text = _T("Last access date")
    cost = models.IntegerField()
    cost.help_text = _T("Number of milliseconds required to generate/download the data.")
    size = models.IntegerField()
    size.help_text = _T("File size.")
    # reader = models.CharField(max_length=60)
    # reader.help_text = _T("Name of the reader which can process the file")
    # plot = models.TextField()
    # plot.help_text = _T("JSON data representing thumbnail plot")
    priority = models.IntegerField()
    priority.help_text = _T("Cache priority.  Remove lower priority items first.")
    # Use cost and size to determine whether the data should be ejected from the cache
    # Don't know if the cost should be the total cost of the computation, or just
    # the cost to compute the node results.

#class FilePlot(models.Model):
#   """
#   Thumbnail version of file.
#   """
#   file = models.OneToOneField('File')
#   file.help_text = _T('Plottable file')
#   png = models.

class FileColumn(models.Model):
    """
    Data column within a file.

    When a file is loaded into dataflow, the data is processed to extract the
    columns that it contains, and the min-max range of each column.  This
    information is used by the file selector to display range of values
    available in each file as an aid to the user in selecting the correct
    file from a set. All columns should be removed when the file is deleted.
    """
    file = models.ForeignKey(File, related_name='columns')
    file.help_text = _T("File containing the column")
    name = models.CharField(max_length=50)
    name.help_text = _T("Column name recorded in the file")
    min = models.FloatField()
    min.help_text = _T("Lowest value recorded for the column")
    max = models.FloatField()
    max.help_text = _T("Highest value recorded for the column")
    #class Meta: ordering = ['name']

class FileAttribute(models.Model):
    """
    Key-value pairs for individual files.

    When a file is loaded into dataflow, the data is processed to extract
    key-value pairs such as the intent of the file.  This information is
    used by the file selector to display the available files to the user.

    The list of attributes is arbitrary.  We could for example use it to
    store default reduction attributes, inferred from the file when first
    loaded, but able to be updated by the user on a file info form.  These
    would then act as the defaults whenever the file is used in a reduction.
    """
    file = models.ForeignKey('File', related_name='attributes')
    file.help_text = _T("File containing the attribute.")
    key = models.CharField(max_length=30)
    key.help_text = _T("Attribute name")
    value = models.TextField()
    value.help_text = _T("JSON+ value of the attribute.  Allows JS primitives in addition to objects.")
    def __unicode__(self):
        return self.key + ": " + repr(self.value)

class DataFile(models.Model):
    """
    External data file.

    The data may have come from a facility with a fixed URI, or it may have
    been uploaded by the user, in which case the URI will start with 'file:'
    but will not otherwise be unique.  Facility files are assumed to be
    available forever from a fixed URI, and so can be deleted to save space
    on the server.
    """
    file = models.OneToOneField('File')
    file.help_text = _T('Data file contents')
    source = models.TextField()
    source.help_text = _T("URI used to retrieve the data.")

class ResultFile(models.Model):
    """
    Result of a dataflow computation.

    The computation result will ideally depend only on the node id,
    its version number, its configuration values (both the default values
    from the template and the applied values from the instance), and its
    inputs (which will be the hash values for some other computation).
    Together, these values will form the hash of the data node.

    When a bug is fixed in the underlying libraries, all nodes affected by
    that bug should bump their version number so that we can identify the
    results which need to be recomputed.

    Data lifetime is determined by the application.  Not all data is
    necessarily stored in the database.  It may be that intermediate values
    are cached in redis, and only the results of the save nodes are stored
    in the database.  We may also provide a way for users to store individual
    outputs without modifying the template with an explicit save node.
    Expensive intermediate computations may be saved automatically, and
    periodically purged.

    Note that saved data from one template in an experiment, e.g., slit
    scans or He3 polarizer efficiency reductions, may be used as an input
    to a further template within the experiment.  When things go really
    wrong, sometimes data from one experiment is used to reduce data in
    separate experiment.  This should be handled transparently, with
    """
    file = models.OneToOneField('File', null=True)
    file.help_text = _T("Resulting data")
    hash = models.CharField(max_length=HASH_LENGTH, primary_key=True)
    hash.help_text = _T("Unique hash for the computation input.")
    state = models.TextField()
    state.help_text = _T("JSON representation of the computation.  This will contain keys for node, version, config and inputs")
    datatype = models.CharField(max_length=300)
    datatype.help_text = _T("Data type name.  The data type determines how the data can be viewed and processed.")
    name = models.CharField(max_length=60)
    name.help_text = _T("Display name for the results file.")
    computation = models.ForeignKey('Computation', null=True)
    computation.help_text = _T("Data flow computation that produced the file.")
    node = models.IntegerField()
    node.help_text = _T("Computation node which produced the output.")
    index = models.IntegerField()
    index.help_text = _T("Output index for the computation node.")
    def __unicode__(self):
        return self.name

class Computation(models.Model):
    """
    A computation is the result applying a inputs to a dataflow template.

    Computation lifetime is determined by the application.  During reduction,
    many computations will be performed as the user selects data, adjusts
    parameters, and finally chooses whether or not the results should be
    saved.  As templates are and they underlying computational nodes are
    updated, users may be prompted to update their reduction results,
    throwing away old computations if the results are not yet published,
    otherwise running the new computation so that they can compare results
    to the old calculations and decide whether the difference will require
    additional analysis.
    """
    hash = models.CharField(max_length=HASH_LENGTH, primary_key=True)
    hash.help_text = _T("Unique hash for the template + configuration used for the computation.")
    # template lifetime is independent of computation lifetime
    template = models.ForeignKey('Template', null=True, on_delete=models.SET_NULL)
    template.help_text = _T("Reference to the named template.  This may be different from the applied template if the named template is updated after it is applied.  Check the applied template hash against the named template hash to decide.")
    dataflow_hash = models.CharField(max_length=HASH_LENGTH)
    dataflow_hash.help_text = _T("Unique hash for the flow graph.")
    dataflow = models.TextField()
    dataflow.help_text = _T("JSON representation of the flow graph representing the computation.")
    configuration = models.TextField()
    configuration.help_text = _T("JSON representation of the parameters for each element of the flow graph.")


class Template(models.Model):
    """
    Templates are a way to specify the flow of data through a reduction.

    Many measurements will be highly stylized, using the same data flow
    on many different datasets.   Each instrument has a set of templates
    associated with it that allow the instrument scientist to set up the
    stylized reductions that are associated with that instrument.  Once the
    template is created, it should be exported as a file and sent to the
    dataflow maintainers.  These  default  reductions are stored with the
    instrument model in the dataflow repository, and populate the initial
    template database for the instrument.

    The standard instrument templates should be flexible enough that most
    of the measurements can be captured with the same data flow, with modular
    components such as footprint correction which allow the user to select
    between ab initio and empirical footprint estimation.   They should make
    the  reduction process as  automatic as possible, so that for example, the
    last dark beam  measurement for a particular instrument configuration
    becomes the default dark beam input for the SANS reduction.

    Other measurements will be one-offs, with a different template for each
    part of the experiment, and templates that change frequently.  Dataflow
    supports copying and modifying templates within and between experiments
    so that users have this flexibility.

    Idea: set up a celery queue to run computations in the background whenever
    a template is updated.  Compute a distance metric between old and new
    results.  If within epsilon*uncertainty, silently update the
    computation.  If not, save the new results and warn the user that the
    old results are out of date when convenient.  If the template changes
    again, clear the queue, delete the last new results and repeat.
    """
    name = models.CharField(max_length=50)
    name.help_text = _T("Name of the template")
    instrument = models.ForeignKey('Instrument', null=True)
    instrument.help_text = _T("Templates are specific to each instrument.")
    dataflow_hash = models.CharField(max_length=HASH_LENGTH)
    dataflow_hash.help_text = _T("Unique hash for the flow graph.")
    dataflow = models.TextField()
    dataflow.help_text = _T("JSON representation of the flow graph representing the computation.")
    #class Meta:
    #    unique_together = ('name','instrument')
    def __unicode__(self):
        return self.name

class Experiment(models.Model):
    """
    Experiments are the primary organizational level of the user interface.

    Data files are grouped into experiments.  The instrument determines which
    reduction steps are available.w
    """
    data = models.ManyToManyField('DataFile', null=True)
    data.help_text = _T("Data files associated with the experiment.")
    results = models.ManyToManyField('ResultFile', null=True)
    results.help_text = _T("Data files associated with the experiment.")
    #templates = models.ManyToManyField('Template', null=True)
    facility = models.ForeignKey('Facility', null=True)
    facility.help_text = _T("Facility providing the data.")
    instrument = models.ForeignKey('Instrument', null=True)
    instrument.help_text = _T("Instrument used for the measurement.")
    experiment_id = models.CharField(max_length=100)
    experiment_id.help_text = _T("Facility specific tracking number for an experiment")
    project = models.ForeignKey('Project')
    project.help_text = _T("Enclosing project")
    def __unicode__(self):
        return self.tracking_number


class Project(models.Model):
    """
    A project is like a directory for experiments.

    Projects can contain experiments or other projects.  Linking is possible,
    allowing one experiment to be part of multiple projects.  Projects may
    be shared by multiple users.  project X user will be unique.
    """
    name = models.CharField(max_length=50)
    name.help_text = _T("Name of the project.")
    users = models.ManyToManyField(User, related_name='users')
    users.help_text = _T("Users who can see the project")
    path = models.CharField(max_length=300, unique=True)
    path.help_text = _T("Path to the project")
    def __unicode__(self):
        return self.name

class Instrument(models.Model):
    """
    The instrument
    """
    name = models.CharField(max_length=50)
    name.help_text = _T("Name of the instrument")
    facility = models.ForeignKey('Facility')
    facility.help_text = _T("Instrument location")
    beamline = models.CharField(max_length=10)
    beamline.help_text = _T("Beamline ID for data retrieval")
    instrument_type = models.CharField(max_length=50)
    instrument_type.help_text = _T("Dataflow model")
    #templates = models.ManyToManyField('Template', null=True)
    #templates.help_text = _T("Standard reduction templates for the instrument")

    def __unicode__(self):
        return self.name

class CalibrationFile(models.Model):
    """
    Calibration values for the instrument.

    Instruments will have a number of calibration values associated with them
    that change slowly over time.  For example, detector efficiency can slowly
    degrade if the detector is overexposed due to build up on the detector
    wires, and so it will need to be periodically remeasured.

    When a reduction template needs a certain calibration measurement, the
    last calibration taken before that measurement will be used.  The user
    will be able to override this default, with the file selector showing
    all calibrations with the list centered on the default.

    The current implementation assumes a small number of calibration files
    so that the list of available files for a particular calibration type
    can be loaded in memory and sent to the user interface.  This should not
    be an issue for per cycle measurements such as SANS detector efficiency,
    which will have at most tens of calibrations per instrument X type.
    More frequent calibrations, such as He3 polarizer efficiency measurements
    or reflectometry slit scans, can be done as part of the usual experiment
    reduction cycle.

    The instrument scientist is ultimately responsible for keeping the
    calibration files up to date, though the process may be automated.
    End users will not have permission to store tag files as calibration files.
    """
    type = models.CharField(max_length=50)
    type.help_text = _T("Calibration type, e.g. detector efficiency")
    instrument = models.ForeignKey('Instrument', related_name="calibrations")
    instrument.help_text = _T("Instrument which has been calibrated")
    file = models.ForeignKey('File')
    file.help_text = _T("File containing the calibration measurement")

class Facility(models.Model):
    """
    Facility containing the instrument.

    By selecting the facility, dataflow can reduce the number of instruments
    displayed to the user.   Facility data servers can export sets of files
    already organized by experiment.
    """
    name = models.CharField(max_length=50)
    name.help_text = _T("Facility name.")
    data_server = models.CharField(max_length=200)
    data_server.help_text = _T("URL of the data server.")
    class Meta:
        verbose_name_plural = "facilities"
    def __unicode__(self):
        return self.name


