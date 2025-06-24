import requests
from django.conf import settings

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    resp = requests.post(url, json={'chat_id': chat_id, 'text': text})
    resp.raise_for_status()
