from flask import Flask, jsonify, request
from FileManager import FileManager

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/list_topic')
def list_topic():
    file_manager = FileManager("topic")
    return file_manager.list_directories()


@app.route('/list_plan')
def list_plan():
    file_manager = FileManager("plan")
    return file_manager.list_directories()


@app.route('/list_files_in_directory')
def list_files_in_directory():
    file_manager = FileManager("topic/picking")
    return file_manager.list_files_in_directory()


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
