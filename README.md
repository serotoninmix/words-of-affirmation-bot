# Affirmation Bot

A Telegram bot to send daily affirmations to your partner.

## Setup

1. **Clone the repository**:
    ```sh
    git clone https://your-repo-url.git
    cd affirmation_bot
    ```

2. **Create a virtual environment**:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up Google Sheets API**:
    - Follow the instructions to enable the Google Sheets API and download the credentials JSON file.
    - Place the credentials JSON file in the `credentials/` directory.

5. **Update configuration**:
    - Edit `src/config.py` to add your Telegram bot token and chat ID.

6. **Run the bot**:
    ```sh
    python src/scheduler.py
    ```

## Usage

- The bot will send affirmations twice a day at 8 AM and 8 PM.
- It ensures no repetition of affirmations within 30 days and adheres to the scheduling rules.
