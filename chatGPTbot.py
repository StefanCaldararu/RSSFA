import os
from discord.ext import commands
import discord
from dotenv import load_dotenv
import openai
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import math

load_dotenv()

BOT_TOKEN = os.getenv('CHAT_BOT_TOKEN')
TARGET_CHANNEL_ID = int(os.getenv('STOCK_REVERSALS_CHANNEL_ID'))
SOURCE_CHANNEL_ID = int(os.getenv('REVERSE_STOCK_SPLIT_NEWS_CHANNEL_ID'))
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

@bot.event
async def on_message(message):
    try:
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
                    n=3,
                    messages=[{"role": "system", "content": f"You are a financial assistant."},
                            {"role": "user", "content": f"""I will provide you with a press release, and I want you to identify a few key components. You must identify what stock is being discussed in the article, and provide the ticker for the stock, the date when the stock is undergoing a reversal, what ratio the reversal will be at, and what type of reversal the stock will undergo. Describe the stock in the following foramt: 
                            
                            [start of description]
                            * ticker: [ticker]
                            * date: [date]
                            * ratio: [ratio]
                            * reversal: [reversal]
                            [end of description]
                            
                            Rules:
                            1. The ticker must be capitalized
                            2. The date must be in the format mm-dd-yyyy
                            3. The ratio must be in the format x-y
                            4. The options for the type of reversal are "round up", "round down", "cash in lieu", "round to nearest whole share", or "unspecified"
                            5. Do not include the [start of description] or [end of description] tags in your response
                            6. Do not include any marker symbols from the description, specifically *, [, ], or any quotation marks.
                            7. Do not include any other information in your response, and no additional lines beyond the 4 required lines.
                            
                            Here is the article: {text}"""}]
                )
                print(chatCompletion.choices[0].message.content)
                print(chatCompletion.choices[1].message.content)
                print(chatCompletion.choices[2].message.content)
                # get the ticker from the generated message
                ticker = chatCompletion.choices[0].message.content.split('\n')[0].split(': ')[1]
                # remove any " or [ or ] or * from the ticker
                ticker = ticker.replace('"', '')
                ticker = ticker.replace('[', '')
                ticker = ticker.replace(']', '')
                ticker = ticker.replace('*', '')
                # get the date from the generated message
                date = chatCompletion.choices[0].message.content.split('\n')[1].split(': ')[1]
                date = date.replace('"', '')
                date = date.replace('[', '')
                date = date.replace(']', '')
                date = date.replace('*', '')
                # get the ratio from the generated message
                ratio = chatCompletion.choices[0].message.content.split('\n')[2].split(': ')[1]
                ratio = ratio.replace('"', '')
                ratio = ratio.replace('[', '')
                ratio = ratio.replace(']', '')
                ratio = ratio.replace('*', '')
                # get the reversal from the generated message
                reversal = chatCompletion.choices[0].message.content.split('\n')[3].split(': ')[1]
                reversal = reversal.replace('"', '')
                reversal = reversal.replace('[', '')
                reversal = reversal.replace(']', '')
                reversal = reversal.replace('*', '')

                reversal1 = chatCompletion.choices[1].message.content.split('\n')[3].split(': ')[1]
                reversal1 = reversal1.replace('"', '')
                reversal1 = reversal1.replace('[', '')
                reversal1 = reversal1.replace(']', '')
                reversal1 = reversal1.replace('*', '')
                
                reversal2 = chatCompletion.choices[2].message.content.split('\n')[3].split(': ')[1]
                reversal2 = reversal2.replace('"', '')
                reversal2 = reversal2.replace('[', '')
                reversal2 = reversal2.replace(']', '')
                reversal2 = reversal2.replace('*', '')
        
                # get the exchange from the stock
                stock = yf.Ticker(ticker)
                exchange = stock.info.get('exchange', 'N/A')
                price = stock.history(period="1d")['Close'][0]


                # generate the default message
                default_message = f"""Stock: {ticker}\nExchange: {exchange}\nPrice: {price}\nDate: {date}\nRatio: {ratio}\nReversal: {reversal}"""
                # if the reversals do not match, post a message stating that in the target channel
                if reversal != reversal1 or reversal != reversal2:
                    await target_channel.send(f"""Purchasable: FALSE\nReason: Unknown reversal\n{default_message}\nEstimated Profit: N/A""")
                    return
                # if the reversal is not a roundup or round to nearest, post a message stating that in the target channel
                if reversal != 'round up' or reversal != 'round to nearest':
                    await target_channel.send(f"""Purchasable: FALSE\nReason: {reversal}\n{default_message}\nEstimated Profit: N/A""")
                    return
                # check if stock is traded on NYSE, NASDAQ, or AMEX
                if exchange != 'NYSE' and exchange != 'NASDAQ' and exchange != 'ASE':
                    await target_channel.send(f"""Purchasable: FALSE\nReason: Exchange not supported\n{default_message}\nEstimated Profit: N/A""")
                    return
                # check if the stock is valued at more then a dollar, and then don't purchase
                if price > 1:
                    await target_channel.send(f"""Purchasable: FALSE
                                                Reason: Price too high
                                                {default_message}
                                                Estimated Profit: N/A""")
                    return
                # get the ratio as an float, rounded to the nearest 2 decimal places after the decimal
                fratio = float(ratio.split('-')[0])
                if(fratio == 1):
                    fratio = float(ratio.split('-')[1])
                # if the reversal is a round up, get the estimated profit
                if reversal == 'round up':
                    # get the estimated profit
                    profit = round(price, 2) * fratio - round(price, 2)
                # if the reversal is a round to nearest, get the estimated profit
                elif reversal == 'round to nearest':
                    # get the estimated profit
                    profit = round(price, 2) * fratio - round(price, 2) * math.ceil(fratio)
                    # if we are spending more than a dollar don't buy the stock
                    if(round(price,2) * math.ceil(fratio) > 1):
                        await target_channel.send(f"""Purchasable: FALSE\nReason: Price too high\n{default_message}\nEstimated Profit: {profit}""")
                        return
                # if the estimated profit is less than .50, don't purchase
                if profit < .50:
                    await target_channel.send(f"""Purchasable: FALSE\nReason: Profit too low\n{default_message}\nEstimated Profit: {profit}""")
                    return
                # otherwise we can purchase so send a message.
                await target_channel.send(f"""Purchasable: TRUE\nReason: N/A\n{default_message}\nEstimated Profit: {profit}""")
    except Exception as e:
        await target_channel.send(f"An error occurred: {e}")

bot.run(BOT_TOKEN)

