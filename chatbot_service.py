from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
import os
import env_setter
import pinecone
import openai
import env_setter
from langchain.agents import load_tools


class ChatBotService:
    def __init__(self):
        env_setter.setup_keys()

        self.openai_api_key = os.environ["OPENAI_API_KEY"]
        self.pinecone_api_key = os.environ["PINECONE_API_KEY"]
        self.pinecone_api_env = os.environ["PINECONE_API_ENV"]

    def get_bot_response(self, message, type="fieldmanual"):
        # Define a dictionary that maps the type to the corresponding function
        response_functions = {
            "chatgpt4": self.get_bot_response_chat_completions,
            "fieldmanual": self.get_bot_response_field_manual,
            "canned": self.get_bot_response_canned,
            "wolfram": self.get_bot_response_wolfram_alpha,
            "serpapi": self.get_bot_response_serapi
        }
        
        # Get the appropriate function based on the type argument
        response_function = response_functions.get(type)
        
        # If the type is not valid, return an empty string
        if response_function is None:
            return "Error ChatBot Type is invalid"
        
        # Call the appropriate function and return the result
        return response_function(message)
    
    def get_bot_response_serapi(self, message):
        llm = OpenAI(temperature=0)

        tool_names = ["serpapi"]
        tools = load_tools(tool_names)

        agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

        response = agent.run(message)

        return response
     
    def get_bot_response_chat_completions(self, message):
        messages = []
        messages.append({"role":"system","content":"you are a helpful bot"})
        messages.append({"role":"user","content": message})
        openai.api_key = self.openai_api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        # If there is no matching response, provide a default response
        reply = response["choices"][0]["message"]["content"]
        return reply
    
    def get_bot_response_wolfram_alpha(self, message):
        llm = OpenAI(temperature=0)
        tool_names = ["wolfram-alpha"]
        tools = load_tools(tool_names)
        
        agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

        response = agent.run(message)

        return response

    def get_bot_response_field_manual(self, message):
        pinecone.init(
            api_key=self.pinecone_api_key,
            environment=self.pinecone_api_env
        )

        index_name = "fieldmanual"

        embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key )
        pine = Pinecone.from_existing_index(index_name, embeddings)

        openAI = OpenAI(temperature=0, openai_api_key=self.openai_api_key )

        chain = load_qa_chain(openAI, chain_type="stuff")

        docs = pine.similarity_search(message, include_metadata=True)
        response = chain.run(input_documents=docs, question=message)
        docs = pine.similarity_search(message, include_metadata=True)
        response = chain.run(input_documents=docs, question=message)
        
        # If there is no matching response, provide a default response
        return response

    def get_bot_response_canned(self, message):
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



