from chatbot_service import ChatBotService
from knowledge_base_service import KnowledgeBaseService
from langchain_service import LangChainService
import env_setter
import os

#set up keys
env_setter.setup_keys()

#Initialize services
langchain_service = LangChainService(
    os.environ["OPENAI_API_KEY"],  os.environ["PINECONE_API_KEY"],  os.environ["PINECONE_API_ENV"])
knowledge_base_service = KnowledgeBaseService()

# Initialize chatbot service with its services and instantiate 
chatbot_service = ChatBotService(langchain_service, knowledge_base_service)

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
    response = chatbot_service.chat_with_langchain(user_input, "chatgpt4")
    
    # Print the chatbot's response
    print(response)
    
#Access the other chatbot service
#response_knowledge = chatbot_service.chat_with_knowledge_base("knowledge_base.knowledge_base.json")  

