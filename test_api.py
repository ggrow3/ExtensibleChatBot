
from chatbot_service import ChatBotService

# Define a function that calls the get_bot_response function and prints the result

def call_get_bot_response(message, type=""):
    chatBotService = ChatBotService()
    response = chatBotService.chat_with_langchain(message, type)(message, type)
    print(response)

# Call the function with some example messages
call_get_bot_response('hello', 'canned')
call_get_bot_response('what branch of the army is the field manual for?', 'fieldmanual')
call_get_bot_response('goodbye','fieldmanual')
call_get_bot_response('what is the athenosphere','wolfram')
call_get_bot_response('unknown message')

call_get_bot_response("are you a field manual?",'chatgpt4')

call_get_bot_response("how many points is lebron james averaging?",'serpapi')


