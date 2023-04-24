# Import the ChatBotService class
import chatbot_service
import env_setter

env_setter.setup_keys()

# Create an instance of the ChatBotService class
chatbot_service = chatbot_service.ChatBotService()

# Start the command-line chatbot
print("Enter in a prompt:")

while True:
    # Get user input from the command line
    user_input = input()
    
    # If the user types 'exit', end the chatbot session
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break
    
    # Get the chatbot's response using the get_bot_response_chat_completions method
    response = chatbot_service.get_bot_response_chat_completions(user_input)
    
    # Print the chatbot's response
    print(response)
    
    

