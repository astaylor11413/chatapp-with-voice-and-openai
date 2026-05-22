import base64
import json
from flask import Flask, render_template, request
from worker import speech_to_text, text_to_speech, openai_process_message
from flask_cors import CORS
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_route():
    print("processing speech to text")
    #retrieve voice data from user's front end post request
    audio_binary = request.data

    #process voice data into text format
    text = speech_to_text(audio_binary)

    #return response to user in json
    response = app.response_class(
        response = json.dumps({'text':text}),
        status=200,
        mimetype='application/json'
    )

    print(response)
    print(response.data)
    return response


@app.route('/process-message', methods=['POST'])
def process_prompt_route():
    #retrieve user message from request
    user_message = request.json['userMessage']

    #retrieve user's preferred voice
    voice = request.json['voice']

    #use openai processor helper function to process message
    openai_response_text = openai_process_message(user_message)

    #use text to speech helper function to translate response into audio
    #include voice preference
    openai_response_speech = text_to_speech(openai_response_text,voice)

    openai_response_speech_base64 = base64.b64encode(openai_response_speech_binary).decode('utf-8')

    #send expected json response back to front end
    response = app.response_class(
        response = json.dumps({
            "openaiResponseText": openai_response_text, 
            "openaiResponseSpeech": openai_response_speech_base64}),
        status = 200,
        mimetype = 'application/json'
    )
    print(response)
    return response


if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0')
