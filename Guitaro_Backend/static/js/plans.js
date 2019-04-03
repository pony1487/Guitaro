const CONFIG = require('./config.json');
let BASE_URL;
let TOPICS_URL;
let PLANS_URL;
let PLANS_LIST;

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

console.log(environment);
console.log(BASE_URL);
console.log(TOPICS_URL);
console.log(PLANS_URL);

$(document).ready(function() {

    //DOM manipulation code
    init();

});
function init(){
    console.log("loaded..");
    fetchPlans();
}

function fetchPlans(){
    fetch(PLANS_URL)
    .then(response => response.json())
    .then(json => {
        PLANS_LIST = json["directories"];
        //console.log(PLANS_LIST);
        createListItem(PLANS_LIST,"plans_list");
        addEventListenerToPlan();
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
        console.log(array[i]);
        let btn = document.createElement('button');
        btn.innerText = array[i];
        btn.id = i;
        btn.className = "list-group-item list-group-item-action";
        element.appendChild(btn);

    }

    if(elementid != "plans_list"){
    let backbutton = document.createElement('button');
        backbutton.innerText = "Back";
        backbutton.addEventListener('click',click_back_button);

        function click_back_button(e){
            console.log("Click");
            $("#lessons_in_plan_container").hide();
            $("#plans_list_container").show();
        }

        element.appendChild(backbutton);
    }
}

function addEventListenerToPlan(lesson_path){
    let ul = document.getElementById('plans_list');
    let buttons = ul.getElementsByTagName('button');

    for(let i = 0; i < buttons.length;i++)
    {
        buttons[i].addEventListener('click', clickPlan);
        buttons[i].myParam = lesson_path;
    }
}

function clickPlan(e){
    //console.log(e.target.innerText);
    list_lesson_in_plan(e.target.innerText);
}

function list_lesson_in_plan(path){
    //clear any previous fetched lessons
    $("#lesson_in_plan_list").empty();

    // If it is a plan lesson
    if(PLANS_LIST.includes(path)){
        let lesson_path = PLANS_URL + "/" + path;
        console.log(lesson_path);

        fetch(lesson_path)
        .then(response => response.json())
        .then(json => {
            let list = json["files"];
            console.log(list);

            if(!$("#lessons_in_plan_container").is(":visible")){
                $("#lessons_in_plan_container").show();
            }

            $("#plans_list_container").hide();
            createListItem(list,"lesson_in_plan_list");
            addEventListenerToLesson(lesson_path);
        })
        .catch(error => {
            console.log(error);
        });
    }
}

function addEventListenerToLesson(lesson_path){
    let ul = document.getElementById('lesson_in_plan_list');
    let buttons = ul.getElementsByTagName('button');

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







