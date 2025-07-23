import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from googletrans import Translator

translator = Translator()
BOT_TOKEN = "8081127120:AAhYSUIQzsLmbysfCXw8GkPqW4kT8-z8x_Y"
group_config = {}

def start(update, context):
    update.message.reply_text("🤖 翻译机器人启动成功。\n发送 /translate on 开启自动翻译。")

def set_translate(update, context):
    chat_id = str(update.effective_chat.id)
    if len(context.args) > 0 and context.args[0].lower() == 'on':
        group_config[chat_id] = True
        update.message.reply_text("✅ 本群已开启自动翻译。")
    else:
        group_config[chat_id] = False
        update.message.reply_text("❌ 本群已关闭自动翻译。")

def auto_translate(update, context):
    chat_id = str(update.effective_chat.id)
    if not group_config.get(chat_id, False):
        return
    text = update.message.text
    try:
        result = translator.translate(text, dest='zh-cn')  # 翻译成中文
        update.message.reply_text(f"🌍 翻译：{result.text}")
    except Exception as e:
        update.message.reply_text("⚠️ 翻译失败，可能是网络或接口问题。")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("translate", set_translate))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, auto_translate))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
