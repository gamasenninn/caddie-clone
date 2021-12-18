# Server sample for Pdf Maker 
# 
#
from flask import Flask,Response,make_response
from pdf_maker import pdf_maker
import json

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello Pdf serve"

    
@app.route('/pdfmaker')
def makepdf():
    with open( './data.json', mode='r', encoding='utf-8') as f:
        d = json.load(f)

    pdfdata = pdf_maker(d,is_BytesIO=True)
    response = make_response(pdfdata)
    response.mimetype = "application/pdf"
    return response

@app.route('/file/<file_name>')
def file(file_name):
    try:
        with open( f"./pdf/{file_name}", mode='rb') as f:
            pdfdata = f.read()
            response = make_response(pdfdata)
            response.mimetype = "application/pdf"
            #response.headers['Content-Type'] = 'application/pdf'
            #response.headers['Content-Disposition'] = f'inline; filename={file_name}'
            return response
    except:
        pass
        return f"file error:{file_name}"

    #return f"This response is PDF Stream {file_name}"



if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5020, debug=True)
