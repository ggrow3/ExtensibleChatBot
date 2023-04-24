from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import LLMChain, ConversationChain
from langchain.chains.conversation.memory import (ConversationBufferMemory, 
                                                  ConversationSummaryMemory, 
                                                  ConversationBufferWindowMemory,
                                                  ConversationKGMemory)
from langchain.callbacks import get_openai_callback

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

        self.llm = OpenAI(temperature=0, openai_api_key=self.openai_api_key)

        self.conversation_buf = ConversationChain(
            llm= self.llm,
            memory=ConversationBufferMemory()
        )

     

    def count_tokens(self, chain, query):
        with get_openai_callback() as cb:
            result = chain.run(query)
            print(f'Spent a total of {cb.total_tokens} tokens')

        return result

    def get_bot_response(self, message, type="fieldmanual"):
        # Define a dictionary that maps the type to the corresponding function
        response_functions = {
            "chatgpt4": self.get_bot_response_chat_completions,
            "fieldmanual": self.get_bot_response_field_manual,
            "canned": self.get_bot_response_canned,
            "wolfram": self.get_bot_response_wolfram_alpha,
            "serpapi": self.get_bot_response_serapi,
            "conversationbuffermemory":self.get_bot_response_with_conversation_buffer_memory
        }
        
        # Get the appropriate function based on the type argument
        response_function = response_functions.get(type)
        
        # If the type is not valid, return an empty string
        if response_function is None:
            return "Error ChatBot Type is invalid"
        
        # Call the appropriate function and return the result
        return response_function(message)
    
    def get_bot_response_serapi(self, message):
     
        tool_names = ["serpapi"]
        tools = load_tools(tool_names)

        agent = initialize_agent(tools, self.llm, agent="zero-shot-react-description", verbose=True)

        response = agent.run(message)

        return response
     
    def get_bot_response_chat_completions(self, message):
        messages = []
        messages.append({"role":"system","content":"you are a helpful bot"})
        messages.append({"role":"user","content": message})
        openai.api_key = self.openai_api_key
        response = openai.ChatCompletion.create(
            #model="gpt-3.5-turbo",
            model="gpt-3.5-turbo",
            messages=messages
        )
        # If there is no matching response, provide a default response
        reply = response["choices"][0]["message"]["content"]
        return reply
    
    def get_bot_response_wolfram_alpha(self, message):
      
        tool_names = ["wolfram-alpha"]
        tools = load_tools(tool_names)
        
        agent = initialize_agent(tools, self.llm, agent="zero-shot-react-description", verbose=True)

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


        chain = load_qa_chain(self.llm, chain_type="stuff")

        docs = pine.similarity_search(message, include_metadata=True)
        response = chain.run(input_documents=docs, question=message)
        docs = pine.similarity_search(message, include_metadata=True)
        response = chain.run(input_documents=docs, question=message)
        
        # If there is no matching response, provide a default response
        return response
      
    def get_bot_response_with_conversation_buffer_memory(self, message):
        #https://www.pinecone.io/learn/langchain-conversational-memory/
        
        ct = self.count_tokens(
            self.conversation_buf, 
            message
        )

        return ct

    def get_bot_response_with_conversation_summary_memory(self, message):
        conversation_sum = ConversationChain(
            llm=self.llm, 
            memory=ConversationSummaryMemory(llm=self.llm)
        )

        ct = self.count_tokens(
            conversation_sum, 
            message
        )

        return ct

    def get_bot_response_with_conversation_buffer_window_memory(self, message):
        llm = OpenAI(temperature=0, openai_api_key=self.openai_api_key)

        conversation_sum = ConversationChain(
            llm=llm, 
            memory=ConversationBufferWindowMemory(k=1)
        )

        ct = self.count_tokens(
            conversation_sum, 
            message
        )

        return ct
   
   
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

