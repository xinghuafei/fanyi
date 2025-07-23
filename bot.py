from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from googletrans import Translator
import os

BOT_TOKEN = "8081127120:AAGheAHP7SeEdvZU1cjGas_zk-G3v3ukYVA"

translator = Translator()
auto_translate_on = {}

def start(update, context):
    update.message.reply_text("欢迎使用翻译机器人！\n使用 /translate on 开启自动翻译。")

def translate_command(update, context):
    chat_id = update.effective_chat.id
    if context.args and context.args[0].lower() == "off":
        auto_translate_on[chat_id] = False
        update.message.reply_text("✅ 本群已关闭自动翻译。")
    else:
        auto_translate_on[chat_id] = True
        update.message.reply_text("✅ 本群已开启自动翻译。")

def handle_message(update, context):
    chat_id = update.effective_chat.id
    if not auto_translate_on.get(chat_id, False):
        return

    text = update.message.text
    src_lang = translator.detect(text).lang

    if src_lang == 'zh-cn' or src_lang == 'zh-tw':
        dest_lang = 'en'
    else:
        dest_lang = 'zh-cn'

    translated = translator.translate(text, dest=dest_lang)
    update.message.reply_text(f"🌍 翻译：{translated.text}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("translate", translate_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
