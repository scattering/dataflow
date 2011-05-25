# TODO: Add /jobs/<id>/data.zip to fetch all files at once in a zip file format
# TODO: Store completed work in /path/to/store/<id>.zip

import os, sys
import logging
import json
import flask
from flask import send_from_directory
from werkzeug import secure_filename

app = flask.Flask(__name__)

# ==== Format download specialialization ===
def _format_response(response, format='.json', template=None):
    """
    Return response as a particular format.
    """
    #print "response",response
    if format == '.html':
        if template is None: flask.abort(400)
        return flask.render_template(template, **response)
    elif format in ('', '.json'):
        return flask.jsonify(**dict((str(k),v) for k,v in response.items()))
    elif format == '.pickle':
        return pickle.dumps(response)
    else:
        flask.abort(400) # Bad request

DATASTORE = '/tmp'
INSTRUMENTS = ['BT7','ANDR']
@app.route('/data<format>', methods=['GET'])
def list_instruments(format='.json'):
    """
    GET /data.<format>

    Return a list of instruments available.
    """
    response = { 'instruments': INSTRUMENTS }
    return _format_response(response, format, template='list_instruments.html')

@app.route('/data/<instrument>/experiments<format>', methods=['GET'])
def recent_experiments(instrument, format='.json'):
    """
    GET /data/<instrument>/experiments<format>

    Return a list of recent experiments.
    """
    if instrument not in INSTRUMENTS:
        raise ValueError("invalid instrument "+instrument)
    path = os.path.join(DATASTORE,instrument)
    try:    files = sorted(os.listdir(path))
    except: files = []
    # TODO: add date, number of measurements, etc.
    response = { 'instrument': instrument, 'experiments': files }
    return _format_response(response, format, template='list_experiments.html')

@app.route('/data/<instrument>/<experiment>/data<format>')
def list_files(instrument, experiment, format=".json"):
    if instrument not in INSTRUMENTS:
        raise ValueError("invalid instrument "+instrument)
    experiment = secure_filename(experiment)
    path = os.path.join(DATASTORE,instrument,experiment)
    try:
        files = sorted(os.listdir(path))
        finfo = [(f,os.path.getsize(os.path.join(path,f)))
                 for f in files if os.path.isfile(os.path.join(path,f))]
    except:
        finfo = []
    response = { 'instrument':instrument,
                 'experiment':experiment,
                 'files': finfo }
    return _format_response(response, format=format, template="list_data.html")

@app.route('/data/<instrument>/<experiment>/data/<filename>')
def get_file(instrument, experiment, filename):
    if instrument not in INSTRUMENTS:
        raise ValueError("invalid instrument "+instrument)
    experiment = secure_filename(experiment)
    path = os.path.join(DATASTORE,instrument,experiment)
    mimetype = None
    as_attachment = True

    return send_from_directory(path, filename,
                               mimetype=mimetype,
                               as_attachment=as_attachment)

def serve():
    app.run()
    #app.run(host='0.0.0.0')

def fullpath(p): return os.path.abspath(os.path.expanduser(p))
def configure(keyfile=None,datastore=None):
    if keyfile:
        app.config['SECRET_KEY'] = open(fullpath(keyfile)).read()
    if datastore:
        global DATASTORE
        DATASTORE = fullpath(datastore)

if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    configure(datastore=os.path.join(root,'sampledata'))
    app.config['DEBUG'] = True
    serve()
