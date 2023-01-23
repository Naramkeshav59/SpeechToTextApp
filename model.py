# from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
# import torch
# import numpy as np
# import soundfile as sf

# class ASRInference:
#     def __init__(self, model_name='patrickvonplaten/wav2vec2-base-100h-with-lm'):
#         self.model = Wav2Vec2ForCTC.from_pretrained(model_name)
#         self.processor = Wav2Vec2Processor.from_pretrained(model_name)
    
#     def inference(self, audio):
#         inputs = self.processor(audio, sampling_rate=16_000, return_tensors="pt")
#         with torch.no_grad():
#             logits = self.model(**inputs).logits
#         predicted_ids = torch.argmax(logits, dim=-1)
#         text = self.processor.decode(predicted_ids[0]).lower()
#         return text

#Importing all the necessary packages
import nltk
import librosa
import torch
from transformers import Wav2Vec2Tokenizer, Wav2Vec2ForCTC

nltk.download("punkt")

#Loading the pre-trained model and the tokenizer
model_name = "facebook/wav2vec2-base-960h"
#model_name = "ai4bharat/indicwav2vec-hindi"
tokenizer = Wav2Vec2Tokenizer.from_pretrained(model_name)
model = Wav2Vec2ForCTC.from_pretrained(model_name)

def load_data(input_file):

  #reading the file
  speech, sample_rate = librosa.load(input_file)
  #make it 1-D
  if len(speech.shape) > 1: 
      speech = speech[:,0] + speech[:,1]
  #Resampling the audio at 16KHz
  if sample_rate !=16000:
    speech = librosa.resample(speech, sample_rate,16000)
  return speech


def correct_casing(input_sentence):

  sentences = nltk.sent_tokenize(input_sentence)
  return (' '.join([s.replace(s[0],s[0].capitalize(),1) for s in sentences]))

def asr_transcript(input_file):

  speech = load_data(input_file)
  #Tokenize
  input_values = tokenizer(speech, return_tensors="pt").input_values
  #Take logits
  logits = model(input_values).logits
  #Take argmax
  predicted_ids = torch.argmax(logits, dim=-1)
  #Get the words from predicted word ids
  transcription = tokenizer.decode(predicted_ids[0])
  #Correcting the letter casing
  #transcription = correct_casing(transcription.lower())
  return transcription
