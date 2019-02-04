from flask import Flask, jsonify, request, send_file
from FileManager import FileManager
from guitaroconfig import valid_directories, valid_topics, valid_plans

app = Flask(__name__)


@app.route('/')
def welcome():
    return 'Welcome to Guitaro!'


@app.route('/list_topic')
def list_topic():
    file_manager = FileManager("topic")
    return file_manager.list_directories()


@app.route('/list_plan')
def list_plan():
    file_manager = FileManager("plan")
    return file_manager.list_directories()


@app.route('/list_files_in_topic')
def list_files_in_topic():
    topic_path = "topic/"
    topic = request.args.get("topic")
    if topic not in valid_topics:
        return "Error: Not a valid topic"
    print(topic)
    file_manager = FileManager(topic_path + topic)
    return file_manager.list_files_in_directory()


@app.route('/list_files_in_plan')
def list_files_in_plan():
    plan_path = "plan/"
    plan = request.args.get("plan")
    if plan not in valid_plans:
        return "Error: Not a valid plan"
    print(plan)
    file_manager = FileManager(plan_path + plan)
    return file_manager.list_files_in_directory()


@app.route('/get_lesson_from_topic', methods=['GET'])
def get_lesson_from_topic():
    topic_path = "topic/"
    topic = request.args.get("topic")
    topic += "/"

    lesson_name = request.args.get("lesson_name")
    file_manager = FileManager(topic_path + topic)
    print(file_manager.get_lesson_path(lesson_name))
    try:
        return send_file(file_manager.get_lesson_path(lesson_name), mimetype="audio/wav", as_attachment=True,
                         attachment_filename=lesson_name)
    except FileNotFoundError as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
