from langchain.memory import ConversationKGMemory
from langchain.llms import OpenAI
from chatbot_settings import ChatBotSettings

i = ChatBotSettings()
llm = OpenAI(temperature=0)
memory = ConversationKGMemory(llm=llm)
memory.save_context({"input": "say hi to sam"}, {"ouput": "who is sam"})
memory.save_context({"input": "sam is a friend"}, {"ouput": "okay"})
memory.load_memory_variables({"input": 'who is sam'})


memory = ConversationKGMemory(llm=llm, return_messages=True)
memory.save_context({"input": "say hi to sam"}, {"ouput": "who is sam"})
memory.save_context({"input": "sam is a friend"}, {"ouput": "okay"})
memory.load_memory_variables({"input": 'who is sam'})

memory.get_current_entities("what's Sams favorite color?")

memory.get_knowledge_triplets("her favorite color is red")


llm = OpenAI(temperature=0)
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain

template = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. 
If the AI does not know the answer to a question, it truthfully says it does not know. The AI ONLY uses information contained in the "Relevant Information" section and does not hallucinate.

Relevant Information:

{history}

Conversation:
Human: {input}
AI:"""
prompt = PromptTemplate(
    input_variables=["history", "input"], template=template
)
conversation_with_kg = ConversationChain(
    llm=llm, 
    verbose=True, 
    prompt=prompt,
    memory=ConversationKGMemory(llm=llm)
)
conversation_with_kg.predict(input="Hi, what's up?")



llm = OpenAI(temperature=0)
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain

template = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. 
If the AI does not know the answer to a question, it truthfully says it does not know. The AI ONLY uses information contained in the "Relevant Information" section and does not hallucinate.

Relevant Information:

{history}

Conversation:
Human: {input}
AI:"""
prompt = PromptTemplate(
    input_variables=["history", "input"], template=template
)
conversation_with_kg = ConversationChain(
    llm=llm, 
    verbose=True, 
    prompt=prompt,
    memory=ConversationKGMemory(llm=llm)
)
conversation_with_kg.predict(input="Hi, what's up?")


conversation_with_kg.predict(input="My name is James and I'm helping Will. He's an engineer.")


conversation_with_kg.predict(input="What do you know about Will?")