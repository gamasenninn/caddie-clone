from api import app
import sys
import json
import uuid
from flask import redirect, request
from flask import Flask,request,json, jsonify,Response,make_response
import importlib
from models import *
import os
import csv

sys.path.append('../')
import pdfmaker.app.pdf_maker as pd
from upload.upload import make_thumb,chext,save_file,remove_files2,get_flist


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


@app.route('/home-page')
def homePage():
    return app.send_static_file('home.html')


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


@app.route('/memo-page')
def memoPage():
    return app.send_static_file('memo.html')

# ------pdf maker -------


@app.route('/pdfmaker', methods=["GET", "POST"])
def makepdf():

    if request.method == "GET":
        return redirect('/pdfmaker/data')
    elif request.method == "POST":
        d = request.json
        uuid_file_name = str(uuid.uuid1())+".pdf"
        alter_file_name = pd.pdf_maker(d, file_name=uuid_file_name)
        return alter_file_name


@app.route('/pdfmaker/<json_file>')
def makepdf_file(json_file):
    with open(f'./{json_file}.json', mode='r', encoding='utf-8') as f:
        d = json.load(f)

    uuid_file_name = str(uuid.uuid1())+".pdf"
    alter_file_name = pd.pdf_maker(d, file_name=uuid_file_name)

    # ------BytesIOを使えば、ファイル作成は必要ない(今回は使わない) ----
    #pdfdata = pdf_maker(d,is_BytesIO=True)
    #response = make_response(pdfdata)
    #response.mimetype = "application/pdf"
    # return response
    return alter_file_name


@app.route('/pdf/<file>', methods=["GET"])
def open_pdf(file):
    return app.send_static_file("pdf/"+file)


@app.route('/unit-page')
def unitPage():
    return app.send_static_file('unit.html')


@app.route('/category-page')
def categoryPage():
    return app.send_static_file('category.html')


@app.route('/maker-page')
def makerPage():
    return app.send_static_file('maker.html')


@app.route('/setting-page')
def settingPage():
    return app.send_static_file('setting.html')


@app.route('/invoice-dust-page')
def invoiceDustPage():
    return app.send_static_file('invoice_dust.html')


@app.route('/quotation-dust-page')
def quotationDustPage():
    return app.send_static_file('quotation_dust.html')


# --------- UPLOAD function ----------
@app.route('/test-upload')
def uptest():
    return app.send_static_file('./uptest.html')


@app.route("/upload-files/<dir_path>", methods=['POST'])
def upload_file(dir_path):
    if 'file' not in request.files:
        make_response(jsonify({'result': 'uploadFile is required.'}))
    f = request.files["file"]
    id = request.form['fileId']
    dir_path = "./static/" + dir_path
    return jsonify(save_file(id, dir_path, f))


@app.route("/delete-files", methods=['DELETE'])
def delete_files():
    dict_data = json.loads(request.data.decode())
    return jsonify(remove_files2(dict_data))


@app.route("/list-files/<dir_path>/<fid>", methods=['GET'])
def get_file_list(dir_path, fid):
    return jsonify(get_flist(fid, f"./static/{dir_path}"))


# ----- csv_upload_test -----
@app.route('/csv-test')
def CsvTest():
    return app.send_static_file('csv_test.html')


@app.route('/upload', methods=['POST'])
def CsvUpload():
    file = request.files['file']
    target = request.form['selected']
    file.save('csv/'+target + '.csv')
    import_csv()
    return "test"


def import_csv():
    fixtures_dir = 'csv/'
    models = importlib.import_module('models')
    dirList = os.listdir(fixtures_dir)
    dirList.remove('.gitkeep')

    for file_name in dirList:
        class_name = file_name.replace(".csv", "").capitalize()
        Klass = getattr(models, class_name)
        with open(fixtures_dir + '/' + file_name, encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            header = next(reader)
            for row in reader:
                klass = Klass()
                for i in range(len(header)):
                    setattr(klass, header[i], row[i])
                db.session.add(klass)
            db.session.commit()


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5010, debug=True)
