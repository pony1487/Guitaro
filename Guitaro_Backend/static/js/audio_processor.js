// /*
// Code for recording audio was modified from these sources/tutorials:
// https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API
// https://addpipe.com/blog/using-recorder-js-to-capture-wav-audio-in-your-html5-web-site/
// */

import { stopRecording,recordLesson } from './audio_recorder';
import { draw_tab } from './lesson_notation';

const PlaybackController = require('./PlaybackController.js');
let playbackController = new PlaybackController();

$(document).ready(function() {
    console.log("Document Ready");
    console.log("user_agent: " + navigator.userAgent);

    fetchLessonToBeNotated();
    loadWavIntoBuffer();

    if(check_for_mobile_browser()){
        console.log("Mobile browser detected");
        init('touchstart');
    }
    else if(!check_for_mobile_browser()){
        console.log("Desktop browser detected");
        init('click');
    }

    $("#record_button").click(function(){
        let record_button = document.getElementById("record_button");
        record_button.className = "btn btn-danger";
        record_button.innerText = "Recording";
    });

    $("#stop_button").click(function(){
        let record_button = document.getElementById("record_button");
        record_button.className = "btn btn-secondary";
        record_button.innerText = "Record";

    });

    $("#play_button").click(function(){
        let play_button = document.getElementById("play_button");
        play_button.className = "btn btn-success";
        play_button.innerText = "Playing";
        console.log(playbackController.checkIsPlaying());

    });

    $("#stop_playing_button").click(function(){
        let play_button = document.getElementById("play_button");
        play_button.className = "btn btn-secondary";
        play_button.innerText = "Play";
        console.log(playbackController.checkIsPlaying());

    });
});


function check_for_mobile_browser() { 
    /*
    Source: https://stackoverflow.com/questions/11381673/detecting-a-mobile-browser
    */
   console.log("check_for_mobile_browser()");
   var check = false;
   (function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);
   return check;
}


function init(event_type){
    console.log("init");
    setHeaderToLessonName(localStorage.getItem("url"));

    let play_button = document.getElementById('play_button');
    play_button.addEventListener(event_type, playLesson);

    let stop_button = document.getElementById('stop_playing_button');
    stop_button.addEventListener(event_type, stopLessonPlaying);

    let pause_button = document.getElementById('pause_button');
    pause_button.addEventListener(event_type, pauseLesson);

    let record_button = document.getElementById('record_button');
    record_button.addEventListener(event_type, recordLesson);

    let stop_recording_button = document.getElementById('stop_button');
    stop_recording_button.addEventListener(event_type, stopRecording);

}


function fetchLessonToBeNotated(){
    //http://127.0.0.1:5000/notation/topics/picking/A_minor_pentatonic_ascending-95.wav
    //http://127.0.0.1:5000/topics/picking/A_minor_pentatonic_ascending-95.wav

    let url = localStorage.getItem("url");

    let notation_url = constructNotationUrl(url);


    if(notation_url.includes("chord-notation")){
        fetch(notation_url)
        .then(response => response.blob())
        .then(image => {
            
            let chord_image_url = URL.createObjectURL(image)
            let image_tag = document.getElementById('chord_image');
            image_tag.src = chord_image_url;

        })
        .catch(error =>{
            console.log(error)
        })
    }else{

        fetch(notation_url)
        .then(response => response.json())
        .then(json => {

            let lesson_fret_list = json.lesson_fret_list;
            let lesson_string_list = json.lesson_string_list;
            let duration_list = json.padded_duration_list;
            let total_beats = json.total_beats;

            // Store bpm for use in audio_recorder.js to determine count in
            localStorage.setItem("bpm", json.bpm);
            draw_tab(lesson_string_list,lesson_fret_list,duration_list,total_beats,"lesson_notation");
        })
        .catch(error => {
            console.log(error);
        });
    }
}


function loadWavIntoBuffer(){
    let url = localStorage.getItem("url");

    fetch(url)
    .then(response => response.arrayBuffer())
    .catch(error =>{
        console.log(error);
    })
    .then(arrayBuffer => {
        let pbc = playbackController.getAudioContext();
        return pbc.decodeAudioData(arrayBuffer);
    })
    .catch(error =>{
        console.log(error);
    })
    .then(audioBuffer => {
        return audioBuffer;
    })
    .catch(error =>{
        console.log(error);
    })
    .then(audioBuffer =>{
        playbackController.setAudioBuffer(audioBuffer);
        playbackController.printAudioBuffer();

    }).catch(error =>{
        alert("Something went wrong: Could not fetch audio file!");
        console.log(error);
    });


}


function playLesson(e){
    playbackController.playAudio();
}

function stopLessonPlaying(e){
    playbackController.stopAudio();
}

function pauseLesson(e){
    let btn = document.getElementById('pause_button');
    let state = playbackController.pauseAudio();
    console.log(state);
	if(state == 'running'){
        btn.innerText = "Resume";
        btn.className = "btn btn-secondary";

	}
	else if(state == 'suspended'){
        btn.innerText = "Suspended";
        btn.className = "btn btn-warning";
	}
}

function setHeaderToLessonName(url){

    let header = document.getElementById('lesson_header');
    let parser = document.createElement('a');
    parser.href = url;
    let arr = parser.pathname.split("/");
    header.innerText += ": " +  arr[3];

}

function constructNotationUrl(url){
    /*
    parser.protocol; // => "http:"
    parser.host;     // => "example.com:3000"
    parser.hostname; // => "example.com"
    parser.port;     // => "3000"
    parser.pathname; // => "/pathname/"
    parser.hash;     // => "#hash"
    parser.search;   // => "?search=test"
    parser.origin;

    */
    let parser = document.createElement('a');
    parser.href = url;

    let notationUrl;

    //check if its a chord lesson or a regular
    if(parser.pathname.includes("chord")){
        notationUrl = parser.origin + "/" + "chord-notation" + parser.pathname;
    }
    else{
        notationUrl = parser.origin + "/" + "notation" + parser.pathname;
    }
    return notationUrl;
}
