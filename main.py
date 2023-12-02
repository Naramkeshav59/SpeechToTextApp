import os
from flask import abort, current_app, jsonify, make_response, request, Flask, render_template, flash, redirect, url_for
from mimetypes import guess_extension
from werkzeug.utils import secure_filename
from model import asr_transcript, preprocess, PorterStemmer
import soundfile as sf
import asyncio
import torch
from transformers import WhisperProcessor, BertTokenizer
from flask_compress import Compress
import tensorflow as tf
import pickle as pkl
import librosa
import numpy as np
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re
from tensorflow.keras.models import load_model

app = Flask(__name__)
Compress(app)
UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'wav'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("main.html")

@app.route('/upload', methods=['POST', 'GET'])
async def upload():
    if request.method == 'POST':
        f = request.files['file']
        # Run the transcription asynchronously
        loop = asyncio.get_event_loop()
        text = await loop.run_in_executor(None, lambda: asr_transcript(f, app.model, app.processor,app.ps,app.encoder,app.cv,app.loaded_model))
        return text

if __name__ == "__main__":
    app.model = torch.load("whisper.pt")
    app.loaded_model = load_model("emoRecog.h5", compile=False)
    app.loaded_model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    app.ps = PorterStemmer()
    with open("encoder.pkl", "rb") as file:
        app.encoder = pkl.load(file)
    with open("CountVectorizer.pkl", "rb") as file:
        app.cv = pkl.load(file)
    app.processor = WhisperProcessor.from_pretrained("openai/whisper-medium.en") 
    app.run(debug=True, host='0.0.0.0', port=8000)
