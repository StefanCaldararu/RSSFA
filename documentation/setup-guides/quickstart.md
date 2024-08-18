# Quickstart
This guide will help you get started with the purchasebot setup. This assumes you are already in a discord server that has the RSS feed subscription and chatGPTbot set up. The primary use case for this is if you heard about this tool from a friend and have been invited to their server. This way, the cost of chatGPT API tokens and having multiple bots running in the background is only incurred by one user.

> **&#9432;** Note:
> I use Linux / Mac OS for development. This guide may not work on Windows as intended, or some commands may need to be modified. All commands are provided in bash syntax. If you are running on Windows, you can either replace the bash commands with the equivalent Windows commands, use the Windows Subsystem for Linux (WSL), or setup a virtual machine with a Linux distribution to run the bots.

## Cloning the Repository
This project is hosted on github and includes [auto-rsa](https://github.com/NelsonDane/auto-rsa) as a submodule. To clone the repository, run the following command:

```bash
git clone --recurse-submodules https://github.com/StefanCaldararu/RSSFA
```

If you have already cloned the repository and forgot to include the `--recurse-submodules` flag, you can run the following command to get the submodule from within the repository:

```bash
git submodule init
git submodule update
```

## Setting up the bot
I used [this](https://discordpy.readthedocs.io/en/stable/discord.html) tutorial to setup my discord bots. You will need to create a bot and get the token for the bot. **MAKE SURE TO SAVE THE BOT TOKEN IN A SAFE PLACE.** I gave my bot administrator permissions because I am lazy, and want to be able to recieve messages from my bot. In most cases, you will only need to be able to read messages. After finishing this tutorial, You should see your bot as having been invited to the discord server.

## Setting up the Environment
This project uses python and requires some specific dependency versions. Additionally, some of my dependencies are frozen while the `auto-rsa` submodule continues to update their package versions. Once you have [Anaconda](https://www.anaconda.com/) installed and have setup a python 3.10 environment, I recommend installing the `RSSFA` dependencies before installing the `auto-rsa` dependencies. This will ensure that the updated versions are installed for the `auto-rsa` dependencies. From within the `RSSFA` directory, run the following command:

```bash
pip install -r requirements.txt
cd auto-rsa
pip install -r requirements.txt
```

Additionally, you will need to populate the `.env` file with your bots information. This includes the `PURCHASE_BOT_TOKEN` (generated in teh previous step), as well as the `STOCK_REVERSALS_CHANNEL_ID`, `PURCHASES_CHANNEL_ID`, and `ERRORS_CHANNEL_ID`. The channel ID's can be found by activating developer mode in discord (`User Settings` -> `Advanced` -> `Developer Mode`), right clicking on the channel, and selecting `Copy ID`. Make sure to include 'quotes' around the bot token, but not around the channel ID's. 

Additionally, you will need to populate the `auto-rsa/.env` file with your brokerage keys. This is covered in the `auto-rsa` documentation.

## Running
To run the bot, simply run the following command in the `RSSFA` directory:

```bash
python purchasebot.py
```

You should receive two discord information messages, followed by a `Bot is ready` message. In this case the bot should be ready to go! You should receive auto-rsa messages in this terminal window whenever a stock is purchased. The bot is currently only setup for dry-runs on firstrade, but this is easily modifiable in the `purchasebot.py` file (do a text search for `args = ['buy', str(quantity), str(ticker), 'firstrade', 'true']` and modify the appropriate `auto-rsa` arguments).

> **&#9432;** Note:
> The bot is currently setup to not post any messages to discord channels. If you are running your own server and would like to be able to do this, please reference the [full installation](./setup.md) guide.