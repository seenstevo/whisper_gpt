# import libraries
import gradio as gr
import threading
import time
import tensorflow as tf

# import local modules
import functions
import error_table
import transcribe
import chat_mode



# initialise chat with system prompt
messages = chat_mode.initialise_chat()

def voice_gpt_conversation(audio):
    start = time.time()
    
    print('#'*50)
    print("starting conversation round")
    ######################## TRANSCRIBE ##################################################
    # get transcription from small model setting to spanish
    transcription = transcribe.transcribe_faster_whisper(audio)
    # time the transcription process
    whisper_end_time = functions.time_stage(start, "whisper transcription")
    ##################### ERROR IDENTIFICATION ###########################################
    # using GPT to carry out error checking on user text and add rows to correction and error tables.
    thread = threading.Thread(target = error_table.error_wrapper(conversation = messages, transcription = transcription))
    # Start the thread to run in background while we continue with main chat function
    thread.start()
    ###################### APPEND USER TEXT TO MESSAGES ##################################
    # add the user text to the messages list
    messages.append({"role": "user", "content": transcription})
    ################### CALL GPT CHAT ####################################################
    # now we make the call to GPT conversation partner or create the summary of conversation
    if transcription.lower().replace('.','').strip() == "hemos terminado":
        response = chat_mode.get_conversation_summary(messages)
    else:
        response = chat_mode.get_chat_response(messages)
    # time taken to get GPT response
    _ = functions.time_stage(whisper_end_time, "GPT response")
    #################### APPEND GPT RESPONSE TO MESSAGES #################################
    # add the response to the messages list
    messages.append(response)
    #################### VOICE SYNTHESIS GPT RESPONSE ####################################
    functions.speak(response["content"])
    #################### PRINT CONVERSATION TO SCREEN ####################################
    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"
    # time full round
    _ = functions.time_stage(start, "end conversation round")
    
    return chat_transcript


audio_input = gr.Audio(source = "microphone", type = "filepath")
output = gr.outputs.Textbox()


interface = gr.Interface(fn = voice_gpt_conversation, inputs = audio_input, outputs = output, title = "Whisper My Spanish")

interface.launch()



