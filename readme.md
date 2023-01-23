This is a client-server architectural Web App made using flask micro framework webservice which is a Speech to Text web application.
## Folder structure and details:
```
.
├── __pycache__ (all the python cache will be here. Not important)
│   └── model.cpython-39.pyc
├── main.py (flask server to receive the audio chunk(request) and return the transcript(response)) 
├── model.py (Models can be trained finetuned here. Includes a function for inferencing which is imported ro main.py) 
├── readme.md (The present text file you are viewing right now)
├── requirements.txt (python dependencies)
├── static (folder for managing static files for the UI part)
│   ├── css
│   │   └── style.css (Basic styling is done here) 
│   └── js (folder containing javascript files)
│       ├── chunk.js (for creating chunks using vad.js and send them to the server using AJAX)
│       ├── recorder.js (for recording the audio using browser's webrtc)
│       └── vad.js      (vad is performed in real-time and we can make decisions based on vad using this)
├── templates
│   └── main.html       (to put together all JavaScript logic and interfacing them to the buttons etc.,).
└── uploads
    └── audio.wav       (temporary file in which the audio chunk from the client is stored and processed in the server for the transcript)
```

## For running demo in your PC locally: (make sure you have git in your system)

1. clone this repository </br> ``` git clone https://github.com/Naramkeshav59/SpeechToTextApp/```
2. navigate to SpeechToText folder in the terminal.
3. create a python virtual environment and activate it. refer <a href ='https://docs.python.org/3/library/venv.html'>virtual environment using venv </a>
4. Install dependencies: </br> ```pip install -r requirements.txt ``` 
5. Run the flask server </br> ```python main.py```
6. The above will take some time for the first time while running reason being it should download the models. Later it won't take much time.
7. Open <a href = 'http://127.0.0.1:8000/'> </a> for testing the app.
8. Cheers that's all we have to do 🥂🥂...




