import sys

from flask import Flask,request,json, jsonify,Response,make_response
#from flask_cors import CORS, cross_origin
import json
import os
import glob
from PIL import Image, ImageDraw, ImageFilter
from make_thumb import make_thumb,chext #サムネイル作成関数

app = Flask(__name__)
#CORS(app, support_credentials=True)

@app.route("/")
def hello():
    version = "{}.{}".format(sys.version_info.major, sys.version_info.minor)
    message = "Hello World from Flask in a uWSGI Nginx Docker container with Python {} (default)".format(
        version
    )
    return message

@app.route("/upload",methods=['POST'])
#@cross_origin(supports_credentials=True)
def upload_file():
    if 'file' not in request.files:
        make_response(jsonify({'result':'uploadFile is required.'}))
    f = request.files["file"]
    id= request.form['fileId'] 

    os.makedirs(f'./static/upload/{id}', exist_ok=True)
    file_path = f'./static/upload/{id}/{f.filename}'
    f.save(file_path)
    
    make_thumb(file_path,f"./static/upload/{id}/thumbs")

    response = {
        "text":"OK",
        "fileId": id,
        "filename": f.filename,      
        "mimetype": f.mimetype,      
    }
    return  jsonify(response)

@app.route("/delete_files",methods=['DELETE'])
#@cross_origin(supports_credentials=True)

def delete_files():
    dict_data = json.loads(request.data.decode())

    for f in dict_data['files']:
        os.remove(f)

    for f in dict_data['thumbs']:
        os.remove(f)

    response={"result":"OK"}
    return  jsonify(response)

@app.route("/file_list/<fid>",methods=['GET'])
#@cross_origin(supports_credentials=True)
def get_file_list(fid):
    file_path_list = glob.glob(f'upload/{fid}/*')
    file_path_list = [".static/"+f.replace('\\','/') for f in file_path_list ]
    file_names = [f.split('/')[-1] for f in file_path_list ]
    #app.logger.debug(file_path_list)
    j_flist = { 
        "list": file_path_list,
        "file_names" : file_names 
    }
    message = jsonify(j_flist)
    return message

@app.route("/file_list2/<fid>",methods=['GET'])
#@cross_origin(supports_credentials=True)
def get_file_list2(fid):

    file_path_list = glob.glob(f'./static/upload/{fid}/*')
    arry = []
    for f in file_path_list:
        if os.path.isfile(f):

            dict_flist = { 
                "path": os.path.split(f)[0]+"/"+os.path.split(f)[1],
                "filename" : os.path.split(f)[1], 
                "dir" : os.path.split(f)[0],
                "thumb_path":  chext(os.path.split(f)[0]+"/thumbs/"+os.path.split(f)[1]),
                "type": os.path.splitext(f)[1].replace('.','').lower(),
                "isfile": os.path.isfile(f),
                "isdir": os.path.isdir(f),
                "status": os.stat(f),
            }
            #app.logger.debug(dict_flist)
            arry.append(dict_flist)
    message = jsonify(arry)
    return message

@app.route('/test')
def uptest():
    return app.send_static_file('./uptest.html')

@app.route('/upload/<fid>/thumbs/<file>')
def upimage(fid,file):
    app.logger.debug(f"{fid}:{file}")
    return app.send_static_file(f'./upload/{fid}/thumbs/{file}')
    #return f'./upload/{fid}/thumbs/{file}'


@app.route('/<f>')
def proc(f):
    return app.send_static_file('./'+f)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5031)
    