from telegram import Bot
import config
import asyncio

bot = Bot(token=config.TELEGRAM_TOKEN)

async def send_message(text):
    await bot.send_message(chat_id=config.CHAT_ID, text=text)

# Initialize and start the bot
if __name__ == "__main__":
    from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
    import logging

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /start is issued."""
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I will be sending you daily affirmations.")

    application = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()
