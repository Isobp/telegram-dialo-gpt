import os, logging, requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction

def get_response(text):
    resp = requests.post(
        "https://api-inference.huggingface.co/models/microsoft/DialoGPT-small",
        json={"inputs": text}
    )
    data = resp.json()
    return data[0].get("generated_text", "آسف ما فهمت")

TOKEN = os.getenv("TELEGRAM_TOKEN")
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher
logging.basicConfig(level=logging.INFO)

def start(update, ctx):
    update.message.reply_text("مرحباً! اسألني شيء 😊")

def handle_msg(update, ctx):
    update.message.chat.send_action(action=ChatAction.TYPING)
    reply = get_response(update.message.text)
    update.message.reply_text(reply)

dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_msg))

if __name__ == "__main__":
    updater.start_polling()
    updater.idle()
