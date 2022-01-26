from flask import Flask, make_response, redirect, request
from flask_cors import CORS, cross_origin
import uuid
import io
import csv
import os

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['UPLOAD_FOLDER'] = '/static'


@app.route('/')
def HelloWorld():
    return 'HelloWorld'


@app.route('/csv_test')
def CsvTest():
    return app.send_static_file('csv_test.html')


# ----- API -----
@app.route('/upload', methods=['POST'])
def CsvUpload():
    file = request.files['file']
    file.save('test.csv')
    return "test"

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5020, debug=True)
