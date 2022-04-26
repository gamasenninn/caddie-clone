from sqlalchemy.dialects.sqlite import insert
from models import *
import importlib
import os
import csv
import re
import datetime


def upsert_csv():
    fixtures_dir = 'csv_dir/import/'
    models = importlib.import_module('models')
    dirList = os.listdir(fixtures_dir)
    dirList.remove('.gitkeep')

    for file_name in dirList:
        class_name = file_name.replace(".csv", "")
        model_class = getattr(models, class_name)
        with open(fixtures_dir + '/' + file_name, encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            header = next(reader)
            for row in reader:
                columnDic = {}
                for i in range(len(header)):
                    # TODO:請求・見積書に紐づく商品・入金テーブルが無いとフロントでエラーになるので対応
                    patternDatetime = r'[12]\d{3}[/\-年](0?[1-9]|1[0-2])[/\-月](0?[1-9]|[12][0-9]|3[01])日?T((0?|1)[0-9]|2[0-3])[:時][0-5][0-9][:分][0-5][0-9][.秒]\d{6}$'
                    stringDatetime = r'' + row[i]
                    progDatetime = re.compile(patternDatetime)
                    resultDatetime = progDatetime.match(stringDatetime)
                    if resultDatetime:
                        tdatetime = datetime.datetime.strptime(
                            row[i], '%Y-%m-%dT%H:%M:%S.%f')
                        row[i] = tdatetime

                    else:
                        pattern = r'[12]\d{3}[/\-年](0?[1-9]|1[0-2])[/\-月](0?[1-9]|[12][0-9]|3[01])日?$'
                        string = r'' + row[i]
                        prog = re.compile(pattern)
                        result = prog.match(string)
                        if result:
                            tdatetime = datetime.datetime.strptime(
                                row[i], '%Y-%m-%d')
                            tdate = datetime.date(
                                tdatetime.year, tdatetime.month, tdatetime.day)
                            row[i] = tdate
                    # CSVの値は全てStrになってしまうので、boolへ変換
                    if row[i] == 'True':
                        row[i] = True
                    if row[i] == 'False':
                        row[i] = False
                    if row[i] == '':
                        row[i] = None
                    columnDic[header[i]] = row[i]
                insert_stmt = insert(model_class).values(columnDic)
                do_update_stmt = insert_stmt.on_conflict_do_update(
                    index_elements=['id'], set_=columnDic)
                db.session.execute(do_update_stmt)
            db.session.commit()
