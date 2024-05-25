# telegram-for-anythingllm

An API Integration from AnythingLLM to Telegram.

Requirements : 
```pip install python-telegram-bot```

You need an API Key from AnythingLLM and a Telegram Bot Token

# What is this script for ?
## main.py
from aya:8b-23-q4_K_M translated to English by llama3:8B-instruct-q8_0


The provided Python code is an example of a Telegram bot that uses the "python-telegram" library to interact with the Telegram API. Here's an analysis of the code:

1. Importations and configurations:
   - The code imports the necessary modules, including `logging` for logging, `asyncio` for asynchronous operations, and specific modules from "python-telegram".
   - Access tokens are defined for the Telegram API (`TELEGRAM_BOT_TOKEN`) and for accessing AnythingLLM (`ANYTHINGLLM_TOKEN`).

2. Message handling functions:
   - `reply(message, update, context)`: This function sends a response to the received message by the bot.
   - `get_message(update, context)`: This function handles text messages sent by the user. It records the message, sends a response "Please wait...", and then calls the `query_anythingllm` function to obtain an answer from the AnythingLLM API.
   - `query_anythingllm(message, update, context)`: This function sends a request to the AnythingLLM API with the received message. It also manages the API's responses and returns the response to the bot.

3. Bot startup function:
   - The `start(update, context)` function is handled by the bot when an user starts the bot using the `/start` command. It sends a welcome message to the user.

4. Execution of the bot:
   - The code creates an instance of the Telegram application with the provided token.
   - Handlers are added to the application to handle text messages and commands.
   - The bot begins to listen for real-time updates and responds to received messages.

In summary, this code creates a simple Telegram bot that can interact with users by sending responses generated by AnythingLLM. It handles text messages, commands, and provides a welcome response when the bot is started. Please note that you should replace 'XXXXXXX' in `ANYTHINGLLM_TOKEN` with your real access token for AnythingLLM.

## main_actions.py
I'm on Windows 10, with Powershell 7, and I wanted the bot to be able to execute some basic actions.

With this script, it should be able to :

* shel (to run some shell commands)                                                        `NOT TESTED`

* pyth (to run pythons scripts)                                                            `TESTED OK`

* ping (to do some ICMP tests)                                                             `TESTED OK`

* port (to do some port scan to see if port is open)                                       `TESTED OK`

* link (to upload a web link to anythingllm database, and embed into your current model)   `TESTED OK`

* curl (to make some basic web requests).                                                  `TESTED OK`

Prompt is included in the script
