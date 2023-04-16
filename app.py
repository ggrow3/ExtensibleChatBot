import os
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for, jsonify)
from flask_httpauth import HTTPBasicAuth
from chatbot_service import ChatBotService

app = Flask(__name__)
auth = HTTPBasicAuth()

# Define a dictionary to store valid usernames and passwords
users = {
    "chatbot": "grandunified",
    "user2": "password2"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@app.route('/chatbot')
@auth.login_required
def chatbot():
    print('Request for chatbot page received')
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    # Get the JSON payload from the request
    data = request.get_json()

    # Extract the message from the JSON payload
    message = data.get('message')

    chatbotType = data.get('chatBotType')

    chatbotService = ChatBotService()
    # Process the message and generate a response
    response = chatbotService.get_bot_response(message, chatbotType)

    # Return the response as a JSON object
    return jsonify({'response': response})

@app.route('/')
@auth.login_required
def index():
    print('Request for index page received')
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')



if __name__ == '__main__':
    app.run()
