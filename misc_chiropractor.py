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
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationKGMemory
from pandasai import PandasAI

import pandas as pd
from difflib import get_close_matches

questions = [
    "How are you doing overall?",
    "Does anyting hurt?",
    "What is your level of pain? (1-5)",
    "Do you have any other symptoms?"
 
]

template = """The following is a conversation between a AI chiropractor and a human patient. The AI Chiropractor has an excellent bedside manner provides specific details from its context. 
If the AI does not know the answer to a question, it truthfully says it does not know. The AI ONLY uses information contained in the "Relevant Information" section and does not hallucinate.
{history}

Conversation:
Human: {input}
    
"""
prompt = PromptTemplate(
        input_variables=["history", "input"], template=template
)

llm = ChatOpenAI(
            temperature=0,
            openai_api_key=ChatBotSettings().OPENAI_API_KEY(),
            model_name="gpt-3.5-turbo"
)

conversation_with_kg = ConversationChain(
        llm=llm, 
        verbose=True, 
        prompt=prompt,
        memory=ConversationKGMemory(llm=llm)
)


patients = [{"name": "John Doe"}]  # List of patients

#patients = [{"name": "John Doe"}, {"name": "Jane Doe"}, {"name":"Steve Smith"}]  # List of patients
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




    # conversation_with_kg.predict(input="Hi, what's up?")

    # conversation_with_kg.predict(input="My name is James and I'm helping Will. He's an engineer.He loves ice cream")


    # conversation_with_kg.predict(input="What do you know about Will?")

    # Open-ended questions
    while True:
        question = input("What do you want to ask? (type 'done' when you are finished) ")
        if question.lower() == 'done':
            break
        messages = [
            SystemMessage(content="You are an adventure mystery cartoon story telling bot."),
            HumanMessage(content="Hi AI, what are your main themes?"),
            AIMessage(content="My theme and things is doing good and solve puzzles and learn about science in the world."),
            HumanMessage(content="I'd like to have you tell me an adventure story with Colin and Ian as my characters.Santorini is a bad guy in the story and so are pollution and externalities caused by man. Tell about regreening earth")
        ]
     
        patient_responses["responses"][question] = conversation_with_kg(question)
        print(patient_responses["responses"][question]["response"])

        patient_responses["questions"].append(question)

    responses.append(patient_responses)




# Original data
data = [{'name': 'John Doe', 'date': '2023-05-13', 'responses': {'How are you doing overall?': 'Good', 'Does anyting hurt?': 'No', 'What is your level of pain? (1-5)': '4', 'Do you have any other symptoms?': 'Legs'}, 'questions': []}]

# Knowledge base
knowledge_base = ['How do you feel overall?', 'Is there any pain?', 'Rate your pain from 1-5', 'Any other symptoms?']

# Flatten the dictionary inside the 'responses' key and match questions to knowledge base
flattened_data = []
for item in data:
    flattened_dict = {}
    flattened_dict['name'] = item['name']
    flattened_dict['date'] = item['date']
    responses = item['responses']
    for question, response in responses.items():
        # Find closest match in knowledge base for the question
        match = get_close_matches(question, knowledge_base, n=1)
        if match:
            # If a match is found, add the match as a new entry in the dictionary
            flattened_dict['matched_question'] = match[0]
        flattened_dict[question] = response
    flattened_data.append(flattened_dict)

# Create DataFrame
df = pd.DataFrame(flattened_data)

from pandasai.llm.openai import OpenAI
llm = OpenAI()

while True:
    pandas_ai = PandasAI(llm, conversational=False)
    user_input = input("What data do you want? ")
    response = pandas_ai.run(df, prompt=user_input)
    print(response)


