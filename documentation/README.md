# Table of Contents
- [README.md](#table-of-contents)
    - [Background](#background)
    - [Prerequisites](#prerequisites)
    - [Overview](#overview)
    - [Installation](#installation)
    - [Contributing](#contributing)
    - [License](#license)
    - [Contact](#contact)

## Background
Reverse Stock Split Arbitrage (RSSA) is a trading strategy that involves buying shares of a company that is about to undergo a reverse stock split and then selling them after the split. The goal is to profit from the price inefficiencies that arise during the reverse stock split process. This project aims to automate the RSSA process using chatGPT, Discord bots, and a trading CLI tool. Further reading can be found in the [Prerequisites](#prerequisites) section.

## Prerequisites
- RSSA Strategy
    - [Here](https://www.revrss.com/blog/) is a blog that I used to learn about the RSSA strategy.
- Python
    - This project is written in Python. A basic understanding of Python and environment setup is required. I use [Anaconda](https://www.anaconda.com/) for my Python environment.
- RSS feed
    - This project uses an RSS feed to get news articles about reverse stock splits. Really Simple Syndication (RSS feeds) should not be confused with Reverse Stock Splits. The feed I use can be found [here](https://www.revrss.com/newswires.xml).
- auto-rsa
    - This project uses [auto-rsa](https://github.com/NelsonDane/auto-rsa), a tool for automatically trading stocks. I found familiarity with the tool to be helpful.
- chatGPT API
    - This project uses the chatGPT API to analyze news articles regarding reverse stock splits. You can find more information about the chatGPT API [here](https://openai.com/chatgpt).
- Discord Bots
    - This project uses Discord bots to communicate with users and provide updates on the RSSA process. You can find more information about Discord developer tools [here](https://discord.com/developers/docs/intro).

## Overview
In this section I will describe my current setup and provide links to each component of the project.

### RSS feed subscription
I have a bot that subscribes to the RSS feed found [here](https://www.revrss.com/newswires.xml), which posts news articles about reverse stock splits. I use [MonitoRSS](https://monitorss.xyz/) as the host for this service. I do not run this RSS feed service myself, and so I cannot guarantee it is still operational. This bot will periodically post links to news articles that mention reverse stock splits to a Discord channel (e.g. "reverse-stock-split-news").

### chatGPTbot
Here I have a discord bot that is run locally that monitors the "reverse-stock-split-news" channel for new messages. When a new message is posted, the bot will use BeautifulSoup to scrape the article and send it to the chatGPT API for analysis. By using a chatGPT descriptor, I can get a consistently-formatted response from the chatGPT API. This response contains the stock ticker, the date of the reverse stock split, the ratio of the split, and the reversal type. The bot will then process this information to determine if the stock is profitable.

> **&#9432;** Note:
> It is worth noting that chatGPT can often be wrong. As such I have tried to make this system lean towards false negatives rather than false positives. This means that if chatGPT is unsure about a stock, it will not recommend trading it.

Following a few checks, the bot will then post a message to a secondary channel (e.g. "stock-reversals") with a recommendation on whether or not to buy the stock, the reason for the recommendation, the stock ticker, exchange market, date of the reversal, ratio of the split, and the reversal type.

### purchasebot
This is a secondary discord bot that is run locally that monitors the "stock-reversals" channel for new messages. This bot does no language processing and simply reads messages and executes trades based on the recommendations given by the chatGPTbot. This bot will buy the stock at the market price. The bot will then post a message to a third channel (e.g. "purchases") with the stock ticker and the number of shares purchased.

### sellbot
There isn't currently a bot for selling stocks, but this will hopefully be implemented in the future.

### Error handling
A simple error handling system is implemented that will catch any exception thrown, and post the error to a "bot-errors" channel. This is to ensure that any issues are caught and can be resolved quickly. 
> **&#9432;** Note:
> A common issue will arrise from auto-rsa dependencies requiring an update. This can be resolved by stopping the bot, runing the command suggested in the error, and then restarting the bot.

## Installation
There are two installation guides provided. The [quickstart](./setup-guides/quickstart.md) guide only provides information on setting up the purchasebot. If you are in a discord server that already has the RSS feed subscription and chatGPTbot set up, there is no need to set those up yourself. The [full installation](./setup-guides/full-installation.md) guide provides information on setting up the entire system in your own discord server.

## Contributing
If you find any bugs or have any suggestions, please open an issue or a pull request. I will primarily be monitoring the issues and pull requests for any feedback or suggestions.

## Contact
If you have any questions or would like to contact me, you can reach me through issues or pull requests on this repository. I can additionally be reached through my email, stefancaldararu@gmail.com. Please include "RSSFA" in the subject line.