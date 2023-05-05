from knowledge_base_service import KnowledgeBaseService
from langchain_service import LangChainService
from typing import Callable, Dict, List, Optional, Union
import os
import env_setter
import json
from typing import Dict, Tuple, List
import env_setter


class ChatBotService:
    def __init__(self, langchain_service, knowledge_base_service):
        self.langchain_service = langchain_service
        self.knowledge_base_service = knowledge_base_service

    def chat_with_langchain(self, message, type):
        return self.langchain_service.get_bot_response(message, type)

    def chat_with_knowledge_base(self, knowledge_base_file):
        self.knowledge_base_service.chat_with_knowledge_base(
            knowledge_base_file)






