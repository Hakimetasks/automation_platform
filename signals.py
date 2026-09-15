import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Advertisement

@receiver(post_save, sender=Advertisement)
def ad_creation_automation_trigger(sender, instance, created, **kwargs):
    # 2.1.1 አዲስ ማስታወቂያ በተሳካ ሁኔታ ሲፈጠር አውቶማቲክ ትሪገር ማድረግ
    if created:
        # 2.3.1 መልዕክቱን በንጽህና ማደራጀት (Message Formatting)
        bot_message = (
            f"📢 *አዲስ ማስታወቂያ ወጥቷል!*\n\n"
            f"📝 *ርዕስ:* {instance.title}\n"
            f"💰 *ጠቅላላ በጀት:* {instance.total_budget} ETB\n"
            f"📉 *የተጣራ በጀት (ከ10% ኮሚሽን በኋላ):* {instance.net_budget} ETB\n"
            f"🏦 *የተቆረጠ ኮሚሽን:* {instance.commission_deducted} ETB\n"
        )
        
        # 2.3.2 ከቴሌግራም ኤፒአይ (Telegram API) ጋር ማገናኘት
        token = getattr(settings, 'TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
        chat_id = getattr(settings, 'TELEGRAM_CHANNEL_ID', '@your_channel_username_here')
        
        telegram_url = f"https://telegram.org{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": bot_message,
            "parse_mode": "Markdown"
        }
        
        try:
            # መልዕክቱን በጀርባ አውቶማቲክ በሆነ መንገድ መላክ
            response = requests.post(telegram_url, json=payload, timeout=10)
            if response.status_code == 200:
                print(f"[AUTOMATION SUCCESS]: Message sent to Telegram for ad: {instance.title}")
            else:
                print(f"[AUTOMATION WARNING]: Failed to send to Telegram. Bot token or Channel ID not set yet.")
        except requests.exceptions.RequestException as e:
            print(f"[AUTOMATION ERROR]: Network error while connecting to Telegram: {e}")
