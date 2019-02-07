from flask import Flask, jsonify, request, send_file, render_template
from FileManager import FileManager
from AudioAnalysis import AudioAnalysis
from guitaroconfig import valid_directories, valid_topics, valid_plans
from werkzeug.utils import secure_filename

import os
import guitaroconfig
import app_utils

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = guitaroconfig.UPLOAD_FOLDER


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


@app.route('/analyse_user_recording', methods=['POST'])
def analyse_user_recording():
    """
    Pattern taken from http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
    :return:
    """
    if request.method == 'POST':
        if 'file' not in request.files:
            print("no file uploaded")
            return "Error"

        file = request.files['file']

        if file and app_utils.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            uploaded_file_path = app.config['UPLOAD_FOLDER'] + "/" + filename
            audio_analysis = AudioAnalysis(uploaded_file_path)
            print(audio_analysis.analyse_notes())
            print(audio_analysis.analyse_timing())

            return "File uploaded"
        else:
            return "Wrong File type: Must be wav"


###############################################################
# TESTING. Delete once done
###############################################################

@app.route('/test_volume')
def test_volume():
    f = open("../audio/plan/beginner/E_Major_LESSON.wav", "r")
    print(str(f))
    return str(f)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
