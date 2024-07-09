# src/get_chat_id.py

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import config
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    chat_id = update.effective_chat.id
    await update.message.reply_text(f'Hello! Your chat ID is {chat_id}')
    print(f"Chat ID: {chat_id}")

async def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    chat_id = update.effective_chat.id
    await update.message.reply_text(f'Your chat ID is {chat_id}')
    print(f"Chat ID: {chat_id}")

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(config.TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()

if __name__ == '__main__':
    main()
