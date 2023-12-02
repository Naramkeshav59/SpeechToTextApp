import librosa
import numpy as np
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re
import pickle as pkl
import tensorflow as tf
from tensorflow.keras.models import load_model

def asr_transcript(input_file, model, processor, ps,encoder, cv, recog_model):
    # Read the WAV file
    audio_data, sample_rate = librosa.load(input_file)
    
    # Process the audio and transcribe it
    input_features = processor(audio_data, sample_rate, return_tensors="pt").input_features
    predicted_ids = model.generate(input_features)
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
    text = transcription[0]
    text=preprocess(text,ps)
    array = cv.transform([text]).toarray()
    pred = recog_model.predict(array)
    a=np.argmax(pred, axis=1)
    output = """{}
                Emotion: {}
             """.format(transcription[0], encoder.inverse_transform(a)[0])
    return output


def preprocess(line,ps):
    review = re.sub('[^a-zA-Z]', ' ', line) #leave only characters from a to z
    review = review.lower() #lower the text
    review = review.split() #turn string into list of words
    #apply Stemming 
    review = [ps.stem(word) for word in review if not word in stopwords.words('english')] #delete stop words like I, and ,OR   review = ' '.join(review)
    #trun list into sentences
    return " ".join(review)
