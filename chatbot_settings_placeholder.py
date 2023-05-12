import os


class ChatBotSettings:
    def __init__(self):
        self.set_environment_variables()
        self.users = self.get_users()

    def set_environment_variables(self):
        os.environ["PINECONE_API_KEY"] = ''
        os.environ["PINECONE_API_ENV"] = ''
        os.environ["OPENAI_API_KEY"] = ""
        os.environ["WOLFRAM_ALPHA_APPID"] = ""
        os.environ["SERPAPI_API_KEY"] = ""
        os.environ["OPENAI_ORGANIZATION_ID"] = ""
        os.environ["DISCORD_BOT_TOKEN"] = "A"

    @property
    def PINECONE_API_KEY(self):
        return os.environ.get("PINECONE_API_KEY")

    @property
    def PINECONE_API_ENV(self):
        return os.environ.get("PINECONE_API_ENV")

    @property
    def OPENAI_API_KEY(self):
        return os.environ.get("OPENAI_API_KEY")

    @property
    def WOLFRAM_ALPHA_APPID(self):
        return os.environ.get("WOLFRAM_ALPHA_APPID")

    @property
    def SERPAPI_API_KEY(self):
        return os.environ.get("SERPAPI_API_KEY")

    @property
    def OPENAI_ORGANIZATION_ID(self):
        return os.environ.get("OPENAI_ORGANIZATION_ID")

    @property
    def DISCORD_BOT_TOKEN(self):
        return os.environ.get("DISCORD_BOT_TOKEN")

    @property
    def KNOWLEDGE_BASE_FILE(self):
        return "knowledge_base.knowledge_base.json"

    @classmethod
    def get_chat_open_ai(cls: Type) -> ChatOpenAI:
        chatbotSettings = cls()
        return ChatOpenAI(temperature=0, openai_api_key=chatbotSettings.OPENAI_API_KEY)

    def get_llm_models():
        openai.organization = self.OPENAI_ORGANIZATION_ID
        openai.api_key = self.OPENAI_API_KEY
        
        model_list = openai.Model.list()['data']
        print(model_list)
        model_ids = [x['id'] for x in model_list]
        model_ids.sort()
        pprint.pprint(model_ids)

    def get_users(self):
        users = {
            "chatbot": "vernalfuture",
            "user2": "anotheruser"
        }
        return users

