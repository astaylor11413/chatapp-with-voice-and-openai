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
    #Set the role for the OpenAI api assistant
    #This is so it can respond within the preferred context
    prompt = "Act like a personal assistant. You can respond to questions, translate sentences, summarize news and give recommendations. Keep responses concise - 2 to 3 sentences maximum."

    #call openAI to process the prompt before interacting with user
    openai_response = openai_client.chat.completions.create(
        model = "gpt-5-nano",
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
