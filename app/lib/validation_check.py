import openai
from pathlib import Path
import os, json, dotenv
import re

env_path = Path('.') / '.env'
if env_path.exists():
    dotenv.load_dotenv(dotenv_path=env_path)

MY_KEY = os.getenv("MY_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def remove_zero_width_spaces(text):
    """
    Remove all zero width spaces (\u200b) from the given text.
    
    Parameters:
    - text: The input string from which zero width spaces should be removed.
    
    Returns:
    - A string with all zero width spaces removed.
    """
    # Define the zero width space Unicode character
    zero_width_space = '\u200b'
    # Use regular expression to replace zero width spaces with nothing
    cleaned_text = re.sub(zero_width_space, '', text)
    
    return cleaned_text

def response_format(answer):
    """
    Formats a string response by removing specific characters and converting to JSON.
    
    Args:
        answer (str): The response string to format.
    
    Returns:
        dict or None: The formatted response as a JSON object, or None if conversion fails.
    """
    try:
        return json.loads(answer.replace('```', '').replace('json', ''))
    except:
        return None

def check_openai_api_key(input_api_key):
    """
    Validates an input API key against the stored API key or attempts to use it with OpenAI.
    
    Args:
        input_api_key (str): The API key to validate.
    
    Returns:
        str or None: The valid API key if the key is correct or None if validation fails.
    """
    input_api_key = remove_zero_width_spaces(input_api_key)
    if MY_KEY and input_api_key == MY_KEY:
        api_key = OPENAI_API_KEY
    else:
        api_key = input_api_key

    try:
        # Attempt to use the API key to list OpenAI models as a validation step
        openai.OpenAI(api_key=api_key).models.list()
        return api_key  # Return the valid API key
    except openai.AuthenticationError:
        return None  # Authentication with OpenAI failed
    except openai.APIConnectionError:
        return None  # Connection to OpenAI API failed
    except UnicodeEncodeError:
        return None  # Issue with encoding the API key
