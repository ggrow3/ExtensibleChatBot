from bot_conversation_chain import BotConversationChain
from bot_knowledge_base import BotKnowledgeBase
from typing import Callable, Dict, List, Optional, Union
import os
import json
from typing import Dict, Tuple, List
from chatbot_settings import ChatBotSettings
from bot_pinecone import BotPineCone
from bot_agent_tools import BotAgentTools
from langchain import (HuggingFaceHub, Cohere)
from langchain.chat_models import ChatOpenAI
from colorama import Fore, Style, init
from bot_dalle_imagine import BotDalle
from bot_gtts_audio import BotGtts


class ChatBotFactory:
    services = {
        'BotConversationChain': BotConversationChain,
        'BotPineCone': BotPineCone,
        'BotAgentTools': BotAgentTools,
        'BotKnowledgeBase': BotKnowledgeBase,
        'BotDalle': BotDalle,
        "BotGtts": BotGtts
    }

    llms = {
        "ChatOpenAI": ChatOpenAI(
            temperature=0,
            openai_api_key=ChatBotSettings().OPENAI_API_KEY(),
            model_name="gpt-3.5-turbo"
        ),
        "Cohere": Cohere(model='command-xlarge'),
        "HuggingFaceHub": HuggingFaceHub(
            repo_id="facebook/mbart-large-50",
            model_kwargs={"temperature": 0, "max_length": 200},
            huggingfacehub_api_token=ChatBotSettings().HUGGING_FACE_API_KEY()
        )
    }

    @classmethod
    def create_service(cls, service_type, settings):
        if service_type in cls.services:
            return cls.services[service_type](settings)
        else:
            raise ValueError(f'Unknown service type {service_type}')


    @classmethod
    def select_chatbot(cls, chatbots, selection_text):
       # Print the options to the user
      
       for i, bot in enumerate(chatbots, start=1):
           print(Fore.GREEN + f"{i}. {bot}")

        # Get user input
       selection = input(Fore.GREEN + "Enter the number of your selection: ")

       selected_bot = list(chatbots)[int(selection) - 1]

       print(Fore.GREEN + f"You selected {selected_bot}")

       return selected_bot