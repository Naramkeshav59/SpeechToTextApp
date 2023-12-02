This is a client-server architectural Speech to Text web application made using flask micro framework. This app enables to get transcript and emotion for real-time english speech. (I am still working to reduce latency) 

## For running demo in your PC locally: (make sure you have git in your PC)

1. clone this repository </br> ``` git clone https://github.com/Naramkeshav59/SpeechToTextApp/```
2. navigate to SpeechToText folder in the terminal.
3. create a python virtual environment and activate it. refer <a href ='https://docs.python.org/3/library/venv.html'>virtual environment using venv </a>
4. Install dependencies: </br> ```pip install -r requirements.txt ```
5. Download the <a href = 'https://openaipublic.azureedge.net/main/whisper/models/d7440d1dc186f76616474e0ff0b3b6b879abc9d1a4926b7adfa41db2d497ab4f/medium.en.pt'>whisper model </a> .
6. Replace the path of whisper model in ```main.py``` with the downloaded path in the line  </br>```app.model = torch.load("</path/to/whisper/model>")```
7. Run the flask server </br> ```python main.py```
8. Open this <a href = 'http://127.0.0.1:8000/'> link </a> for testing the app in your browser locally.
9. Cheers!! that's all we have to do 🥂🥂...




