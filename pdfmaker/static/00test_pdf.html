# Server sample for Pdf Maker 
# 
#
from flask import Flask,make_response,redirect
from pdf_maker import pdf_maker
import json
import uuid

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello Pdf serve"

@app.route('/test')
def test():
    return app.send_static_file('test-pdf.html')

@app.route('/pdf/<file>',methods=["GET"])
def open_pdf(file):
    return app.send_static_file("pdf/"+file)
    
@app.route('/pdfmaker',methods=["GET","POST"])
def makepdf():
    return redirect('/pdfmaker/data')

@app.route('/pdfmaker/<json_file>')
def makepdf_file(json_file):
    with open( f'./{json_file}.json', mode='r', encoding='utf-8') as f:
        d = json.load(f)

    uuid_file_name = str(uuid.uuid1())+".pdf"
    alter_file_name = pdf_maker(d,file_name=uuid_file_name)


    #pdfdata = pdf_maker(d,is_BytesIO=True)
    #response = make_response(pdfdata)
    #response.mimetype = "application/pdf"
    #return response
    return alter_file_name

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


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5020, debug=True)
