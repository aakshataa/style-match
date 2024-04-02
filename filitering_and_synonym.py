import requests
import json
import base64
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def get_image_base64_encoding(image_path: str) -> str:
    """ Function to return the base64 string representation of an image - Given by our ASTICA API
    """
    with open(image_path, 'rb') as file: 
        image_data = file.read()
    image_extension = os.path.splitext(image_path)[1]
    base64_encoded = base64.b64encode(image_data).decode('utf-8')
    return f"data:image/{image_extension[1:]};base64,{base64_encoded}"


def asticaAPI(endpoint:str, payload:Any, timeout:float) -> dict:
    """ The function sends a POST request to the specified endpoint, including the provided payload, with a specified timeout. 
    It expects a response with a status code of 200 (meaning success). If the response status code is 200, it returns the response
    data in JSON format. If the response status code is not 200, it returns a JSON object indicating an error occurred - Given by our ASTICA API"""
    response = requests.post(endpoint, data=json.dumps(payload), timeout=timeout,
                                headers={'Content-Type': 'application/json', })
    if response.status_code == 200:
        return response.json()
    else:
        return {'status': 'error', 'error': 'Failed to connect to the API.'}


def astica_description(filelocation: str) -> str:
    """ Given an image, our ASTICA API uses computer visison to create a description of it. The code was originally given by our ASTICA API but we modified it

    Preconditions:
    - filelocation should be a valid path linking to users directory
    
    """
    # API configurations
    asticaAPI_key = '0F432E35-599B-4DC3-AEB7-A6FF2B4E96A0274078E18C7F0C-3476-405E-92BB-0A2FC41C441B' # We had to get this key off of ASTICA - these keys are used identify and authenticate an app/user. 
    asticaAPI_timeout = 25  # in seconds. "gpt" or "gpt_detailed" require increased timeouts
    asticaAPI_endpoint = 'https://vision.astica.ai/describe'
    asticaAPI_modelVersion = '2.1_full'

    asticaAPI_input = get_image_base64_encoding(filelocation)  # use base64 image input (slower)

    asticaAPI_visionParams = 'gpt_detailed,describe,color,categories'  # comma separated, defaults to "all".
    asticaAPI_gpt_prompt = 'write a detailed description of the clothing item including fabric, style, color, and cut. Do not mention background and person'  # we can use this prompt to shape the ASTICA computer vision description

    # Define payload dictionary
    asticaAPI_payload = {
        'tkn': asticaAPI_key,
        'modelVersion': asticaAPI_modelVersion,
        'visionParams': asticaAPI_visionParams,
        'input': asticaAPI_input,
        'gpt_prompt': asticaAPI_gpt_prompt,
        'prompt_length': asticaAPI_prompt_length,
    }

    asticaAPI_result = asticaAPI(asticaAPI_endpoint, asticaAPI_payload, asticaAPI_timeout)

    if 'status' in asticaAPI_result:
        # Output Error if exists
        if asticaAPI_result['status'] == 'error':
            print('Output:\n', asticaAPI_result['error'])
        # Output Success if exists
        if asticaAPI_result['status'] == 'success':
            if 'caption_GPTS' in asticaAPI_result and asticaAPI_result['caption_GPTS'] != '':
                long_caption = asticaAPI_result['caption_GPTS']
                return long_caption

def user_image_description(filelocation: str) -> str:
   """ Returns our ASTICA description when given the file path from our directory
   
   Preconditions:
    - filelocation should be a valid path linking to users directory
   """
    return astica_description(filelocation)
