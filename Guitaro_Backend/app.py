from flask import Flask, jsonify, request, send_file, render_template, Response
from FileManager import FileManager
from AudioAnalysis import AudioAnalysis
from AudioComparison import AudioComparison
from PracticeGenerator import PracticeGenerator
from Notation import Notation
from chordrecognition.ChordAnalyser import ChordAnalyser
from chordrecognition.ChordComparison import ChordComparison
from guitaroconfig import valid_directories, valid_topics, valid_plans
from werkzeug.utils import secure_filename
from flask_cors import CORS

import os
import guitaroconfig
import app_utils
import json

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = guitaroconfig.UPLOAD_FOLDER


@app.route('/')
def welcome():
    return render_template("upload.html")


@app.route('/topics')
def list_topics():
    file_manager = FileManager("topics")
    return jsonify(file_manager.list_directories())


@app.route('/plans')
def list_plans():
    file_manager = FileManager("plans")
    return jsonify(file_manager.list_directories())


@app.route('/topics/<topic>')
def list_files_in_topic(topic):
    topic_path = "topics/"
    if topic not in valid_topics:
        return "Error: Not a valid topic"
    file_manager = FileManager(topic_path + topic)
    return jsonify(file_manager.list_files_in_directory())


@app.route('/topics/<topic>/<lesson>', methods=['GET'])
def get_lesson_from_topic(topic, lesson):
    # TODO: This seems hacky/brittle. Rewrite
    topic_path = "topics/"
    topic += "/"
    file_manager = FileManager(topic_path + topic)

    try:
        return send_file(file_manager.get_lesson_path(lesson), mimetype="audio/wav", as_attachment=True,
                         attachment_filename=lesson)
    except FileNotFoundError as e:
        return str(e)


# Notate regurlar lessons
@app.route('/notation/topics/<topic>/<lesson>', methods=['GET'])
def get_lesson_notation(topic, lesson):
    print("Test notation")
    topic_path = "topics/"
    topic += "/"
    file_manager = FileManager(topic_path + topic)

    bpm = file_manager.get_tempo_from_file_name(lesson)

    lesson_file_path = file_manager.get_lesson_path("/" + lesson)

    lesson_analysis = AudioAnalysis(lesson_file_path)

    lesson_note_list, lesson_freq_list = lesson_analysis.analyse_notes()
    lesson_timing_list = lesson_analysis.analyse_timing()

    lesson_notation_creator = Notation(lesson_freq_list, lesson_timing_list, bpm)

    lesson_string_list = lesson_notation_creator.get_strings_to_be_played()
    lesson_fret_list = lesson_notation_creator.get_frets_to_be_played()
    padded_duration_list = lesson_notation_creator.get_padded_duration_list()

    total_beats = lesson_notation_creator.calculate_total_beats(padded_duration_list)

    d = app_utils.create_dictionary(lesson_string_list=lesson_string_list, lesson_fret_list=lesson_fret_list,
                                    padded_duration_list=padded_duration_list, total_beats=total_beats, bpm=bpm)
    return jsonify(d)


# Notate chord lesson
@app.route('/chord-notation/plans/<plan>/<lesson>', methods=['GET'])
def get_chord_notation(plan, lesson):
    plan_path = "plans/"
    plan += "/"
    file_manager = FileManager(plan_path + plan)

    #DEBUG
    d = {
        "lesson_fret_list":[],
        "lesson_string_list":[],
        "duration_list": [],
        "total_beats": 4
    }
    return jsonify(d)



@app.route('/plans/<plan>')
def list_files_in_plan(plan):
    plan_path = "plans/"

    if plan not in valid_plans:
        return "Error: Not a valid plan"
    file_manager = FileManager(plan_path + plan)
    return jsonify(file_manager.list_files_in_directory())


@app.route('/plans/<plan>/<lesson>', methods=['GET'])
def get_lesson_from_plan(plan, lesson):
    plan_path = "plans/"
    plan += "/"

    file_manager = FileManager(plan_path + plan)
    print(file_manager.get_lesson_path(lesson))
    try:
        return send_file(file_manager.get_lesson_path(lesson), mimetype="audio/wav", as_attachment=True,
                         attachment_filename=lesson)
    except FileNotFoundError as e:
        return str(e)


@app.route('/analyse/<dirone>/<dirtwo>/<lesson>', methods=['POST'])
def analyse_user_recording(dirone, dirtwo, lesson):
    """
    Pattern taken from http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
    The route contains the path to the lesson the user is attempting. This is needed to get the lesson and analyse it.
    :return:
    """

    if request.method == 'POST':
        if 'file' not in request.files:
            print("no file uploaded")
            return "Error: No File uploaded"

        # Users attempt
        file = request.files['file']

        print(file.filename)

        # Path to where the lesson the user attempted is stored
        lesson_path = "{}/{}".format(dirone, dirtwo)

        file_manager = FileManager(lesson_path)
        lesson_file_path = file_manager.get_lesson_path("/" + lesson)
        bpm = file_manager.get_tempo_from_file_name(lesson)

        if file and app_utils.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Save user file to be analysed
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            uploaded_file_path = app.config['UPLOAD_FOLDER'] + "/" + filename
            user_audio_analysis = AudioAnalysis(uploaded_file_path)

            # Analyse the lesson and the users attempt
            lesson_analysis = AudioAnalysis(lesson_file_path)

            user_note_list, user_freq_list = user_audio_analysis.analyse_notes()
            user_timing_list = user_audio_analysis.analyse_timing()

            lesson_note_list, lesson_freq_list = lesson_analysis.analyse_notes()
            lesson_timing_list = lesson_analysis.analyse_timing()

            print("Lessons_freq_list" + str(lesson_freq_list))

            print("user_freq_list" + str(user_freq_list))

            # Generate the Notation Infromation
            user_notation_creator = Notation(user_freq_list, user_timing_list, bpm)

            user_string_list = user_notation_creator.get_strings_to_be_played()
            user_fret_list = user_notation_creator.get_frets_to_be_played()
            user_duration_list = user_notation_creator.get_padded_duration_list()
            total_beats = user_notation_creator.calculate_total_beats(user_duration_list)

            # Compare the lesson and the users attempt
            audio_comparison = AudioComparison(lesson, lesson_note_list, lesson_timing_list, user_note_list,
                                               user_timing_list, bpm, user_string_list, user_fret_list,
                                               user_duration_list, total_beats)

            return jsonify(audio_comparison.get_comparision_dict())
        else:
            return "Wrong File type: Must be wav"


@app.route('/analyse-chords/<dirone>/<dirtwo>/<lesson>', methods=['POST'])
def analyse_user_chords(dirone, dirtwo, lesson):
    if request.method == 'POST':
        if 'file' not in request.files:
            print("no file uploaded")
            return "Error: No File uploaded"

        # Users attempt
        file = request.files['file']

        # Path to where the lesson the user attempted is stored
        lesson_path = "{}/{}".format(dirone, dirtwo)

        file_manager = FileManager(lesson_path)
        lesson_file_path = file_manager.get_lesson_path("/" + lesson)

        if file and app_utils.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Save user file to be analysed
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            uploaded_file_path = app.config['UPLOAD_FOLDER'] + "/" + filename

            user_chord_analyser = ChordAnalyser(uploaded_file_path)
            user_chroma_list = user_chord_analyser.compute_chromagram()
            user_note_list = user_chord_analyser.get_notes_of_chord(user_chroma_list)

            lesson_chord_analyser = ChordAnalyser(lesson_file_path)
            lesson_chroma_list = lesson_chord_analyser.compute_chromagram()
            lesson_note_list = lesson_chord_analyser.get_notes_of_chord(lesson_chroma_list)

            chord_comparision = ChordComparison(lesson, user_note_list, lesson_note_list)
            return jsonify(chord_comparision.get_comparision_dict())
        else:
            return "Wrong File type: Must be wav"


@app.route('/practice-generator')
def practice_generator_form():
    """
    This is for testing only. When creating client use the topics route to populate the select list
    :return:
    """
    file_manager = FileManager("topic")
    topics_str = file_manager.list_directories()

    # convert from str
    json_of_topics = json.loads(topics_str)
    topic_list = json_of_topics['directories']
    return render_template("practice_generator.html", list_of_topics=topic_list)


@app.route('/generate-routine', methods=['POST'])
def generate_routine():
    if request.method == 'POST':
        multiselect = request.form.getlist('Topics')
        time = request.form['Time']

        form_dict = dict()
        form_dict["topics"] = multiselect
        form_dict["time"] = time

        # DEBUG. Will need to handle multiple topics
        single_topic = multiselect[0]
        practice_generator = PracticeGenerator(single_topic)
        practice_generator.get_topic_path()
        practice_generator.get_random_lesson_names()

        return jsonify(form_dict)
    return Response(status=400)


@app.route('/test-post', methods=['POST'])
def test_post():
    if request.method == 'POST':
        d = dict()
        d["message"] = "Success"
        print(d)
        return jsonify(d)
    return Response(status=400)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
