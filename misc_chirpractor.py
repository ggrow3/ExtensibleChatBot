import json
import datetime
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


questions = [
    "How are you doing overall?",
    "Does anyting hurt?",
    "What is your level of pain? (1-5)",
    "Do you have any other symptoms?"
 
]



patients = [{"name": "John Doe"}, {"name": "Jane Doe"}]  # List of patients
responses = []

for patient in patients:
    patient_responses = {
        "name": patient["name"],
        "date": str(datetime.date.today()),
        "responses": {},
        "questions": []
    }

    # Predefined questions
    for question in questions:
        answer = input(question + " ")
        patient_responses["responses"][question] = answer

    test_llm = ChatOpenAI(
            temperature=0,
            openai_api_key=ChatBotSettings().OPENAI_API_KEY(),
            model_name="gpt-3.5-turbo"
    )

    self.conversation_buf: ConversationChain = ConversationChain(
            llm=stest_llm,
            memory=ConversationBufferMemory()
    )

    # Open-ended questions
    while True:
        question = input("What do you want to ask? (type 'done' when you are finished) ")
        if question.lower() == 'done':
            break
        messages = [
            SystemMessage(content="You are patient seeking help from a chiropractor.")
        ]
        messages.append(HumanMessage(content=question))
        patient_responses["responses"][question] = test_llm(messages)
        print(patient_responses["responses"][question])

        patient_responses["questions"].append(question)

    responses.append(patient_responses)

# # Save the responses in a separate JSON file
# with open('responses.json', 'w') as file:
#     json.dump(responses, file)
print(responses)

v = input("the end")


