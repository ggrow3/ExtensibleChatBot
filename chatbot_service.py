from knowledge_base_service import KnowledgeBaseService
from langchain_service import LangChainService
from typing import Callable, Dict, List, Optional, Union
import os
import env_setter
import json
from typing import Dict, Tuple, List
import env_setter


class ChatBotService:
    def __init__(self, langchain_service: LangChainService, knowledge_base_service: KnowledgeBaseService) -> None:
        self.langchain_service: LangChainService = langchain_service
        self.knowledge_base_service: KnowledgeBaseService = knowledge_base_service

    def chat_with_langchain(self, message: str, type: str) -> Union[str, Dict[str, str]]:
        return self.langchain_service.get_bot_response(message, type)

    def chat_with_knowledge_base(self, knowledge_base_file: str) -> None:
        self.knowledge_base_service.chat_with_knowledge_base(knowledge_base_file)







