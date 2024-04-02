"""
basically what this file does:

1. given an image_path, it first goes through astica_description() and we are returned a description ( i edited the code to alter the
   type/lenght of description)
2. then it goes into fitering_out_stop_words() where stop words and adjectives are removed
        --> in this i added a list clothes and clothes in description. so basically its taking the list that has all the stop words
           removed and seeing if it mentions any specfic article of clothing. then after it adds it to the final returned list.
           this is because after i run the code that filters out adjectives it SOMETIMES removes the type of clothing item
       --> so i am adding this in after just so when we do the sim score we are also checking if we are comparing
           [black, shiney, skirt] and not just [ black , shiney]
3. then it goes into the synonym_extractor() and we are returned a dictionary w all the synomym with the key words


so to do simularity_score() in graph.py:
- we need to call steps 1-3 on the users uploaded image
- we need to call step 2 on the zara description
- then we gonna go through each list and see if there any similar words, and if there is then the score goes up by one
- i was thinking to make the score out of 15? ( in the astica code i made it that the description gives max 15 words)
"""
import requests
import json
import base64
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


# nltk.download('averaged_perceptron_tagger')


def get_image_base64_encoding(image_path: str) -> str:
    """
    #Function to return the base64 string representation of an image
    *Part of API
    """
    with open(image_path, 'rb') as file:
        image_data = file.read()
    image_extension = os.path.splitext(image_path)[1]
    base64_encoded = base64.b64encode(image_data).decode('utf-8')
    return f"data:image/{image_extension[1:]};base64,{base64_encoded}"


def asticaAPI(endpoint, payload, timeout):
    """*Part of API"""
    response = requests.post(endpoint, data=json.dumps(payload), timeout=timeout,
                                headers={'Content-Type': 'application/json', })
    if response.status_code == 200:
        return response.json()
    else:
        return {'status': 'error', 'error': 'Failed to connect to the API.'}


def astica_description(filelocation: str):
    """*Part of API
    Given an image and prompt, API creates a description. """
    # API configurations
    asticaAPI_key = '0F432E35-599B-4DC3-AEB7-A6FF2B4E96A0274078E18C7F0C-3476-405E-92BB-0A2FC41C441B'
    asticaAPI_timeout = 25  # in seconds. "gpt" or "gpt_detailed" require increased timeouts
    asticaAPI_endpoint = 'https://vision.astica.ai/describe'
    asticaAPI_modelVersion = '2.1_full'

    asticaAPI_input = get_image_base64_encoding(filelocation)  # use base64 image input (slower)

    asticaAPI_visionParams = 'gpt_detailed,describe,color,categories'  # comma separated, defaults to "all".
    asticaAPI_gpt_prompt = 'write a detailed description of the clothing item including fabric, style, color, and cut. Do not mention background and person'  # only used if visionParams includes "gpt" or "gpt_detailed"
    asticaAPI_prompt_length = '25'  # number of words in GPT response

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

    return astica_description(filelocation)

"""fiter = filter_out_all('blazer.png')
print(fiter)
s = synonym_extractor(fiter)
print(s)"""
