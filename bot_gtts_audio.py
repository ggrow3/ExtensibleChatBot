from abc import ABC, abstractmethod
from typing import Any
from gtts import gTTS


class BotGtts(ABC):
   
    def __init__(self, settings: Any):
        pass


    def get_bot_response(self, text: str) -> str:
        language = 'en'
        
        # # Passing the text and language to the engine, 
        # # here we have marked slow=False. Which tells 
        # # the module that the converted audio should 
        # # have a high speed
        myobj = gTTS(text=text, lang=language, slow=False)

        return myobj


