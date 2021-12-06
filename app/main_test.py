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


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5010)
