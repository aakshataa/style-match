"""
TODO: cite source
"""

from typing import Any
import json
import base64
import os
import requests


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


def astica_api(endpoint: Any, payload: Any, timeout: Any) -> Any:
    """*Part of API"""
    response = requests.post(endpoint, data=json.dumps(payload), timeout=timeout,
                             headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        return response.json()
    else:
        return {'status': 'error', 'error': 'Failed to connect to the API.'}


def astica_description(filelocation: str) -> str | None:
    """*Part of API
    Given an image and prompt, API creates a description. """
    # API configurations
    astica_api_key = '0F432E35-599B-4DC3-AEB7-A6FF2B4E96A0274078E18C7F0C-3476-405E-92BB-0A2FC41C441B'
    astica_api_timeout = 25  # in seconds. "gpt" or "gpt_detailed" require increased timeouts
    astica_api_endpoint = 'https://vision.astica.ai/describe'
    astica_api_model_version = '2.1_full'

    astica_api_input = get_image_base64_encoding(filelocation)  # use base64 image input (slower)

    astica_api_vision_params = 'gpt_detailed,describe,color,categories'  # comma separated, defaults to "all".

    # only used if visionParams includes "gpt" or "gpt_detailed"
    astica_api_gpt_prompt = ('write a detailed description of the clothing item '
                             + 'including fabric, style, color, and type. Do not mention background and person.')
    astica_api_prompt_length = '25'  # number of words in GPT response

    # Define payload dictionary
    astica_api_payload = {
        'tkn': astica_api_key,
        'modelVersion': astica_api_model_version,
        'visionParams': astica_api_vision_params,
        'input': astica_api_input,
        'gpt_prompt': astica_api_gpt_prompt,
        'prompt_length': astica_api_prompt_length,
    }

    astica_api_result = astica_api(astica_api_endpoint, astica_api_payload, astica_api_timeout)

    if 'status' in astica_api_result:
        # Output Success if exists
        if astica_api_result['status'] == 'success':
            if 'caption_GPTS' in astica_api_result and astica_api_result['caption_GPTS'] != '':
                long_caption = astica_api_result['caption_GPTS']
                return long_caption

    return None


def user_image_description(filelocation: str) -> str:
    """
    Return a text description of the image that the given filelocation points to.

    Preconditions:
        - filelocation is a valid file path
        - filelocation points to an image file
    """

    return astica_description(filelocation)


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['requests', 'json', 'base64', 'typing', 'os'],  # the names (strs) of imported modules
        'allowed-io': ['get_image_base64_encoding'],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
