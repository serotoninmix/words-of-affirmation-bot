import schedule
import time
from datetime import datetime, timedelta
from telegram_bot import send_message
from utils import get_google_sheets_data, select_affirmation, update_history
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Scheduler script started")

affirmations = get_google_sheets_data()
history = []
affirmations_sent_today = 0
last_sent_time = None

async def send_affirmation():
    global affirmations_sent_today, last_sent_time, history

    logger.info("send_affirmation function called")

    # Ensure no more than 2 affirmations per day
    if affirmations_sent_today >= 2:
        logger.info("Maximum affirmations sent today")
        return

    now = datetime.now()

    # Ensure at least 5 hours between affirmations
    if last_sent_time and (now - last_sent_time) < timedelta(hours=5):
        logger.info("Waiting for 5 hours between affirmations")
        return

    # Determine the time of day
    time_of_day = 'Morning' if now.hour < 12 else 'Night' if now.hour >= 18 else 'Anytime'
    affirmation = select_affirmation(affirmations, history, time_of_day)

    if affirmation:
        await send_message(affirmation["Affirmation"])
        history = update_history(history, affirmation["Affirmation"])
        affirmations_sent_today += 1
        last_sent_time = now
        logger.info(f"Sent affirmation: {affirmation['Affirmation']}")

    # Reset counter at midnight
    if now.hour == 0:
        affirmations_sent_today = 0

async def check_minimum_affirmations():
    # Ensure at least 1 affirmation every 3 days
    global affirmations_sent_today
    if affirmations_sent_today == 0:
        await send_affirmation()

def run_async_job(job):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(job)

# Schedule jobs
schedule.every().day.at("08:00").do(lambda: run_async_job(send_affirmation()))
schedule.every().day.at("20:00").do(lambda: run_async_job(send_affirmation()))
schedule.every(3).days.do(lambda: run_async_job(check_minimum_affirmations()))

logger.info("Scheduled jobs added")

# Main loop
while True:
    schedule.run_pending()
    time.sleep(1)
