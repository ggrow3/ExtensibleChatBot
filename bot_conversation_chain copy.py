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
from langchain import OpenAI
from chatbot_settings import ChatBotSettings
import pinecone
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from bot_abstract_class import BotAbstract



class BotConversationChain(BotAbstract):
    def __init__(self, chatBotSettings: ChatBotSettings()):
        self.chatbotSettings = chatBotSettings

        self.llm = chatBotSettings.llm
        self.memory = chatBotSettings.memory
        print(self.llm)
        self.conversation_buf: ConversationChain = ConversationChain(
            llm=self.llm,
            memory=self.memory
        )

    def get_bot_response(self, text: str):
        reply = self.conversation_buf(text)
      
        return reply['response']





    
