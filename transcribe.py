import whisper
from faster_whisper import WhisperModel
import torch

from functions import read_config

# whisper model
config = read_config('config.ini')
model_name = config.get('whisper', 'model_name')
language = config.get('whisper', 'language')
device = config.get('system', 'device')


whisper_model = WhisperModel(model_name, device = device, compute_type = "int8")

def transcribe_faster_whisper(audio, language = language, beam_size = 5):
    '''
    Here we wrap the faster_whisper model call which runs a lot faster and even trims out silences
    '''
    segments, _ = whisper_model.transcribe(audio, task = "transcribe", language = language, beam_size = beam_size,
                                           vad_filter = True, vad_parameters = dict(min_silence_duration_ms = 500))
    segments = list(segments)
    transcription = " ".join([segment.text for segment in segments])

    return transcription


# whisper_model = whisper.load_model(name = model_name, device = "cpu")
# # this quantization helps reduce whisper model time a little
# whisper_model = torch.quantization.quantize_dynamic(whisper_model, {torch.nn.Linear}, dtype = torch.qint8, inplace = True)

# def transcribe_whisper(audio, language = language, beam_size = 5):
#     '''
#     This is a wrapper to the standard whisper model transcribe call, it runs very slowly
#     '''
#     transcription = whisper_model.transcribe(audio, 
#                                             task = "transcribe", 
#                                             language = language, 
#                                             beam_size = beam_size)

#     return transcription['text']










# from transformers import AutoProcessor, AutoModelForCTC
# import librosa
# import numpy as np
# import torch
# import scipy
# from scipy.io import wavfile

# #
# processor = AutoProcessor.from_pretrained("facebook/wav2vec2-large-xlsr-53-spanish")
# model = AutoModelForCTC.from_pretrained("facebook/wav2vec2-large-xlsr-53-spanish")


#     # downsample audio
#     sample_rate, audio_data = wavfile.read(audio)
    
#     target_sample_rate = 16000  # Set your desired sample rate
#     if sample_rate != target_sample_rate:
#         num_samples = round(len(audio_data) * float(target_sample_rate) / sample_rate)
#         audio_data = scipy.signal.resample(audio_data, num_samples)
        
#     audio_data = torch.tensor(audio_data)
    
#     # audio = librosa.resample(np.array(audio).astype(np.float32), orig_sr = 48000, target_sr = 16000)
#     # # convert to tensor
#     # audio_data, sample_rate = tf.audio.decode_wav(tf.io.read_file(audio))
#     # print("#"*50, "Sample rate:", sample_rate)
#     # # reshape
#     # audio_data = tf.reshape(audio_data, [-1, 2])
#     # pass to processing model
#     inputs = processor(audio_data, return_tensors = "pt", sampling_rate = 16000)
#     # get predictions
#     with torch.no_grad():
#         logits = model(**inputs).logits
#         logits = logits.view(logits.shape[1], logits.shape[2], logits.shape[3])
#     predicted_ids = torch.argmax(logits, dim = -1)
#     # convert predictions back to text
#     transcription = processor.batch_decode(predicted_ids)