import os
from discord.ext import commands
import discord
from dotenv import load_dotenv
import openai
import requests
from bs4 import BeautifulSoup

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID'))
SOURCE_CHANNEL_ID = int(os.getenv('SOURCE_CHANNEL_ID'))
openai.api_key = os.getenv('OPEN_AI_KEY')

def analyze_article(url):
    # Fetch the HTML content of the article
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the article text
    article_text = ''
    article = soup.find('article')
    if article:
        paragraphs = article.find_all('p')
        article_text = ' '.join([p.get_text() for p in paragraphs])

    return article_text

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

    if not target_channel:
        print('Target channel not found')
        return
    
    # check if message contains http
    if message.content.startswith('http'):
        url = message.content
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract text from the parsed HTML
            text = soup.get_text()
            chatCompletion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": f"You are a financial assistant."},
                        {"role": "user", "content": f"""I will provide you with a press release, and I want you to identify a few key components. You must identify what stock is being discussed in the article, and provide the ticker for the stock, the date when the stock is undergoing a reversal, what ratio the reversal will be at, and what type of reversal the stock will undergo. The options for the type of reversal are "round up", "round down", "cash in lieu", "round to nearest whole share", or "unspecified". Your response should be structured as follows (with the example data replaced): 
                        
                        "ticker: EXPL
                            date: 01-01/2024
                            ratio: 1:100
                            reversal: round up
                        "
                        
                        Here is the article: {text}"""}]
            )
            # get the response from the AI and post it to the target channel
            await target_channel.send(chatCompletion.choices[0].message.content)

bot.run(BOT_TOKEN)

