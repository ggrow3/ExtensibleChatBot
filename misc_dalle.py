import os
import openai
from env_setter import ChatBotSettings

i = ChatBotSettings()
# Your API Key Here: 👇
openai.api_key = i.OPENAI_API_KEY
# Your Image Prompt Here: 👇
prompt = "A Chat bot floating in the clouds"
response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="256x256",
)
print(response["data"][0]["url"])