import subprocess
from discord.ext import commands
import discord
from dotenv import load_dotenv
import os
import math

load_dotenv()

BOT_TOKEN = os.getenv('PURCHASE_BOT_TOKEN')
SOURCE_CHANNEL_ID = int(os.getenv('STOCK_REVERSALS_CHANNEL_ID'))
# TARGET_CHANNEL_ID = int(os.getenv('PURCHASES_CHANNEL_ID'))
# ERRORS_CHANNEL_ID = int(os.getenv('ERRORS_CHANNEL_ID'))

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Bot is ready')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.channel.id != SOURCE_CHANNEL_ID:
        return
    try:
        # split the message into lines
        lines = message.content.split('\n')
        # get if it is a purchase or not
        purchase = lines[0].split(': ')[1].strip().lower()
        # if it is not a purchase, return
        if purchase == 'false':
            return
        # get the ticker from the message
        ticker = lines[2].split(': ')[1].strip()
        # get the type of reversal from the message
        reversal = lines[7].split(': ')[1].strip().lower()
        # get the ratio
        ratio = lines[6].split(': ')[1].strip()
        fratio = float(ratio.split('-')[0])
        if fratio == 1:
            fratio = float(ratio.split('-')[1])
        # if roundup, only purchase one
        if reversal == 'round up':
            quantity = 1
        else:
            quantity = math.ceil(fratio/2)+1
        # purchase the stock.
            
        script_path = 'auto-rsa/autoRSA.py'
        args = ['buy', str(quantity), str(ticker), 'firstrade', 'true']
        print("running subprocess")
        process = subprocess.Popen(['python3', script_path] + args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        process.stdin.write('\n')
        process.stdin.flush()

        # Stream the output in real-time
        for line in process.stdout:
            print(line, end='')
        # Wait for the process to finish and get the return code
        process.stdout.close()
        process.wait()

        # stdout, stderr = process.communicate()
        # print("Output:", stdout.decode())
        # print("Error:", stderr.decode())
        # print("Return Code:", process.returncode)
        if(process.returncode != 0):
            # errors_channel = bot.get_channel(ERRORS_CHANNEL_ID)
            # await errors_channel.send(f"An error occurred with purchase: {process.stderr}")
            return
        # send a message to the target channel
        # target_channel = bot.get_channel(TARGET_CHANNEL_ID)
        # await target_channel.send(f"Purchase of {quantity} shares of {ticker} successful.")


    except Exception as e:
        print(e)
        # errors_channel = bot.get_channel(ERRORS_CHANNEL_ID)
        # await errors_channel.send(f"An error occurred: {e}")

bot.run(BOT_TOKEN)



# import subprocess

# # Path to the script you want to run
# script_path = 'path/to/your_script.py'

# # Arguments to pass to the script
# args = ['arg1', 'arg2', 'arg3']

# # Launch the script with arguments
# process = subprocess.Popen(['python', script_path] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# # Optionally, read output and error
# stdout, stderr = process.communicate()

# # Print the output and error (if any)
# print("Output:", stdout.decode())
# print("Error:", stderr.decode())
# print("Return Code:", process.returncode)