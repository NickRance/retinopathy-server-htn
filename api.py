from flask import Flask
import json
import os
import types
import requests
import sys
from pprint import pprint

import posixpath
import BaseHTTPServer
import urllib
import cgi
import shutil
import mimetypes
import re
import time
import labelimageb as labelimage
import cleanup
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
 #lala

from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'input/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # tfoutput = labelimage.test(file)
            tfoutput = labelimage.test(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            finaloutput = {}
            finaloutput['results'] = {}
            finaloutput['results']['status'] = ("not diseased." in tfoutput)
            finaloutput['results']['confidence'] = float(tfoutput[-8:-1])
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            print(finaloutput)
            return json.dumps(finaloutput)
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run(debug=True, host = os.getenv("IP","0.0.0.0"),port = int (os.getenv('PORT', 33507)))
    #app.run()