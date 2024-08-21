# Setup

This guide will help you setup the full RSSFA bot suite that I have. This includes the RSS feed subscription, chatGPTbot, and purchasebot. While I will not be providing a step-by-step guide, there will be links to tutorials that I used to familiarize myself with these tools. For a full list of prerequisites, reference this [README](../README.md).

> **&#9432;** Note:
> I use Linux / Mac OS for development. This guide may not work on Windows as intended, or some commands may need to be modified. All commands are provided in bash syntax. If you are running on Windows, you can either replace the bash commands with the equivalent Windows commands, use the Windows Subsystem for Linux (WSL), or setup a virtual machine with a Linux distribution to run the bots.

## Setting up a Discord Server

Reference [this](https://support.discord.com/hc/en-us/articles/204849977-How-do-I-create-a-server) support doc for creating a discord server. I recommend also creating all the necessary channels at this time. I have my channels named as follows:

- reverse-stock-split-news: The channel where the RSS feed subscription bot posts news articles about reverse stock splits.
- stock-reversals: The channel where the chatGPTbot posts recommendations on whether or not to buy a stock.
- purchases: The channel where the purchasebot posts the stock ticker and the number of shares purchased.
- bot-errors: The channel where all bots are able to post error messages.

## Setting up the RSS feed subscription
As mentioned previously, I use [MonitoRSS](https://monitorss.xyz/) to make posts to discord whenever a new article is posted to [this](https://www.revrss.com/newswires.xml) RSS feed. Once you have this setup, you should see the `MonitoRSS` bot posting links to press releases in the `reverse-stock-split-news` channel.

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

## Setting up the chatGPTbot
This is the bot that requires the most setup. I used [this](https://discordpy.readthedocs.io/en/stable/discord.html) guide for help with setting up a basic discord bot. **MAKE SURE TO SAVE THE BOT TOKEN IN A SAFE PLACE.** This bot will need to be able to read messages from the `reverse-stock-split-news` channel, and post messages to the `stock-reversals` channel. Make sure to populate the `CHAT_BOT_TOKEN` in the `.env` file with the bot token, and the `REVERSE_STOCK_SPLIT_NEWS_CHANNEL_ID`, `STOCK_REVERSALS_CHANNEL_ID`, and `ERRORS_CHANNEL_ID` with the appropriate channel ID's. The channel ID's can be found by activating developer mode in discord (`User Settings` -> `Advanced` -> `Developer Mode`), right clicking on the channel, and selecting `Copy ID`. Make sure to include 'quotes' around the bot token, but not around the channel ID's.

Additionally, you will need to populate the `OPEN_AI_KEY` with an API key from OpenAI. I used [this](https://platform.openai.com/docs/quickstart) tutuorial to get started with the OpenAI API. Make sure to include 'quotes' around the API key. Your OpenAI account must also be funded in order for the chatGPTbot to be able to access the API.

Once all of these keys are populated, make sure to setup a python environment with the dependencies in the `requirements.txt` file. I use [Anaconda](https://www.anaconda.com/) to manage my python environments. Once you have a python 3.10 environment setup, run the following command from within the `RSSFA` directory:

```bash
pip install -r requirements.txt
```
The chatGPTbot is now ready to run. Simply run the following command in the `RSSFA` directory:

```bash
python chatGPTbot.py
```

You should see a `Bot is ready` message in the terminal window. Try posting an old link in the `reverse-stock-split-news`, and we should receive a message in the `stock-reversals` channel looking something like this:

```bash
Purchasable: FALSE
Reason: Too close to reversal date
Stock: TOVX
Exchange: ASE
Price: 0.13279999792575836
Date: 08-26-2024
Ratio: 1-25
Reversal: round up
Estimated Profit: N/A
```

To keep the bot running, I am currently using [tmux](https://github.com/tmux/tmux/wiki) to be able to run the bot in the background. In the future, I hope to be able to host this bot on either [AWS](https://aws.amazon.com/) or on a small computer sucha as a [Raspberry Pi](https://www.raspberrypi.org/).

## Setting up the purchasebot

The [quickstart](./quickstart.md) provides information on how to setup the purchasebot. 