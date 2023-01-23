import os
from flask import abort, current_app, jsonify, make_response, request,Flask, render_template,flash,redirect,url_for
from mimetypes import guess_extension
from werkzeug.utils import secure_filename
#from model import ASRInference 
from model import asr_transcript
import soundfile as sf

#asr = ASRInference()
#i = 0  #for file name index
app = Flask(__name__)
UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'wav'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__,template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route("/")
def home():
    return render_template("main.html")

@app.route('/upload', methods = ['POST','GET'])
def upload():
    """ audio_data = request.files.get("audio_data")
     with sr.AudioFile(audio_data) as source:
          # listen for the data (load audio to memory)
          audio = r.record(source)
     # recognize (convert from speech to text)
     text = r.recognize_google(audio)
     return jsonify(text)"""
    if request.method == 'POST':
      f = request.files['file']
      # with open('./uploads/audio.wav','wb') as audio:
      #   f.save(audio)
      #aud,fs= sf.read('uploads/audio.wav')
      #text = asr.inference(aud)
      #text = asr_transcript('uploads/audio.wav')
      text = asr_transcript(f)
      return text






if __name__ == "__main__":
  app.run(debug=True,host ='0.0.0.0',port =8000)