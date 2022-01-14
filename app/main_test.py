from api import app
import sys
import json
import uuid
from flask import redirect,request
sys.path.append('../')
import pdfmaker.app.pdf_maker as pd

@app.route('/test')
def test():
    return "Hello TEST!"


@app.route('/')
def hello():
    return "Hello world!"


@app.route('/test-view-r')
def rootn():
    return app.send_static_file('test_view_r.html')


@app.route('/test-view-crud')
def crud_test():
    return app.send_static_file('test_view_crud.html')


@app.route('/test-view-crud2')
def crud_test2():
    return app.send_static_file('test_view_crud2.html')


@app.route('/test-view-crud3')
def crud_test3():
    return app.send_static_file('test_view_crud3.html')


@app.route('/test-view-crud4')
def crud_test4():
    return app.send_static_file('test_view_crud4.html')


@app.route('/test-view-crud5')
def crud_test5():
    return app.send_static_file('test_view_crud5.html')


@app.route('/test-view-invoice-switchable')
def crud_test_invoice_switchable():
    return app.send_static_file('test_view_invoice_switchable.html')


@app.route('/test-view-crud6')
def crud_test6():
    return app.send_static_file('test_view_crud6.html')


@app.route('/invoice-page')
def invoicePage():
    return app.send_static_file('invoice.html')


@app.route('/quotation-page')
def quotationPage():
    return app.send_static_file('quotation.html')


@app.route('/customer-page')
def customerPage():
    return app.send_static_file('customer.html')


@app.route('/item-page')
def itemPage():
    return app.send_static_file('item.html')

#------pdf maker -------
@app.route('/pdfmaker',methods=["GET","POST"])
def makepdf():

    if request.method == "GET":
        return redirect('/pdfmaker/data')
    elif request.method == "POST":
        d = request.json
        uuid_file_name = str(uuid.uuid1())+".pdf"
        alter_file_name = pd.pdf_maker(d,file_name=uuid_file_name)
        return alter_file_name

@app.route('/pdfmaker/<json_file>')
def makepdf_file(json_file):
    with open( f'./{json_file}.json', mode='r', encoding='utf-8') as f:
        d = json.load(f)

    uuid_file_name = str(uuid.uuid1())+".pdf"
    alter_file_name = pd.pdf_maker(d,file_name=uuid_file_name)

    #------BytesIOを使えば、ファイル作成は必要ない(今回は使わない) ----
    #pdfdata = pdf_maker(d,is_BytesIO=True)
    #response = make_response(pdfdata)
    #response.mimetype = "application/pdf"
    #return response
    return alter_file_name

@app.route('/pdf/<file>',methods=["GET"])
def open_pdf(file):
    return app.send_static_file("pdf/"+file)


@app.route('/unit-page')
def unitPage():
    return app.send_static_file('unit.html')


@app.route('/setting-page')
def settingPage():
    return app.send_static_file('setting.html')


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5010)
