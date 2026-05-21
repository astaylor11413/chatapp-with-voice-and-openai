from openai import OpenAI
import requests

openai_client = OpenAI()


def speech_to_text(audio_binary):
    #define the data needed to be sent for the http POST request
    #POST is for sending/processing data
    #requires api URL, Paramaters, Body

    #define the api URL being used
    base_url = "https://sn-watson-stt.labs.skills.network"
    api_url = base_url+'/speech-to-text/api/v1/recognize'

    #define the model you want to use to process speech
    params = {
        'model':'en-US_Multimedia',
    }

    #define the body/data which is the audio being processed
    body = audio_binary

    #Send http request with all defined variables and save response
    response = requests.post(api_url,params=params,data=body).json()

    #parse the json response to retrieve assistant text
    while bool(response.get('reults')):
        print('speech to text response:', response)
		text = response.get('results')
                        .pop()
                        .get('alternatives')
                        .pop()
                        .get('transcript')
		print('recognised text: ', text)
		return text


def text_to_speech(text, voice=""):
    return none



def openai_process_message(user_message):
    return none
