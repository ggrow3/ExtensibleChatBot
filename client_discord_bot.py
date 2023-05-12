# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord
from discord.ext import commands
import os
from env_setter import ChatBotSettings
import chatbot_service
from discord import app_commands
import discord
import asyncio
import json
from langchain_service import LangChainService
from knowledge_base_service import KnowledgeBaseService


# https://cloud.google.com/blog/topics/developers-practitioners/build-and-run-discord-bot-top-google-cloud
# https://medium.com/sltc-sean-learns-to-code/hosting-a-discord-bot-on-google-cloud-ca0dea5df988
# GETS THE CLIENT OBJECT FROM DISCORD.PY. CLIENT IS SYNONYMOUS WITH BOT.


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

# https://www.youtube.com/watch?v=jh1CtQW4DTo
# EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.


@bot.event
async def on_ready():
	try:
		synced = await bot.tree.sync()
		print(f"Synced {len(synced)} command")
	except Exception as e:
		print(e)

	# CREATES A COUNTER TO KEEP TRACK OF HOW MANY GUILDS / SERVERS THE BOT IS CONNECTED TO.
	guild_count = 0

	# LOOPS THROUGH ALL THE GUILD / SERVERS THAT THE BOT IS ASSOCIATED WITH.
	for guild in bot.guilds:
		# await tree.sync(guild=discord.Object(id=guild.id))
		# PRINT THE SERVER'S ID AND NAME.
		print(f"- {guild.id} (name: {guild.name})")

		# INCREMENTS THE GUILD COUNTER.
		guild_count = guild_count + 1

	# PRINTS HOW MANY GUILDS / SERVERS THE BOT IS IN.
	print("SampleDiscordBot is in " + str(guild_count) + " guilds.")


@bot.tree.command(name="hello", description="says hello")
async def hello(interaction: discord.Interaction):
	await interaction.response.send_message("hello")


@bot.command()
async def test(ctx, *args):
    arguments = ', '.join(args)
    await ctx.send(f'{len(args)} arguments: {arguments}')

def load_conversations():
    try:
        with open("conversations.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_conversations(conversations):
    with open("conversations.json", "w") as file:
        json.dump(conversations, file, indent=4)

@bot.command()
async def show_conversation(ctx):
    conversations = load_conversations()
    channel_id = str(ctx.channel.id)

    if channel_id in conversations:
        conversation_text = ""
        for message_data in conversations[channel_id]:
            message_text = f"<@{message_data['author_id']}>: {message_data['content']}"
            if "reactions" in message_data:
                reactions_text = " | Reactions: "
                for emoji, users in message_data["reactions"].items():
                    reactions_text += f"{emoji} ({len(users)}) "
                message_text += reactions_text
            conversation_text += message_text + "\n"
        await ctx.send(f"Conversation in this channel:\n\n{conversation_text}")
    else:
        await ctx.send("No conversation history in this channel.")


@bot.event
async def on_raw_reaction_add(payload):
    # Ignore reactions from the bot itself
    if payload.user_id == bot.user.id:
        return

    # Load conversations
    conversations = load_conversations()

    # Store reactions in the conversations dictionary
    channel_id = str(payload.channel_id)
    message_id = payload.message_id
    emoji = str(payload.emoji)
    user_id = payload.user_id

    if channel_id not in conversations:
        conversations[channel_id] = [{"message_id": message_id, "reactions": {emoji: [user_id]}}]
    else:
        for message_data in conversations[channel_id]:
            if message_data.get("message_id") == message_id:
                if "reactions" not in message_data:
                    message_data["reactions"] = {emoji: [user_id]}
                elif emoji not in message_data["reactions"]:
                    message_data["reactions"][emoji] = [user_id]
                else:
                    message_data["reactions"][emoji].append(user_id)
                break
        else:
            conversations[channel_id].append({"message_id": message_id, "reactions": {emoji: [user_id]}})

    # Save conversations
    save_conversations(conversations)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Load conversations
    conversations = load_conversations()

    # Store messages and author IDs in the conversations dictionary
    channel_id = str(message.channel.id)
    author_id = message.author.id
    message_id = message.id
	
    if channel_id not in conversations:
        conversations[channel_id] = [{"author_id": author_id, "content": message.content, "message_id": message_id}]
    else:
        conversations[channel_id].append({"author_id": author_id, "content": message.content, "message_id": message_id})

    # Save conversations
    save_conversations(conversations)

    # Process commands
    await bot.process_commands(message)




@bot.tree.command(name="chatgpt", description="this is chatgpt")
@app_commands.describe(thing_to_say="say hello to the chatbot")
@app_commands.describe(version="versions are chatgpt4, fieldmanual, canned, wolfram,serpapi,conversationbuffermemory")
async def chat(interaction: discord.Interaction, thing_to_say: str, version: str):
    print("Received interaction")

    await interaction.response.defer()

    chatBotSettings = ChatBotSettings()
  
      
    chatOpenAI : ChatOpenAI = ChatOpenAI(
            temperature=0, openai_api_key=self.chatbotSettings.OPENAI_API_KEY)
    langchain_service = LangChainService(chatBotSettings, chatOpenAI)
    knowledge_base_service = KnowledgeBaseService()
    chatBotService = chatbot_service.ChatBotService(langchain_service,knowledge_base_service)
    response = chatBotService.chat_with_langchain(thing_to_say, version)
    await interaction.followup.send(response)


  #await interaction.response.send_message(response)



# Run the bot with your bot token
bot.run(os.environ["DISCORD_BOT_TOKEN"] )