import pandas as pd
import json
import openai
import csv

from functions import read_config

# load in the openai api key
config = read_config('config.ini')
api_key = config.get('openai', 'api_key')
openai.api_key = api_key



error_check_system_prompt = '''\
Eres un experto en español que deberá "Corregir e Identificar" errores en un texto de un no nativo. \
Para corregir los errores, primero generarás una versión corregida del texto. Considerarás el contexto del texto al hacer esta versión corregida. \
Después del texto corregido, utilizarás esta versión corregida para crear una tabla. La tabla tendrá tres columnas: Errores, Correcciónes, Etiquetas. \
Asegúrate de que la "Corrección" mantenga el mismo significado que el "Error". \
Clasifica el tipo de error y despues utiliza la etiqueta más apropiada de esta lista: \
['ser/estar', 'tiempo_verbal', 'subjuntivo', 'preposición', 'concordancia_de_género', 'adverbio', 'artículo', 'orden_de_palabras', \
'elección_de_palabras', 'lo/el/la_que', 'pronombre_directo/indirecto', pretérito_imperfecto_del_subjuntivo, 'otro']\
'''

def error_wrapper(conversation, transcription):
    '''
    Wrap the call to the functions to retrieve errors from GPT and save these to files
    '''
    error_check_response = error_check(conversation, transcription)
    error_tables(error_check_response, transcription)
    

def error_check(conversation, transcription):
    '''
    Here we pass previous user and assistant interactions (context) plus the latest text (transcription) wrapped in an instruction to identify errors.
    '''
    messages = [{"role": "system", "content": error_check_system_prompt}]
    # logic to ensure we only select most recent interactions (if they exist) for giving context to error identification
    if len(conversation) > 2:
        context = conversation[-2:]
        messages.append(context[0])
        messages.append(context[1])
        
    messages.append({"role": "user", "content": f"Corrige e identifica los errores del siguiente texto: ```{transcription}```. \
    Responde en formato JSON con las claves 'Correction' y 'Table' y nunca da más texto fuera del JSON"})

    response = openai.ChatCompletion.create(model = "gpt-3.5-turbo", messages = messages, temperature = 0, max_tokens = 1000)
    return response["choices"][0]["message"]['content']


def error_tables(error_check_response, transcription):
    '''
    We pass the error_check response to log two types of data in two tables.
    The first is the pair of student text and the teacher correction/improvement.
    The second are the rows of Error, Correction and Tag. 
    '''
    start_index = error_check_response.find('{')
    end_index = error_check_response.rfind('}') + 1

    if start_index != -1 and end_index != -1:
        json_str = error_check_response[start_index:end_index]
        error_dict = json.loads(json_str)
    
    # add the imrpoved/corrected full sentences to table
    student_teacher_row = pd.DataFrame({'Student': [transcription], 'Teacher': [error_dict['Correction']]}).values.tolist()
    add_rows('/home/sean/Documentos/AI_projects/whisper_gpt/tables/student_teacher.csv', student_teacher_row)
    # add the specific error table rows to error table
    error_rows = pd.DataFrame(error_dict['Table']).values.tolist()
    add_rows('/home/sean/Documentos/AI_projects/whisper_gpt/tables/errors.csv', error_rows)
    
    
def add_rows(old_table: str, new_rows: list):
    '''
    Helper to simply write the latest errors to existing files
    '''
    with open(old_table, 'a', newline = '') as file:
        writer = csv.writer(file)
        writer.writerows(new_rows)
