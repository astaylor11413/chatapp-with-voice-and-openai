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

    #set the headers for the request
    headers = {
        'Content-Type': 'audio/webm',
    }
    
    #define the model you want to use to process speech
    params = {
        'model':'en-US_Multimedia',
    }

    #define the body/data which is the audio being processed
    body = audio_binary

    #Send http request with all defined variables and save response
    response = requests.post(api_url,params=params,headers=headers,data=body).json()

    #parse the json response to retrieve assistant text
    if response.get('results'):
        text = response.get('results')[-1].get('alternatives')[-1].get('transcript')
        print('Recognized text: ', text)
        return text
		
    return "Could not understand audio"


def text_to_speech(text, voice=""):
    #define the data needed to be sent for the http POST request
    #POST is for sending/processing data
    #requires api URL, Paramaters, Body
    base_url = "https://sn-watson-tts.labs.skills.network"
    api_url = base_url + "/text-to-speech/api/v1/synthesize?output=output_text.wav"

    #if user selects a preferred voice, add a voice parameter for request
    if voice != "" and voice != "default":
        api_url += "&voice=" + voice

    #set the headers for the request
    headers = {
        'Accept': 'audio/wav',
        'Content-Type': 'application/json',
    }

    #set the body of the request
    json_data = {
        'text' : text,
    }

    #send request to TTS service and save response
    response = requests.post(api_url, headers=headers, json=json_data)
    print('TTS response:',response)
    return response.content
    
    


def openai_process_message(user_message):
    #Set the role for the OpenAI api assistant
    #This is so it can respond within the preferred context
    prompt = "Act like a personal assistant. You can respond to questions, translate sentences, summarize news and give recommendations. Keep responses concise - 2 to 3 sentences maximum."

    #call openAI to process the prompt before interacting with user
    openai_response = openai_client.chat.completions.create(
        model = "gpt-4o-mini",
        messages=[
            {"role":"system","content":prompt},
            {"role":"user","content":user_message}
        ],
        max_completion_tokens=1000
    )
    print("openai_response:",openai_response)

    #parse response to get message for prompt
    response_text = openai_response.choices[0].message.content
    return response_text
