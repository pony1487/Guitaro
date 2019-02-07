from flask import Flask, jsonify, request, send_file, render_template
from FileManager import FileManager
from AudioAnalysis import AudioAnalysis
from AudioComparison import AudioComparison
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


@app.route('/topics')
def list_topics():
    file_manager = FileManager("topic")
    return file_manager.list_directories()


@app.route('/plans')
def list_plans():
    file_manager = FileManager("plan")
    return file_manager.list_directories()


@app.route('/topics/<topic>')
def list_files_in_topic(topic):
    topic_path = "topic/"
    if topic not in valid_topics:
        return "Error: Not a valid topic"
    file_manager = FileManager(topic_path + topic)
    return file_manager.list_files_in_directory()


@app.route('/topics/<topic>/<lesson>', methods=['GET'])
def get_lesson_from_topic(topic, lesson):
    # TODO: This seems hacky/brittle. Rewrite
    topic_path = "topic/"
    topic += "/"
    file_manager = FileManager(topic_path + topic)

    try:
        return send_file(file_manager.get_lesson_path(lesson), mimetype="audio/wav", as_attachment=True,
                         attachment_filename=lesson)
    except FileNotFoundError as e:
        return str(e)


@app.route('/plans/<plan>')
def list_files_in_plan(plan):
    plan_path = "plan/"

    if plan not in valid_plans:
        return "Error: Not a valid plan"
    file_manager = FileManager(plan_path + plan)
    return file_manager.list_files_in_directory()


@app.route('/plans/<plan>/<lesson>', methods=['GET'])
def get_lesson_from_plan(plan, lesson):
    plan_path = "plan/"
    plan += "/"

    file_manager = FileManager(plan_path + plan)
    print(file_manager.get_lesson_path(lesson))
    try:
        return send_file(file_manager.get_lesson_path(lesson), mimetype="audio/wav", as_attachment=True,
                         attachment_filename=lesson)
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

        # Users attempt
        file = request.files['file']

        # Retrieve the Lesson( How do we know what lesson the user recorded? Which folder is it in? )

        if file and app_utils.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            uploaded_file_path = app.config['UPLOAD_FOLDER'] + "/" + filename
            audio_analysis = AudioAnalysis(uploaded_file_path)

            # DEBUG
            print(audio_analysis.analyse_notes())
            print(audio_analysis.analyse_timing())
            ###

            user_note_list = audio_analysis.analyse_notes()
            user_timing_list = audio_analysis.analyse_timing()

            audio_comparison = AudioComparison(user_note_list, user_timing_list, user_note_list, user_timing_list)
            print(audio_comparison.compare_note_lists())
            print(audio_comparison.compare_timing_lists())
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
