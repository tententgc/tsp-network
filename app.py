from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form.get('message')
        # Print received message
        print("Message received: ", message)
        return 'Message received', 200
    else:
        return 'Hello from Node!'

@app.route('/send', methods=['POST'])
def send_message():
    target = request.form.get('target')
    message = request.form.get('message')
    # Send the message
    response = requests.post(f'http://{target}', data={'message': message})
    return response.text, response.status_code

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
