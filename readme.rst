Dataflow is a template-based system for analyzing data.

The architecture is a basic dataflow architecture with the algorithm
visible on the screen as a series of boxes and lines.  Users can compose
new reduction templates or edit existing ones.  Once a template has been
created, it can be reused with different data sets and in different
experiments.

Users will enter the system from a particular instrument home page.
This will bring them to a screen showing the data available in the
instrument archive as well a set of templates for interacting with
the data. Clicking on a data file will show a raw plot of its contents,
so the system can be used a quick way to view the available data.

To perform a reduction, the user will choose from a set of preconstructed
templates, then associate the available data with the inputs into the
template.  By clicking on the various template terminals or the lines
connecting them, the data can be viewed at that stage of the reduction 
process.  Clicking a node should display a graph for each terminal.
When the reduction is complete and the data is saved, the data processing 
template is saved along with it.

Users can also choose to edit the reduction templates if specialized 
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

Reduction templates are applied to particular datasets.  This can happen 
one by one in the diagram (that is, by clicking an input terminal and 
filling in the associated data file), or can be done en masse in a
spreadsheet view, one row per reduced dataset.  The results from one
reduction flow can be used as the input to another, such as a slit scan 
composed of multiple datasets being used in a specular calculation.
