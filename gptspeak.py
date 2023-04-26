import gradio as gr
import requests
import whisper
import openai
import time
import pyttsx3

import api_key

openai.api_key = api_key.API_KEY

# whisper model
model = whisper.load_model("small")


# set up the gpt3.5 model system prompt
#content = 'As a Spanish teacher and language assistant, you will be teaching and assisting a native English-speaking student who has an intermediate-advanced level of Spanish. The student will communicate with you in Spanish using voice-to-text technology, which may result in transcription errors. Each of your responses will consist of two parts: the first part, labeled "inference," will indicate what you infer the text should have been, considering any transcription errors. If you do not infer any errors in transcription, the "inference" text will simply be "OK." After providing your inference, you will give your "response", simulating a conversation in Spanish. This will continue until the student says "conversation over." At this point, you will analyze the conversation and create a bullet-point summary of any grammar errors or tips for improving the choice of words.'
content = 'As a Spanish teacher and language assistant, you will be teaching and assisting a native English-speaking student. The student will communicate with you in Spanish using voice-to-text technology, which may result in transcription errors. You will give short but naturalist responses in Spanish, taking into account any possible transcription errors, that allow a conversation to flow. This will continue until the student says "hemos terminado." At this point, you will analyze the conversation and create a bullet-point summary of any grammar errors or tips for improving the choice of words.'

# keep a record of the conversation
messages = [{"role": "system", "content": content}]

# tokens
tokens = []


def voice_gpt_conversation(audio):
    start = time.time()
    
    print("starting conversation round")
    # get transcription from small model setting to spanish
    transcription = model.transcribe(audio, task = "transcribe", language = "es", fp16 = False, beam_size = 5)['text']
    print(f"finished decoding. {time.time() - start}")
    print(transcription)

    # add the user text to the messages list
    messages.append({"role": "user", "content": transcription})

    print(f"calling to gpt. {time.time() - start}")
    
    # now we make the call to gpt3.5 and get the response
    response = openai.ChatCompletion.create(model = "gpt-3.5-turbo", messages = messages)

    print(f"finished call to gpt. {time.time() - start}")

    # add the response to the messages list
    system_message = response["choices"][0]["message"]
    messages.append(system_message)

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(system_message['content'])
    engine.runAndWait()

    # add the total tokens to the tokens list
    tokens.append(int(response['usage']['total_tokens']))

    print(tokens, sum(tokens))

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    return chat_transcript


audio_input = gr.Audio(source = "microphone", type = "filepath")
output = gr.outputs.Textbox()


gr.Interface(fn = voice_gpt_conversation, inputs = audio_input, outputs = output, title = "Whisper My Spanish").launch()



