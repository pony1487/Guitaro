from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/testdebug')
def test_debug():
    print("debug works")
    return 'testdebug'


if __name__ == '__main__':
    app.run()
