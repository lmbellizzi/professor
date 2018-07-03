import os
import requests
import traceback
import json
from flask import Flask, request
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

#token = os.getenv('FB_ACCESS_TOKEN')
token = os.environ['FB_ACCESS_TOKEN']
#verify_token = os.getenv('FB_VERIFY_TOKEN')
verify_token = os.environ['FB_VERIFY_TOKEN']
app = Flask(__name__)


# Sends response messages via the Send API
def sendHello(sender_psid):
    return {"recipient": {"id": sender_psid},"message": {"text": "Hello World!"}}
    

@app.route('/', methods=['POST', 'GET'])
def webhook():
    if request.method == 'POST':
        try:
            data = json.loads(request.data.decode())
            text = data['entry'][0]['messaging'][0]['message']['text']
            print(text)
            sender = data['entry'][0]['messaging'][0]['sender']['id']
            print(sender)
            payload = sendHello(sender)
            print(payload)
            try:
                r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload)
            except Exception as e:
                print(e)
            return 'ok'
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            return 'Something wrong'
    elif request.method == 'GET':
        if request.args.get('hub.verify_token') == verify_token:
            return request.args.get('hub.challenge')
        return 'Wrong Verify Token'
    return None

if __name__ == '__main__':
    app.run(debug=True)