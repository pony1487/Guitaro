import { loadWavIntoBuffer } from './audio_processor';

const CONFIG = require('./config.json');
let BASE_URL;
let TOPICS_URL;
let PLANS_URL;
let TOPICS_LIST;

// Set up local dev or prod aws
let environment = process.env.NODE_ENV === 'production' ? 'production' : 'development';

if(environment == 'production'){
    BASE_URL = CONFIG.awsUrl;
    TOPICS_URL = CONFIG.awsTopics;
    PLANS_URL = CONFIG.awsPlans;
}
else if(environment == 'development'){
    BASE_URL = CONFIG.localUrl;
    TOPICS_URL = CONFIG.localTopics;
    PLANS_URL = CONFIG.localPlans;
}

console.log("environment: " + environment);
console.log("BASE_URL: " + BASE_URL);
console.log("TOPICS_URL: " + TOPICS_URL);
console.log("PLANS_URL: " + PLANS_URL);

$(document).ready(function() {
    init();
});

function init(){
    console.log("loaded..");
    fetchTopics();
}

function fetchTopics(){
    fetch(TOPICS_URL)
    .then(response => response.json())
    .then(json => {

            TOPICS_LIST = json["directories"];
            createListItem(TOPICS_LIST,"topics_list");
            addEventListenerToTopic();

    })
    .catch(error => {
        console.log(error);
    });
}





function createListItem(array,elementid){
    /*
    Create a button for each item in the array and append them all to the list in topics.html
    <button id=<i> type="button" class="list-group-item list-group-item-action">Dapibus ac facilisis in</button>
    */
    let element = document.getElementById(elementid);
    for(let i = 0;i < array.length;i++){
        let btn = document.createElement('button');
        btn.innerText = array[i];
        btn.id = i;
        btn.className = "list-group-item list-group-item-action";
        element.appendChild(btn);

    }

    if(elementid != "topics_list"){
    let backbutton = document.createElement('button');
        backbutton.innerText = "Back";
        backbutton.addEventListener('click',click_back_button);

        element.appendChild(backbutton);
    }

    function click_back_button(e){
        $("#lessons_in_topic_container").hide();
        $("#topic_list_container").show();
    }
}

function addEventListenerToTopic(lesson_path){
    let ul = document.getElementById('topics_list');
    let buttons = ul.getElementsByTagName('button');

    for(let i = 0; i < buttons.length;i++)
    {
        buttons[i].addEventListener('click', clickPlan);
        buttons[i].myParam = lesson_path;
    }
}

function clickPlan(e){
    console.log(e.target.innerText);
    list_lesson_in_topic(e.target.innerText);
}

function list_lesson_in_topic(path){

    //clear any previous fetched lessons
    $("#lesson_in_topic_list").empty();

    // If it is a topic lesson
    if(TOPICS_LIST.includes(path)){
        let lesson_path = TOPICS_URL + "/" + path;
        fetch(lesson_path)
        .then(response => response.json())
        .then(json => {

            let list = json["files"];

            if(!$("#lessons_in_topic_container").is(":visible")){
                $("#lessons_in_topic_container").show();
            }

            $("#topic_list_container").hide();
            createListItem(list,"lesson_in_topic_list");
            addEventListenerToLesson(lesson_path);

        })
        .catch(error => {
            console.log(error);
        });
    }
}

function addEventListenerToLesson(lesson_path){
    let ul = document.getElementById('lesson_in_topic_list');
    let buttons = ul.getElementsByTagName('button');

    console.log("addEventListenerToLesson");
    for(let i = 0; i < buttons.length;i++)
    {
        buttons[i].addEventListener('click', clickLesson);
        buttons[i].myParam = lesson_path;

    }
}


function clickLesson(e){
    let url = e.target.myParam + "/" + e.target.innerText;

    //backbutton is a clickable list element as well.
    //dont change page to audioprocessor.html if user clicks back button
    if(e.target.innerText != "Back"){
        if (typeof(Storage) !== "undefined") {
            localStorage.setItem('url', url);
            try {
                window.location.href = Flask.url_for("audio_processor_page", {})
            }catch (e) {
                console.log(e);
            }

        } else {
            console.log("no local storage support");
        }
    }
}







