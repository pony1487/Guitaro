import { init_notation,draw_tab,draw_chord } from './lesson_notation';

export function processFeedbackJSON(feedBackObj){

    let user_string_list = feedBackObj.user_string_list;
    let user_fret_list = feedBackObj.user_fret_list;
    let wrong_note_indexes = feedBackObj.wrong_note_indexes;


    let user_note_durations = feedBackObj.user_duration_list;
    let user_total_beats = feedBackObj.total_beats;


    ///////////////////////////////////
    //Test data as I dont have a guitar to play in the library
    ///////////////////////////////////
    // let user_fret_list = [5,8,4,7,6,7]
    // let user_note_list = ["A","C","C#","E","G#","A"]
    // let user_string_list = ["E","E","A","A","D","D"]
    // let wrong_note_indexes = [2,4];

    // let user_fret_list = [3,6,3,5,5,3,5,3,6,3,6];
    // let user_note_list = ["G","Bb","C","D","G","Bb","C","D","F","G","Bb"];
    // let user_string_list = ["E","E","A","A","D","G","G","B","B","e","e"];


    // let user_fret_list = [8,10,7,8,10,7,9,10]
    // let user_note_list = ["C","D","E","F","G","A","B","C"]
    // let user_string_list = ["E","E","A","A","A","D","D","D"]

    /////////////////////////////////////////////

    //draw user
    let note_coordinates = draw_tab(user_string_list,user_fret_list,user_note_durations,user_total_beats,"user_notation");
    let success = draw_feedback_overlay(note_coordinates,wrong_note_indexes);


    if(!success){
        let lesson_name_p = document.getElementById('lesson_name');
        let lesson_bpm_p = document.getElementById('lesson_bpm');
        let lesson_feedback_p = document.getElementById('lesson_feedback');
        let lesson_note_duration_p = document.getElementById('lesson_note_duration');
        let user_note_duration_p = document.getElementById('user_note_duration');
        let timing_difference_p = document.getElementById('timing_difference');
        let wrong_notes_played_p = document.getElementById('wrong_notes_played');

        lesson_name_p.textContent = "Lesson Name: " +  feedBackObj.lesson;
        lesson_bpm_p.textContent = "Lesson BPM: " +  feedBackObj.lesson_tempo;
        lesson_feedback_p.textContent = "Feedback: " +  feedBackObj.feedback;
        lesson_note_duration_p.textContent = "Lesson Note Durations: " + feedBackObj.lesson_note_durations;
        user_note_duration_p.textContent = "Your Note Durations: " +  feedBackObj.user_note_durations;
        timing_difference_p.textContent = "Timing Difference: " + feedBackObj.percentage_difference;
        wrong_notes_played_p.textContent = "Wrong Notes Played: " + feedBackObj.notes_not_in_lesson;
    }
}

export function process_chord_feedback(feedBackObj){

    console.log(feedBackObj);
    draw_chord("user_notation");

    let lesson_name_p = document.getElementById('lesson_name');
    lesson_name_p.textContent = "Lesson Name: " +  feedBackObj.lesson;

    let lesson_feedback_p = document.getElementById('lesson_feedback');
    lesson_feedback_p.textContent = "Feedback: " +  feedBackObj.feedback;

    let lesson_lesson_notes_p = document.getElementById('lesson_note_list');
    lesson_lesson_notes_p.textContent = "Lesson Notes: " +  feedBackObj.lesson_note_list;

    let lesson_user_note_list_p = document.getElementById('user_note_list');
    lesson_user_note_list_p.textContent = "User Notes: " +  feedBackObj.user_note_list;
}


function draw_feedback_overlay(coordinate_obj,wrong_note_indexes){

    //Return zero if the user played it correctly, if not return 1
    if(!Array.isArray(wrong_note_indexes) || !wrong_note_indexes.length) {
        //wrong_note_indexes is empty,so the user played it correctly or the array doenst exist
        //WELL DONE!
        //TO DO
        let lesson_feedback_p = document.getElementById('lesson_feedback');
        lesson_feedback_p.textContent = "Feedback: Nailed it! Well Done!";

        return 0;

    }
    else{
        //draw the feedback
        let canvas = document.getElementById("userNotationCanvas");
        let ctx = canvas.getContext("2d");

        let rect_width = 15;
        let rect_height = 15;


        ctx.moveTo(0, 0);
        ctx.fillStyle = "red";


        let x_coordinates = coordinate_obj.x_coordinates;
        let y_coordinates = coordinate_obj.y_coordinates;

        for(let i = 0;i < wrong_note_indexes.length;i++){
            let wrong_note_index = wrong_note_indexes[i];

            let x = x_coordinates[wrong_note_index];
            let y = y_coordinates[wrong_note_index];

            //Draw the rect at the center rather than the top left
            let new_x = x - rect_width / 2
            let new_y = y - rect_height / 2

            ctx.fillRect(new_x,new_y,rect_height,rect_width);

        }
        return 1;
    }
}
