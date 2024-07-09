import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random
import logging
import config

logger = logging.getLogger(__name__)

# Set up Google Sheets API
def get_google_sheets_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(config.GOOGLE_SHEETS_CREDENTIALS_PATH, scope)
    client = gspread.authorize(creds)
    sheet = client.open(config.SHEET_NAME).sheet1
    return sheet.get_all_records()

# Select a random affirmation
def select_affirmation(affirmations, history, time_of_day):
    available_affirmations = []
    for a in affirmations:
        try:
            if a["Time of Day"] in ["Anytime", time_of_day] and a["Affirmation"] not in history:
                available_affirmations.append(a)
        except KeyError as e:
            logger.error(f"Missing key in affirmation: {e}. Affirmation data: {a}")

    if not available_affirmations:
        return None

    return random.choice(available_affirmations)

# Maintain history
def update_history(history, affirmation):
    history.append(affirmation)
    # Ensure no repetition within the last 30 days
    if len(history) > 30:
        history.pop(0)
    return history
