.. currentmodule:: apps

tracks
======

*tracks* is a data processing app for django.    The architecture is a
basic dataflow architecture with the algorithm visible on the screen
as a series of boxes and lines.  Users can compose new dataflow templates
or edit existing ones.  Once a template has been created, it can be reused
with different data sets and in different experiments.

Basic Usage
-----------

When users enter the system they will need to select an instrument.
This will bring them to a screen showing the data available in the
instrument archive as well a set of templates for interacting with
the data. Clicking on a data file will show a raw plot of its contents,
so the system can be used a quick way to view the available data.

To perform an analysis, the user will choose from a set of available
templates, then associate the available data with the inputs into the
template.  By clicking on the various template terminals or the lines
connecting them, the data can be viewed at that stage of the  process.
Clicking a node should display a graph for each terminal. When the
analysis is complete and the data is saved, the data processing
template is saved along with it.

Users can also choose to create new templates if specialized
steps are needed.  This will display the available modules which the
user can then add to the diagram.  The adjusted diagram can be turned
into a template by setting reasonable default values for the fields
and data inputs.  This will then appear in the users pool of available
templates.

To set up reduction for a new instrument, the instrument scientist must
do some work:

    * implement the data archive api so users can access facility data
    * define any new data types for the instruments, and their plots
    * create modules for reading instrument data
    * create modules for instrument specific reduction steps
    * create instrument definition file from modules and data
    * using the diagram editor, define default templates

The data archive api should be written so that it can take a data flow
request and produce the reduced data on demand.  That way, the computation
is closer to the data and less bandwidth is required.

Analysis templates are applied to particular datasets.  This can happen
one by one in the diagram (that is, by clicking an input terminal and
filling in the associated data file), or can be done *en masse* in a
spreadsheet view, one row per reduced dataset.  The results from one
reduction flow can be used as the input to another, such as a slit scan
composed of multiple datasets being used in a specular calculation.

Concepts
--------

*Template Language*

    A set of processing nodes.  This should include data loaders,
    transformers, and writers.  Different instrument classes will have
    different languages, such as SANS, TAS and reflectometry, but they
    may share data handling across instruments.

*Template* (:class:`tracks.models.Template`)

    A processing graph, with default configuration of the nodes.  The graph
    should contain blocks for selecting data inputs and saving processed
    outputs and graphs.  Users will be able to save any intermediate output
    through the user interface.

*Computation* (:class:`tracks.models.Computation`)

    A template and a configuration.  The computation is the heart of the
    dataflow analysis.  The individual node outputs have a unique
    hash based on the input values and the configuration parameters.  If
    the inputs or the configuration changes, then the output hash will
    change, as will the hash of any processing node which depends on it.
    These intermediate computations are stored in a redis cache so that
    changing computation parameters on a single node will not force the
    entire template to be reevaluated.

*Instrument* (:class:`tracks.models.Instrument`)

    A template language and a facility. The tracks site administrator must
    maintain the set of instruments available on the site.  Each instrument
    is associated with a facility, which supplies data for the instrument
    processor.  Each instrument will have a set of templates associated with,
    maintained by the instrument scientist.

    ***TODO*** support permissions to associate a template with an instrument,
    possibly with a many-to-many relation between instruments and users, or
    possibly with a permission tag for each instrument.

    ***TODO*** instrument should have a primary user so users can request
    help/report bugs.

*Facility* (:class:`tracks.models.Facility`)

    A collection of instruments and a data source.

    ***TODO*** Facilities may supply compute resources for processing
    dataflows near the data, which will be necessary when data sets are
    large and require significant computing resources to process.

*Experiment* (:class:`tracks.models.Experiment`)

    An instrument, a set of data, a set of templates and a set of results.
    Experiments

*Project* (:class:`tracks.models.Project`)

    A set of experiments and a set of users.  Projects support collaboration
    between users.  Usually experiments will belong to a single project,
    though there may be some experiments that are shared between different
    projects depending on the collaborators.

Settings
--------

Tracks has a number of settings that need to be maintained.

Javascript/css dependencies are set in :mod:`tracks.context_processors`.  The
defaults should work for most situations, but more complex sites may want
more control of which external javascript libraries are used.

TODOs
=====

* Clean unused datasets, results, experiments, projects.  We may want
to track the creator of each of these so that we can warn them before purging.
We could organize this as a recycle bin for each project, so that things can
be recovered.  Projects should probably have owners who can delete them.  Need
to work out the sharing of experiments between projects.

* Want to ease the sharing of templates. Users should be able to
easily pull up templates for any experiment with the same instrument that
they are working on, and maybe templates for other users.  Maybe want
private templates, but make shared the default.

* Template presentation order, such as
   * templates in the current experiment
   * templates in the current project
   * standard templates for the instrument
   * templates in other projects for the user
   * remaining templates
Templates could be sorted by number of uses.  Only templates for the current
instrument should be presented, or maybe for the instrument class.

* On reloading a computation, set the focus on the primary result, which is
the saved node.  Don't recompute the intermediate results unless the user
requests them.
