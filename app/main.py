from api import app


@app.route('/test')
def test():
    return "Hello TEST!"


@app.route('/')
def hello():
    return "Hello world!"


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5010)
