import os
import openai
from chatbot_settings import ChatBotSettings

i = ChatBotSettings()
# Your API Key Here: 👇
openai.api_key = ChatBotSettings().OPENAI_API_KEY()
# Your Image Prompt Here: 👇
prompt = "Factory creating chatbots building other chatbots in a factory. Don't include any text in the picture"
response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="256x256",
)
print(response["data"][0]["url"])