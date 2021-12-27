from api import app


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


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5010)
