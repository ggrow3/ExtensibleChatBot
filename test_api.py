from app import app, get_bot_response_canned, get_bot_response

# Define a function that calls the get_bot_response function and prints the result

def call_get_bot_response(message, type=""):
    response = get_bot_response(message, type)
    print(response)

# Call the function with some example messages
call_get_bot_response('hello', 'canned')
call_get_bot_response('what branch of the army is the field manual for?', 'fieldmanual')
call_get_bot_response('goodbye','fieldmanual')
call_get_bot_response('unknown message')

call_get_bot_response("are you a field manual?",'chatgpt4')


