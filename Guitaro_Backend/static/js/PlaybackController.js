class PlaybackController {
    constructor() {
        this.playbackAudioContext = new AudioContext();
        this.audioBuffer;
        this.source;
        this.isPlaying = false;
    }

    setAudioBuffer(audioBuffer){
        this.audioBuffer = audioBuffer;
    }
    printAudioBuffer(){
        console.log(this.audioBuffer);
    }

    getAudioContext(){
        return this.playbackAudioContext;
    }

    playAudio(){
        //const source = this.playbackAudioContext.createBufferSource();
        this.source = this.playbackAudioContext.createBufferSource();
        this.source.buffer = this.audioBuffer;
        this.source.connect(this.playbackAudioContext.destination);
        this.source.start();
        this.isPlaying = true;
    }

    stopAudio(){
        if(!this.source.stop){
            this.source.stop = source.noteOff;
        }
        this.source.stop(0);
        this.isPlaying = false;
    }

    pauseAudio(){
    if(this.playbackAudioContext.state == 'running'){
        this.playbackAudioContext.suspend();
        this.isPlaying = false;
        return "suspended";
    }
    else if(this.playbackAudioContext.state == 'suspended'){
        this.playbackAudioContext.resume();
        this.isPlaying = true;
        return "running";
    }
    }

    checkIsPlaying(){
        return this.isPlaying;
    }
}

module.exports = PlaybackController;


