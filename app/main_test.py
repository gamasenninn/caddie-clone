from sqlalchemy import insert, true
from sqlalchemy.dialects.sqlite import insert
from api import app
import sys
import json
import uuid
from flask import redirect, request
from flask import Flask, request, json, jsonify, Response, make_response, send_file, send_from_directory,render_template
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import importlib
from models import *
import os
import csv

# sys.path.append('../')
import pdfmaker.app.pdf_maker as pd
from upload.upload import make_thumb, chext, save_file, remove_files2, get_flist

# ------　ユーザー認証 -------
app.secret_key = os.urandom(24)
login_manager = LoginManager()
login_manager.login_view = 'get_login'
login_manager.init_app(app)


class LoginUser(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


@login_manager.user_loader
def load_user(user_id):
    return LoginUser(user_id)


@app.route('/')
def home():
    #return app.send_static_file('home.html')
    return render_template('home.html')

@app.route('/login', methods=['GET'])
def get_login():
    return app.send_static_file('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    user_id = request.form["userId"]
    password = request.form["password"]
    checkUser = User.query.filter_by(name=user_id).first()
    if checkUser:
        if checkUser.password == password:
            user = LoginUser(user_id)
            login_user(user)
            next = request.args.get('next')
            return redirect(next or '/')
        else:
            return redirect('/login')
    else:
        return redirect('/login')


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    # return redirect('/login')
    return redirect('/')

# ------　ユーザー認証ここまで -------


@app.route('/test')
def test():
    return "Hello TEST!"


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
@login_required
def invoicePage():
    return app.send_static_file('invoice.html')


@app.route('/quotation-page')
@login_required
def quotationPage():
    return app.send_static_file('quotation.html')


@app.route('/customer-page')
@login_required
def customerPage():
    return app.send_static_file('customer.html')


@app.route('/item-page')
@login_required
def itemPage():
    #return app.send_static_file('item.html')
    return render_template('item.html')


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
@login_required
def unitPage():
    return app.send_static_file('unit.html')


@app.route('/category-page')
@login_required
def categoryPage():
    return app.send_static_file('category.html')


@app.route('/maker-page')
@login_required
def makerPage():
    return app.send_static_file('maker.html')


@app.route('/setting-page')
@login_required
def settingPage():
    #user_id = current_user.id
    checkUser = User.query.filter_by(name=current_user.id).first()
    if checkUser:
        if checkUser.role == "admin":
            return app.send_static_file('setting.html')
    return redirect('/login')


@app.route('/csv-upload-page')
@login_required
def csvUploadPage():
    return app.send_static_file('csv_upload.html')


@app.route('/invoice-dust-page')
@login_required
def invoiceDustPage():
    return app.send_static_file('invoice_dust.html')


@app.route('/quotation-dust-page')
@login_required
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


@app.route('/csv-import', methods=['POST'])
def CsvUpload():
    file = request.files['file']
    target = request.form['selected_import']
    file.save('csv/import/'+target + '.csv')
    try:
        upsert_csv()
    except:
        return jsonify({"result": "error", "message": "更新に失敗しました。CSVを正しく入力してください。"}), 500
    return jsonify({"result": "ok", "message": "更新に成功しました"})


def upsert_csv():
    fixtures_dir = 'csv/import/'
    models = importlib.import_module('models')
    dirList = os.listdir(fixtures_dir)
    dirList.remove('.gitkeep')

    for file_name in dirList:
        class_name = file_name.replace(".csv", "").capitalize()
        model_class = getattr(models, class_name)
        with open(fixtures_dir + '/' + file_name, encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            header = next(reader)
            for row in reader:
                columnDic = {}
                for i in range(len(header)):
                    columnDic[header[i]] = row[i]
                insert_stmt = insert(model_class).values(columnDic)
                do_update_stmt = insert_stmt.on_conflict_do_update(
                    index_elements=['id'], set_=columnDic)
                try:
                    db.session.execute(do_update_stmt)
                except:
                    db.session.rollback()
                    db.session.close()
                    csv_file.close()
                    os.remove(fixtures_dir+file_name)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                db.session.close()
            finally:
                csv_file.close()
                os.remove(fixtures_dir+file_name)

# ----- csv_export -----


@app.route('/csv-export', methods=['POST'])
def CsvExport():
    data = request.json
    class_name = data.get('tableName')
    fixtures_dir = 'csv/export/'

    models = importlib.import_module('models')
    model_class = getattr(models, class_name)
    model_schema = getattr(models, class_name+"Schema")
    columnlist = model_class.__table__.columns.keys()  # カラムリスト取得

    result = model_class.query.all()
    dataList = model_schema(many=True).dump(result)  # dict型のテーブル内データ

    with open(fixtures_dir+'test.csv', 'w', encoding='utf-8', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(columnlist)
        for d in dataList:
            sortList = []
            for column in columnlist:
                sortList.append(d[column])  # 並び順整形
            writer.writerow(sortList)
        f.close()

    downloadFileName = os.getcwd() + fixtures_dir+'test.csv'
    downloadFile = fixtures_dir+'test.csv'

    return send_file(downloadFile, as_attachment=True,
                     download_name=downloadFileName,
                     mimetype='application/csv')

# ----- admin_db_init -----


@app.route('/db-init-page')
@login_required
def dbInitPage():
    checkUser = User.query.filter_by(name=current_user.id).first()
    if checkUser:
        if checkUser.role == "admin":
            return app.send_static_file('db_init.html')
    return redirect('/login')


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5010, debug=True)
