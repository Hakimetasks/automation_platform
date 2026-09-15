import time
from celery import shared_task
from django.db import transaction
from core.models import User, AdCampaign

@shared_task
def process_ad_view_payout(user_id, campaign_id):
    """1.2.1 & 4.1.2: Background task to validate view time and payout user"""
    try:
        campaign = AdCampaign.objects.get(id=campaign_id)
        # በሮድማፑ 1.2.1 መሰረት የተሰጠውን የማስታወቂያ ሰከንድ በጀርባ ይቆጥራል (10 - 90 ሰከንድ)
        view_time = max(10, min(90, campaign.ad_view_time))
        time.sleep(view_time)
        
        # የክፍያ ስራውን በአስተማማኝ ሁኔታ (Atomic Transaction) ማከናወን
        with transaction.atomic():
            user = User.objects.select_for_update().get(id=user_id)
            if user.is_frozen:
                return f"User {user_id} is frozen. Payout cancelled."
                
            # ለምሳሌ፡ በአንድ እይታ 0.10 ብር/ሳንቲም ክፍያ መጨመር
            payout_amount = 0.10
            user.balance += payout_amount
            user.save()
            
            return f"Successfully paid {payout_amount} to user {user_id} for campaign {campaign_id}"
            
    except AdCampaign.DoesNotExist:
        return f"Campaign {campaign_id} not found"
    except User.DoesNotExist:
        return f"User {user_id} not found"
