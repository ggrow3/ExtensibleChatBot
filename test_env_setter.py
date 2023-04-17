import os

def setup_keys():
    os.environ["PINECONE_API_KEY"] = ''
    os.environ["PINECONE_API_ENV"] = ''
    os.environ["OPENAI_API_KEY"] = ""
    os.environ["WOLFRAM_ALPHA_APPID"] = ""
    os.environ["SERPAPI_API_KEY"] = ""