from flask import Flask, make_response, redirect, request
from flask_cors import CORS, cross_origin
import uuid

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route('/')
def HelloWorld():
    return 'HelloWorld'


@app.route('/csv_test')
def CsvTest():
    return app.send_static_file('csv_test.html')


# ----- API -----
@app.route('/upload', methods=['POST'])
def CsvUpload():
    d = request.json
    uuid_file_name = str(uuid.uuid1())+".pdf"
    # alter_file_name = pdf_maker(d, file_name=uuid_file_name)
    return uuid_file_name


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5020, debug=True)
