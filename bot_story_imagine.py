from abc import ABC, abstractmethod
from typing import Any
from gtts import gTTS
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from langchain.chains import LLMChain, ConversationChain
import openai
from langchain.chat_models import ChatOpenAI
from chatbot_settings import ChatBotSettings
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

class BotStoryImagine(ABC):
   
    def __init__(self, settings: Any):
         self.llm = settings.llm
         self.memory = settings.memory
        


    def get_bot_response(self, text: str) -> str:
        language = 'en'
        
        test_llm = ChatOpenAI(
            temperature=0,
            openai_api_key=ChatBotSettings().OPENAI_API_KEY(),
            model_name="gpt-3.5-turbo"
        )

       
        messages = [
            SystemMessage(content="You are an adventure mystery cartoon story telling bot."),
            HumanMessage(content="Hi AI, what are your main themes?"),
            AIMessage(content="My theme and things is doing good and solve puzzles and learn about science in the world."),
            HumanMessage(content="I'd like to have you tell me an adventure story with Colin and Ian as my characters.Santorini is a bad guy in the story and so are pollution and externalities caused by man. Tell about regreening earth")
        ]

        reply = test_llm(messages)

        rs = reply.content

        myobj = gTTS(text=rs, lang=language, slow=False)
        myobj.save("welcome.mp3")

        response = openai.Image.create(
            prompt=text,
            n=1,
            size="256x256",
        )
        image_path = response["data"][0]["url"]
        print(image_path)
       
        self.create_pdf("Story Bot", "story.pdf", image_path, rs)
       
        return myobj
    
    def create_pdf(self, doc_title, doc_filename, image_path, doc_text):
        document = SimpleDocTemplate(doc_filename, pagesize=letter)
    
        # Container for the 'Flowable' objects
        elements = []
    
        styles = getSampleStyleSheet()

        bodytext_style = styles['BodyText']
    
        # Add title
        title = Paragraph(doc_title, styles['Title'])
        elements.append(title)
    
        # Add image
        img = Image(image_path, 200, 200)  # The numbers 200, 200 are the width and height in points
        elements.append(img)

        text = Paragraph(doc_text, styles['BodyText'])
        elements.append(text)
    

        # Generate PDF
        document.build(elements)

       



class ResponseMultiModal:

    def __init__(self, settings: Any):
        self.audio = ""
        self.pdf = ""
        self.text = ""
        self.imageurl = ""

   


    