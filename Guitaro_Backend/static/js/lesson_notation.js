import Vex from 'vexflow';
/*
var C7 = new Vex.Flow.StaveNote({ keys: ['C/4', 'E/4', 'G/4', 'Bb/4'], duration: '8'});
C7.setStyle({fillStyle: "blue", strokeStyle: "blue"});

*/

class NotationDrawer{
    constructor(tab_notation) {
        this.div = tab_notation
        this.VF = Vex.Flow;
        this.x = 500;
        this.y = 200;
        this.renderer = new this.VF.Renderer(this.div, this.VF.Renderer.Backends.SVG);
        this.renderer.resize(this.x, this.y);

        this.context = this.renderer.getContext();
        this.stave = new this.VF.TabStave(10, 40, 450);
        this.stave.addClef("tab").setContext(this.context).draw();

        this.notes = [];
        this.voice;
        this.formatter;

        this.note_x_coordinates = [];
        this.note_y_coordinates = [];
    }

    setNotes(tab_note){
        //Append ONE tab_note.Call it while there is notes left
        let vf_tab_note = new this.VF.TabNote(tab_note);
        this.notes.push(vf_tab_note);
    }

    setCoordinates(){
        for(let i = 0; i < this.notes.length; i++){
            this.note_x_coordinates.push(this.notes[i].getAbsoluteX());
            this.note_y_coordinates.push(this.notes[i].getYs());
        }
    }

    getCoordinates(){
        return {
            x_coordinates: this.note_x_coordinates,
            y_coordinates: this.note_y_coordinates
        };
    }


    printNotes(){
        for(let i = 0; i < this.notes.length; i++){
            console.log(this.notes[i].positions);
            console.log(this.notes[i].duration);
            console.log("abosulte x: " + this.notes[i].getAbsoluteX() + "y: " + this.notes[i].getYs());
        }

    }

    createVoice(beat_count){
        // Create a voice in 4/4 and add notes
        //NOTE: the num of beats has to match number of notes
        try{
            this.voice = new this.VF.Voice({num_beats: beat_count,  beat_value: 4});
            this.voice.addTickables(this.notes);
            this.voice.setStrict(false);
        }catch(err){
            console.log(err);
        }

    }

    formatAndJustify(){
        // Format and justify the notes to 400 pixels.
        this.formatter = new this.VF.Formatter().joinVoices([this.voice]).format([this.voice], 400);
    }

    render(){
        // Render voice
        this.voice.draw(this.context, this.stave);
    }
}


export function draw_tab(string_list,fret_list,note_durations,total_beats,element_name){

        let note_durations_length = note_durations.length;
        let tab_notation = document.getElementById(element_name);

        console.log(element_name);
        console.log(tab_notation);

        let fret_list_length = fret_list.length;

        let notationDrawer = new NotationDrawer(tab_notation);

        for(let i = 0; i < fret_list_length; i++){

            let str = string_list[i];
            let fret = fret_list[i];

            let note_duration = note_durations[i];

            let str_num = string_note_to_number_mapping[str];
            let dur = duration_mapping[note_duration];

            // It looks cleaner if I hard code it to be one single duration.
            let tab_note ={
                positions: [{str: str_num, fret: fret}],
                duration: "8"
            }
            try{
                notationDrawer.setNotes(tab_note);

            }catch(err){
                console.log(err);
                console.log("index of problem: " + i);
                console.log("fret: " + fret_list[i]);
                console.log("String: " + string_list[i]);
            }
        }


        notationDrawer.createVoice(total_beats);
        notationDrawer.formatAndJustify();
        notationDrawer.render();

        notationDrawer.setCoordinates();
        return notationDrawer.getCoordinates();
}

export function draw_chord(element_name){
    console.log("draw chord");
    let chord_notation = document.getElementById(element_name);

}



let string_note_to_number_mapping = {
    E: 6,
    A: 5,
    D: 4,
    G: 3,
    B: 2,
    e: 1
}

//for tab_note
let duration_mapping = {
    whole:"1",
    half:"2",
    quarter:"4",
    eight:"8",
    sixteenth:"16",
    thirty_second: "32"
}

let beat_count = {
    whole:"4",
    half:"2",
    quarter:"1",
    eight:"0.5",
    sixteenth:"0.25",
    thirty_second: "0.125"
}