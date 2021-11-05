import sys

from flask import Flask,request,json, jsonify,Response,make_response
from flask_cors import CORS, cross_origin
import json
import os
import glob

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route("/")
def hello():
    version = "{}.{}".format(sys.version_info.major, sys.version_info.minor)
    message = "Hello World from Flask in a uWSGI Nginx Docker container with Python {} (default)".format(
        version
    )
    return message

@app.route("/upload",methods=['POST'])
@cross_origin(supports_credentials=True)
def upload_file():
    if 'file' not in request.files:
        make_response(jsonify({'result':'uploadFile is required.'}))
    f = request.files["file"]
    id= request.form['fileId']
    os.makedirs(f'./upload/{id}', exist_ok=True)
    f.save(f'./upload/{id}/{f.filename}')
    response = {
        "text":"OK",
        "fileId": id,
        "filename": f.filename,      
        "mimetype": f.mimetype,      
    }
    return  jsonify(response)

@app.route("/delete_files/<fid>",methods=['DELETE'])
@cross_origin(supports_credentials=True)

def delete_files(fid):
    #f = request.files["file"]
    #id= request.form['fileId']
    #os.makedirs(f'./upload/{id}', exist_ok=True)
    #f.save(f'./upload/{id}/{f.filename}')
    #response = {
    #    "text":"OK",
    #    "fileId": id,
    #    "filename": f.filename,      
    #    "mimetype": f.mimetype,      
    #}
    response={"result":"OK"}
    return  jsonify(response)

@app.route("/file_list/<fid>",methods=['GET'])
@cross_origin(supports_credentials=True)
def get_file_list(fid):
    file_list = glob.glob(f'upload/{fid}/*')
    file_list = ["../"+f.replace('\\','/') for f in file_list ]
    app.logger.debug(file_list)
    j_flist = { "list": file_list}
    message = jsonify(j_flist)
    return message

@app.route('/<f>')
def proc(f):
    return app.send_static_file('./'+f)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)
    