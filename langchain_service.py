from typing import Callable, Dict, List, Optional, Union
from langchain.agents import load_tools, initialize_agent
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import LLMChain, ConversationChain
from langchain.chains.conversation.memory import (ConversationBufferMemory,
                                                  ConversationSummaryMemory,
                                                  ConversationBufferWindowMemory,
                                                  ConversationKGMemory)
from langchain.callbacks import get_openai_callback
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
import pinecone


class LangChainService:
    def __init__(self, openai_api_key, pinecone_api_key, pinecone_api_env):

        self.openai_api_key: str = openai_api_key
        self.pinecone_api_key: str = pinecone_api_key
        self.pinecone_api_env: str = pinecone_api_env

        self.llm: ChatOpenAI = ChatOpenAI(
            temperature=0, openai_api_key=self.openai_api_key)

        self.conversation_buf: ConversationChain = ConversationChain(
            llm=self.llm,
            memory=ConversationBufferMemory()
        )

    def _count_tokens(self, chain: Union[LLMChain, ConversationChain], query: str) -> str:
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

        response_function: Optional[Callable[[str],
                                             str]] = response_functions.get(type)

        if response_function is None:
            return "Error ChatBot Type is invalid"

        return response_function(message)

    def get_bot_response_serapi(self, message: str) -> str:
        tool_names: List[str] = ["serpapi"]
        tools = load_tools(tool_names)

        agent = initialize_agent(
            tools, self.llm, agent="zero-shot-react-description", verbose=True)

        response: str = agent.run(message)

        return response

    def get_bot_response_chat_prompt_template(self, message: str) -> str:
        prompt_template = PromptTemplate(
            input_variables=["query"],
            template=template
        )

        openai = OpenAI(
            model_name="text-davinci-003",
            openai_api_key=self.openai_api_key
        )

        reply: str = openai(prompt_template.format(query=message))
        return reply

    def get_bot_response_google_wolfram(self, message):

        tool_names = ["serpapi", "wolfram-alpha"]
        tools = load_tools(tool_names)

        agent = initialize_agent(
            tools, self.llm, agent="zero-shot-react-description", verbose=True)

        response = agent.run(message)

        return response

    def get_bot_response_chat_completions(self, message: str) -> str:
        
        chatOpenAI = ChatOpenAI(
           model_name="gpt-3.5-turbo"
        )
        
        reply: str = chatOpenAI.call_as_llm(message)

        return reply

    def get_bot_response_wolfram_alpha(self, message):

        tool_names = ["wolfram-alpha"]
        tools = load_tools(tool_names)

        agent = initialize_agent(
            tools, self.llm, agent="zero-shot-react-description", verbose=True)

        response = agent.run(message)

        return response

    def get_bot_response_field_manual(self, message):
        pinecone.init(
            api_key=self.pinecone_api_key,
            environment=self.pinecone_api_env
        )

        index_name = "fieldmanual"

        embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key)
        pine = Pinecone.from_existing_index(index_name, embeddings)

        chain = load_qa_chain(self.llm, chain_type="stuff")

        docs = pine.similarity_search(message, include_metadata=True)
        response = chain.run(input_documents=docs, question=message)
        docs = pine.similarity_search(message, include_metadata=True)
        response = chain.run(input_documents=docs, question=message)

        # If there is no matching response, provide a default response
        return response

    def get_bot_response_with_conversation_buffer_memory(self, message):
        # https://www.pinecone.io/learn/langchain-conversational-memory/

        ct = self._count_tokens(
            self.conversation_buf,
            message
        )

        return ct

    def get_bot_response_with_conversation_summary_memory(self, message):
        conversation_sum = ConversationChain(
            llm=self.llm,
            memory=ConversationSummaryMemory(llm=self.llm)
        )

        ct = self._count_tokens(
            conversation_sum,
            message
        )

        return ct

    def get_bot_response_with_conversation_buffer_window_memory(self, message):
     
        conversation_sum = ConversationChain(
            llm=self.llm,
            memory=ConversationBufferWindowMemory(k=1)
        )

        ct = self._count_tokens(
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
