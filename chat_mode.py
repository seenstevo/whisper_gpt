import openai

import functions


# load in the openai api key
config = functions.read_config('config.ini')
api_key = config.get('openai', 'api_key')
openai.api_key = api_key

def initialise_chat():
    convo_system_prompt = '''\
    Eres un compañero de conversación de España para una persona no nativa de habla hispana que desea practicar su conversación. \
    ¡Estás entusiasmado, animado y divertido, y usas un tono informal! \
    Sabes mucho sobre el mundo, la cultura y la historia española y latinoamericana, y has viajado mucho. \
    El estudiante a menudo cometerá errores al usar palabras incorrectas, por lo que intentarás inferir lo que el estudiante quiso decir. \
    Tu trabajo es ser parlanchín, hacer preguntas y mostrar interés en lo que dicen, y mantener la conversación en marcha.\
    '''
    return [{"role": "system", "content": convo_system_prompt}]


def get_chat_response(messages):
    '''
    This is the general purpose chat 
    '''
    response = openai.ChatCompletion.create(model = "gpt-3.5-turbo", messages = messages, max_tokens = 500)
    return response["choices"][0]["message"]


def get_conversation_summary(messages):
    summary_instruction = '''\
    Ahora analizarás la conversación anterior y destacarás algunos de los errores cometidos, dando ejemplos concretos y cómo puedes mejorarlos. \
    Sé muy específico citando ejemplos concretos, evita dar consejos vagos y sugiere cómo yo podría haber dicho mejor.\
    '''
    messages.append({"role": "user", "content": summary_instruction})
    
    response = openai.ChatCompletion.create(model = "gpt-3.5-turbo", messages = messages, max_tokens = 500)
    return response["choices"][0]["message"]