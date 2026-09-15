import os
import random
from telethon import TelegramClient, events

# 4.1.3: Initialize values from environment variables or use placeholders
API_ID = int(os.environ.get('TELEGRAM_API_ID', 123456))
API_HASH = os.environ.get('TELEGRAM_API_HASH', 'your_api_hash_here')
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'your_bot_token_here')

# Create the robot client instance
client = TelegramClient('bot_session', API_ID, API_HASH)

async def send_verification_code(chat_id, reference_number):
    """2.2.1: Send 2FA verification details to the user via Telegram"""
    message = (
        f"🚨 **Security Verification** 🚨\n\n"
        f"Your Reference Number: `{reference_number}`\n"
        f"Please verify this reference number on the platform login screen.\n\n"
        f"⏳ This request will expire in 3 minutes."
    )
    async with client:
        await client.send_message(chat_id, message)
        return True
