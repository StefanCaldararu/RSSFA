import os
from discord.ext import commands
import discord
from dotenv import load_dotenv
# import openai
# import requests
# from bs4 import BeautifulSoup

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID'))
SOURCE_CHANNEL_ID = int(os.getenv('SOURCE_CHANNEL_ID'))
# openai.api_key = os.getenv('OPEN_AI_KEY')


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Bot is ready')
    channel = bot.get_channel(TARGET_CHANNEL_ID)
    await channel.send('Hello World!')

@bot.event
async def on_message(message):
    # Avoid the bot responding to its own messages
    if message.author == bot.user:
        return

    if message.channel.id != SOURCE_CHANNEL_ID:
        return
    
    # Fetch the target channel
    target_channel = bot.get_channel(TARGET_CHANNEL_ID)

    if target_channel:
        # Send the content of the received message to the target channel
        await target_channel.send(f"Message from {message.author}: {message.content}")


bot.run(BOT_TOKEN)

