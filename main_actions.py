# Temperature 0.3

## PROMPT for AnythingLLM
# Tu es un Assistant Virtuel. Tout ce que tu écris est surveillé en temps réel par un serveur informatique, afin de pouvoir déclencher un script selon tes instructions. Tu es le relais de l'Utilisateur. L'Utilisateur ne peux pas faire les actions qu'il te demande. Toi tu peux, car tu est propulsé par un puissant serveur qui sait analyser tes demandes et les exécuter. Ce serveur n'exécute les requêtes QUE quand elles sont formées comme indiqué dans ces exemples :

# CMD | None | this is a Test
# CMD | shel | set
# CMD | pyth | my_python_script.py
# CMD | ping | 192.168.0.1
# CMD | port | 192.168.0.1:8080
# CMD | link | https://www.wikidata.org/wiki/Q90
# CMD | curl | http://192.168.0.1/json.htm?type=command&param=switchlight&idx=123&switchcmd=Toggle

# Lorsque tu renvoies une réponse formattée de la sorte, ta réponse est interceptée et analysée par le serveur. Si elle est bien formée, il l'éxecute, puis il envoit un retour d'état à l'Utilisateur, sans que tu n'en soies informé.
# Le premier champ indique au serveur que le message est une commande à exécuter. Il est impératif que le message commence par CMD pour qu'il soit reconnu par le serveur comme une commande à traiter.
# Le deuxième champ indique le type de commande à exécuter :
# None (pour les tests)
# shel (pour éxecuter des commandes Shell)
# pyth (pour éxecuter des commandes python ou des scripts en python)
# ping (pour faire des tests ICMP)
# port (pour faire des scan de port réseau sur des hôtes)
# link (pour uploader des pages web dans ta base de données)
# curl (pour faire des requêtes web basiques).
# Le troisième et dernier champ contient les données nécessaires pour exécuter la commande demandée.
# Dans le cas d'un shell, c'est une commande shell.
# Dans le cas d'un python, ce sera le nom d'un script python.
# Dans le cas d'un ping, ce sera l'adresse IP ou le nom d'hôte à pinger.
# Dans le cas d'un port, ce sera l'adresse IP et le port à scanner.
# Dans le cas d'un link, ce sera l'URL d'un site web à inclure dans ta base de données, grace à la méthode d'embedding. Si l'adresse du site n'incluait pas http:// ou https://, tu les ajoutera pour que le site à inclure soit de la forme : http://www.google.fr. Puis tu réponds selon le format indiqué dans tes consignes.
# Dans le cas d'un curl, ce sera l'URL sur laquelle faire le curl.
# Par exemple, pour allumer la lumiere principale du Bureau à Paris, il faut envoyer :
# CMD | curl | http://192.168.0.1/json.htm?type=command&param=switchlight&idx=123&switchcmd=On
# Et pour l'éteindre, il faudra envoyer :
# CMD | curl | http://192.168.0.1/json.htm?type=command&param=switchlight&idx=123&switchcmd=Off
# La switchcmd "Toggle" permet de basculer la lumière sur son état opposé. Il est aussi possible d'envoyer une switchcmd "On" ou "Off", ce qui aura pour effet d'allumer ou d'éteindre la lumière concernée.

# Compte tenu de la conversation suivante, de la pertinence du contexte, et de la question posée, produis une réponse en répondant à la question actuelle posée par l'utilisateur. Renvois uniquement ta réponse à la question en fonction des informations ci-dessus en suivant les instructions de l'utilisateur si nécessaire. Si aucune information pertinente n'est fournie, n'utilise pas les informations fournies et réponds normalement.
## END of PROMPT

## For Memory
# var  = "CMD | None | this is a Test"
# var  = "CMD | shel | set"
# var  = "CMD | pyth | my_python_script.py"
# var  = "CMD | ping | 192.168.0.1"
# var  = "CMD | port | 192.168.0.1:8080"
# var  = "CMD | link | https://www.wikidata.org/wiki/Q90"
# var  = "CMD | curl | http://192.168.0.1/json.htm?type=command&param=switchlight&idx=123&switchcmd=Toggle"

import re
import os
import ping3
import logging
import asyncio
import requests
import subprocess
import socket
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

ANYTHINGLLM_TOKEN  = 'Bearer XXXXXXX-XXXXXXX-XXXXXXX-XXXXXXX'
TELEGRAM_BOT_TOKEN = '1234567890:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
ANYLLM_MODEL       = 'aya-23'
ANYURLHOST         = 'localhost'
ANYURLPORT         = '3001'
ANYURLEMBED        = 'http://' + ANYURLHOST + ':' + ANYURLPORT + '/api/v1/workspace/' + ANYLLM_MODEL + '/update-embeddings'
ANYURLUPLOAD       = 'http://' + ANYURLHOST + ':' + ANYURLPORT + '/api/v1/document/upload-link'
ANYURLCHAT         = 'http://' + ANYURLHOST + ':' + ANYURLPORT + '/api/v1/workspace/' + ANYLLM_MODEL + '/chat'
POWERSHELLEXEC     = 'C:\\Program Files\\PowerShell\\7\\pwsh.exe'

def ping_port(host, port):
    logging.info("FUNC : Port Scan")
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except OSError:
        return False

def upload_link(link):
    logging.info("FUNC : Upload Link")
    url = ANYURLUPLOAD
    headers = {
        'accept': 'application/json',
        'Authorization': ANYTHINGLLM_TOKEN,
        'Content-Type': 'application/json',
    }
    data = {
        "link": link
    }
    upload_response = requests.post(url, headers=headers, json=data)
    if upload_response.status_code == 200:
        logging.info("FUNC : Upload Ok")
        upload_response_json = upload_response.json()
        success_response = upload_response_json.get('success', 'No SUCCESS found')
        documents = upload_response_json.get('documents', 'No DOCUMENTS found')
        doc_full_location = documents[0]['location']
        doc_location = "custom-documents/" + os.path.basename(doc_full_location)
        return True, doc_location
    else:
        return False

def embed(file):
    logging.info("FUNC : Embeddings")
    logging.info("FUNC : File path : " + file)
    url = ANYURLEMBED
    headers = {
        'accept': 'application/json',
        'Authorization': ANYTHINGLLM_TOKEN,
        'Content-Type': 'application/json',
    }
    data = {
        "adds": [file]
    }
    response = requests.post(url, headers=headers, json=data)
    if (response.status_code == 200):
        return True
    else:
        return False

def curl_url(url):
    logging.info("FUNC : cURL URL")
    response = requests.post(url)
    if response.status_code == 200:
        response_json = response.json()
        text_response = response_json.get('status', 'No STATUS found')
        logging.info("Status : " + text_response)
        return text_response

def prepare_cmd(var):
    logging.info("FUNC : Prepare CMD")
    commande  = var.split("|")[0].strip()
    logging.info(f"Message Type : {commande}")
    programme  = var.split("|")[1].strip()
    commande_brute  = var.split("|")[-1].strip()
    logging.info(f"Commande brute : {commande_brute}")
    if programme == "None":
        logging.info("NO EXTERNAL PROG")
        return commande_brute
    else:
        logging.info(f"Programme externe : {programme}")
        return commande_brute, programme

# Fonction pour le /start du Bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Bonjour! Posez-moi une question!")

# Fonction pour récupérer les messages envoyés au Bot
async def get_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("User Request : " + update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Reçu. Réponse en cours de génération...")
    message = update.message.text
    await query_anythingllm(message, update, context)

# Fonction pour envoyer une requête à AnythingLLM
async def query_anythingllm(message, update, context):
    url = ANYURLCHAT
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

# Fonction pour envoyer la reponse au user
async def reply(message, update: Update, context: ContextTypes.DEFAULT_TYPE):
    # check if bot reply contains a CMD to execute
    if message.startswith("CMD "):
        logging.info("CMD detected in LLM answer")
        logging.info(message)
        commande_brute, programme = prepare_cmd(message)
        # logging.info("Programme : " + programme)
        # logging.info("Commande  : " + commande_brute)
        if (programme == "curl"):
            logging.info("CURL detected in LLM answer")
            # extract URL for curl
            logging.info("Extracting URL")
            extracted_url = commande_brute
            # run a cURL to extracted URL
            logging.info("Running cURL")
            message = curl_url(extracted_url)
            await context.bot.send_message(text=message, chat_id=update.effective_chat.id)
        elif (programme == "ping"):
            logging.info("PING detected in LLM answer")
            adresse_ip = commande_brute
            resultat = ping3.ping(adresse_ip)
            if resultat:
                # ping OK
                message = (f"L'adresse {adresse_ip} est accessible.")
            else:
                # ping KO
                message = (f"L'adresse {adresse_ip} n'est PAS accessible.")
            await context.bot.send_message(text=message, chat_id=update.effective_chat.id)
        elif (programme == "shel"):
            logging.info("SHELL detected in LLM answer")
            commande = commande_brute
            result = subprocess.run([POWERSHELLEXEC, "-Command", commande], shell=True, capture_output=True, text=True, encoding="cp858")
            message = (result.stdout)
            await context.bot.send_message(text=message, chat_id=update.effective_chat.id)
        elif (programme == "port"):
            logging.info("PORT Scan detected in LLM answer")
            host  = commande_brute.split(":")[0].strip()
            port  = commande_brute.split(":")[1].strip()
            logging.info("HOST : " + host)
            logging.info("PORT : " + port)
            if ping_port(host, port):
                message = (f"Le port {port} est ouvert sur l'hôte {host}")
            else:
                message = (f"Le port {port} n'est PAS ouvert sur l'hôte {host}")
            await context.bot.send_message(text=message, chat_id=update.effective_chat.id)
        elif (programme == "link"):
            logging.info("LINK detected for Upload in LLM answer")
            result = upload_link(commande_brute)
            status = result[0]
            doc_path = result[1]
            if not status:
                message = "ECHEC Upload"
                await context.bot.send_message(text=message, chat_id=update.effective_chat.id)
            else:
                message = "Document Uploaded avec succès. Patientez durant l'embedding... (1mn max.)"
                await context.bot.send_message(text=message, chat_id=update.effective_chat.id)
                ## EMBED directly
                if embed(doc_path):
                    message = "Document Embedded avec succès. Vous pouvez désormais poser une question en rapport avec ce document."
                else:
                    message = "ECHEC Embedding"
                await context.bot.send_message(text=message, chat_id=update.effective_chat.id)
        elif (programme == "pyth"):
            logging.info("PYTHON detected in LLM answer")
            commande = "python " + commande_brute
            result = subprocess.run([POWERSHELLEXEC, "-Command", commande], shell=True, capture_output=True, text=True, encoding="cp858")
            message = (result.stdout)
            if not message:
                message = (result.stderr)
            await context.bot.send_message(text=message, chat_id=update.effective_chat.id)
        else:
            logging.info("No External Prog detected in LLM answer")
            message = "This seems to be a TEST"
            await context.bot.send_message(text=message, chat_id=update.effective_chat.id)
    else:
        logging.info("Normal Message detected in LLM answer")
        await context.bot.send_message(text=message, chat_id=update.effective_chat.id)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), get_message)
    application.add_handler(start_handler)
    application.add_handler(message_handler)
    application.run_polling()
