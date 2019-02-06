from flask import Flask, jsonify, request, send_file, render_template
from FileManager import FileManager
from guitaroconfig import valid_directories, valid_topics, valid_plans

app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template("upload.html")


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

    print(topic)

    lesson_name = request.args.get("lesson_name")
    file_manager = FileManager(topic_path + topic)
    print(file_manager.get_lesson_path(lesson_name))
    try:
        return send_file(file_manager.get_lesson_path(lesson_name), mimetype="audio/wav", as_attachment=True,
                         attachment_filename=lesson_name)
    except FileNotFoundError as e:
        return str(e)


@app.route('/get_lesson_from_plan', methods=['GET'])
def get_lesson_from_plan():
    plan_path = "plan/"
    plan = request.args.get("topic")
    plan += "/"

    lesson_name = request.args.get("lesson_name")
    file_manager = FileManager(plan_path + plan)
    print(file_manager.get_lesson_path(lesson_name))
    try:
        return send_file(file_manager.get_lesson_path(lesson_name), mimetype="audio/wav", as_attachment=True,
                         attachment_filename=lesson_name)
    except FileNotFoundError as e:
        return str(e)


@app.route('/receive_recording_from_user', methods=['POST'])
def receive_recording_from_user():
    print("in receive file")
    if request.method == 'POST':
        print("in if==POST")
        if 'file' not in request.files:
            print("no file uploaded")
            return "Error"
        uploaded_file = request.files['file'].read()
        print(uploaded_file)

        return str(uploaded_file)


@app.route('/test_volume')
def test_volume():
    f = open("../audio/plan/beginner/E_Major_LESSON.wav", "r")
    print(str(f))
    return str(f)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
