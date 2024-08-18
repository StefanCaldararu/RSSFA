import subprocess
from discord.ext import commands
import discord
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('PURCHASE_BOT_TOKEN')
SOURCE_CHANNEL_ID = int(os.getenv('STOCK_REVERSALS_CHANNEL_ID'))
TARGET_CHANNEL_ID = int(os.getenv('PURCHASES_CHANNEL_ID'))
ERRORS_CHANNEL_ID = int(os.getenv('ERRORS_CHANNEL_ID'))

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Bot is ready')
    target_channel = bot.get_channel(TARGET_CHANNEL_ID)
    await target_channel.send('Bot is ready')

bot.run(BOT_TOKEN)