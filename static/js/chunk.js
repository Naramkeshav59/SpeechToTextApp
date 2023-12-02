//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream; 						//stream from getUserMedia()
var rec; 							//Recorder.js object
var input; 							//MediaStreamAudioSourceNode we'll be recording
function startUserMedia(stream) {
	// Create MediaStreamAudioSourceNode
	var source = audioContext.createMediaStreamSource(stream);

	// Setup options
	var options = {
	 source: source,
	 voice_stop: function() {document.getElementById('status').innerHTML = "silent";
	makeChunk();
	startRecording();
}, 
	 voice_start: function() {document.getElementById('status').innerHTML = "speaking"}
	}; 
	
	// Create VAD
	var vad = new VAD(options);
  }

// shim for AudioContext when it's not avb. 
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record

var recordButton = document.getElementById("Start");
var stopButton = document.getElementById("Stop");


//add events to those 2 buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);




function startRecording() {
	console.log("recordButton clicked");
	document.getElementById("outp").innerHTML = "";

	/*
		Simple constraints object, for more advanced audio features see
		https://addpipe.com/blog/audio-constraints-getusermedia/
	*/

    var constraints = { audio: true, video:false }

 	/*
    	Disable the record button until we get a success or fail from getUserMedia() 
	*/

	recordButton.disabled = true;
	stopButton.disabled = false;
	

	/*
    	We're using the standard promise based getUserMedia() 
    	https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
	*/

	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
		console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

		/*
			create an audio context after getUserMedia is called
			sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
			the sampleRate defaults to the one set in your OS for your playback device
		*/
		audioContext = new AudioContext({
			sampleRate: 16000,
		  });
		

		/*  assign to gumStream for later use  */
		gumStream = stream;
		startUserMedia(gumStream);
		/* use the stream */
		input = audioContext.createMediaStreamSource(stream);

		/* 
			Create the Recorder object and configure to record mono sound (1 channel)
			Recording 2 channels  will double the file size
		*/
		rec = new Recorder(input,{numChannels:1})
      

		//start the recording process
		rec.record()

		console.log("Recording started");

	}).catch(function(err) {
        
	  	//enable the record button if getUserMedia() fails
    	recordButton.disabled = false;
    	stopButton.disabled = true;
    
	});
}


function stopRecording() {
	
	//disable the stop button, enable the record too allow for new recordings
	stopButton.disabled = true;

	recordButton.disabled = false;
	
	location.reload();
}

function makeChunk(){
	console.log("Audio chunk created");
	//tell the recorder to stop the recording
	rec.stop();
	gumStream.getAudioTracks()[0].stop();
	//create the wav blob and pass it on to createDownloadLink
	rec.exportWAV(createDownloadLink);

}

function createDownloadLink(blob) {
    var url = URL.createObjectURL(blob);
    var au = document.createElement('audio');
    var li = document.createElement('li');
    var link = document.createElement('a');
	var filename 
    //add controls to the <audio> element 
    au.controls = true;
    au.src = url;
    //link the a element to the blob 
    link.href = url;
    filename = new Date().toISOString() + '.wav';
	link.download = filename;
    link.innerHTML = link.download;
    //add the new audio and a elements to the li element 
    li.appendChild(au);
    li.appendChild(link);
    //add the li element to the ordered list 
    recordingsList.appendChild(li);
	sendAudioToServer(blob,filename);
	
}
function sendAudioToServer(blob,filename) {
	var xhr = new XMLHttpRequest();
	let fd = new FormData();
	fd.append("file",blob,"audio.wav"); 
	xhr.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
		  document.getElementById("outp").innerHTML =
		  this.responseText;
		}
	  };
	xhr.open("POST","/upload",true);
	xhr.send(fd);

}