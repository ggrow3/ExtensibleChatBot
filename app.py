import os

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for, jsonify)

from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
import os
import env_setter
import pinecone
import openai

app = Flask(__name__)

env_setter.setup_keys()

@app.route('/chatbot')
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

    # Process the message and generate a response
    response = get_bot_response(message, chatbotType)

    # Return the response as a JSON object
    return jsonify({'response': response})




def get_bot_response(message, type="fieldmanual"):
    # Define a dictionary that maps the type to the corresponding function
    response_functions = {
        "chatgpt4": get_bot_response_chat_completions,
        "fieldmanual": get_bot_response_field_manual,
        "canned": get_bot_response_canned
    }
    
    # Get the appropriate function based on the type argument
    response_function = response_functions.get(type)
    
    # If the type is not valid, return an empty string
    if response_function is None:
        return "Error ChatBot Type is invalid"
    
    # Call the appropriate function and return the result
    return response_function(message)

def get_bot_response_chat_completions(message):
   messages = []
   messages.append({"role":"system","content":"you are a helpful bot"})
   messages.append({"role":"user","content": message})
   openai.api_key = os.environ["OPENAI_API_KEY"]
   response=openai.ChatCompletion.create(
     model="gpt-3.5-turbo",
     messages=messages
   )
   # If there is no matching response, provide a default response
   reply = response["choices"][0]["message"]["content"]
   return reply

def get_bot_response_field_manual(message):
   pinecone.init(
        api_key=os.environ['PINECONE_API_KEY'],
        environment=os.environ['PINECONE_API_ENV']
   )

   index_name = "fieldmanual"

   embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
   pine = Pinecone.from_existing_index(index_name, embeddings)

   openAI = OpenAI(temperature=0, openai_api_key=os.environ['OPENAI_API_KEY'])

   chain = load_qa_chain(openAI, chain_type="stuff")

   docs = pine.similarity_search(message, include_metadata=True)
   response = chain.run(input_documents=docs, question=message)
 
   # If there is no matching response, provide a default response
   return response


def get_bot_response_canned(message):
    # Define simple predefined responses based on user input
    responses = {
        'hello': 'Hi there! How can I help you?',
        'how are you': 'I am doing well, thank you!',
        'goodbye': 'Goodbye! Have a great day!'
    }

    # Convert the message to lowercase and find a matching response
    response = responses.get(message.lower())

    # If there is no matching response, provide a default response
    return response or 'I am not sure how to respond to that.'


@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name')

    if name:
        print('Request for hello page received with name=%s' % name)
        return render_template('hello.html', name=name)
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
