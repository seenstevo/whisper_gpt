from gtts import gTTS
import playsound
import time
import configparser


def speak(text):
    '''
    Using the gtts and playsound libraries, voice synthesise the GPT output.
    '''
    tts = gTTS(text, lang = 'es')
    tts.save('speak.mp3')
    playsound.playsound('speak.mp3')
    
    
def time_stage(start, stage: str):
    '''
    Print out the time taken to run each step
    '''
    stop = time.time()
    print(f"finished stage {stage} in {round((stop - start), 2)}s")
    return stop


def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config