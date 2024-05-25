import logging
import asyncio
#import telegram
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, CallbackContext
import requests

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

ANYTHINGLLM_TOKEN  = 'Bearer XXXXXXX-XXXXXXX-XXXXXXX-XXXXXXX'
TELEGRAM_BOT_TOKEN = '1234567890:XXX-XXXXXXX-XXXXXXX-XXXXXXXXXXXXXXX'

async def reply(message, update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(text=message, chat_id=update.effective_chat.id)

# Fonction pour récupérer les messages envoyés au Bot
async def get_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("User Request : " + update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Please wait...")
    message = update.message.text
    await query_anythingllm(message, update, context)

# Fonction pour envoyer une requête à AnythingLLM
async def query_anythingllm(message, update, context):
    url = 'http://localhost:3001/api/v1/workspace/aya-23/chat'             ## CHANGE OR TUNE THE URL
    headers = {
        'accept': 'application/json',
        'Authorization': ANYTHINGLLM_TOKEN,
        'Content-Type': 'application/json',
    }
    data = {
        'message': message,
        'mode': 'chat'
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        logging.info("AnythingLLM : 200 Ok")
        response_json = response.json()
        final_reponse = response_json.get('textResponse', 'No textResponse found')
        #return final_reponse
        await reply(final_reponse, update, context)
    else:
        logging.error("Failed to get response from AnythingLLM.")
        exit(1)

# Fonction pour le /start du Bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! How can I help you?")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), get_message)
    application.add_handler(start_handler)
    application.add_handler(message_handler)
    application.run_polling()
