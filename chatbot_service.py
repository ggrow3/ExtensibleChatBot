from typing import Callable, Dict, List, Optional, Union
import os
import env_setter
import pinecone
import openai
import json
from typing import Dict, Tuple, List
from difflib import get_close_matches

from langchain.agents import load_tools, initialize_agent
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


class ChatBotService:
    def __init__(self) -> None:
        env_setter.setup_keys()

        self.openai_api_key: str = os.environ["OPENAI_API_KEY"]
        self.pinecone_api_key: str = os.environ["PINECONE_API_KEY"]
        self.pinecone_api_env: str = os.environ["PINECONE_API_ENV"]

        self.llm: OpenAI = OpenAI(temperature=0, openai_api_key=self.openai_api_key)

        self.conversation_buf: ConversationChain = ConversationChain(
            llm=self.llm,
            memory=ConversationBufferMemory()
        )

    def count_tokens(self, chain: Union[LLMChain, ConversationChain], query: str) -> str:
        with get_openai_callback() as cb:
            result: str = chain.run(query)
            print(f'Spent a total of {cb.total_tokens} tokens')

        return result

    def get_bot_response(self, message: str, type: str = "fieldmanual") -> str:
        response_functions: Dict[str, Callable[[str], str]] = {
            "chatgpt4": self.get_bot_response_chat_completions,
            "fieldmanual": self.get_bot_response_field_manual,
            "canned": self.get_bot_response_canned,
            "wolfram": self.get_bot_response_wolfram_alpha,
            "serpapi": self.get_bot_response_serapi,
            "conversationbuffermemory": self.get_bot_response_with_conversation_buffer_memory
        }

        response_function: Optional[Callable[[str], str]] = response_functions.get(type)

        if response_function is None:
            return "Error ChatBot Type is invalid"

        return response_function(message)

    def get_bot_response_serapi(self, message: str) -> str:
        tool_names: List[str] = ["serpapi"]
        tools = load_tools(tool_names)

        agent = initialize_agent(tools, self.llm, agent="zero-shot-react-description", verbose=True)

        response: str = agent.run(message)

        return response

    def get_bot_response_chat_completions(self, message: str) -> str:
        messages: List[Dict[str, str]] = []
        messages.append({"role": "system", "content": "you are a helpful bot"})
        messages.append({"role": "user", "content": message})
        openai.api_key = self.openai_api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        reply: str = response["choices"][0]["message"]["content"]
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

    def load_knowledge_base(self, file_name: str) -> List[Dict[str, str]]:
        try:
            with open(file_name, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_knowledge_base(self, file_name: str, knowledge_base: List[Dict[str, str]]) -> None:
        with open(file_name, "w") as f:
            json.dump(knowledge_base, f, indent=2)

    def ask_question(self,knowledge_base: List[Dict[str, str]], question: str, max_matches: int = 1) -> str:
        questions = [item["question"] for item in knowledge_base]
        close_matches = get_close_matches(question, questions, n=max_matches, cutoff=0.6)
        if close_matches:
            matched_question = close_matches[0]
            for item in knowledge_base:
                if item["question"] == matched_question:
                    return item["answer"]
        else:
            return "I don't know the answer to that question. Please provide the answer."

    def learn_answer(self, knowledge_base: List[Dict[str, str]], question: str, answer: str) -> None:
        knowledge_base.append({"question": question, "answer": answer})

    #can only be used with chatbot_client
    def chat_with_knowledge_base(self, knowledge_base_file: str) -> None:
        knowledge_base = self.load_knowledge_base(knowledge_base_file)

        while True:
            question = input("Ask me a question or type 'exit' to stop: ")
            if question.strip().lower() == 'exit':
                break

            answer = self.ask_question(knowledge_base, question)
            if answer.startswith("I don't know"):
                print(answer)
                new_answer = input("Answer: ")
                self.learn_answer(knowledge_base, question, new_answer)
                self.save_knowledge_base(knowledge_base_file, knowledge_base)
            else:
                print("Answer:", answer)

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