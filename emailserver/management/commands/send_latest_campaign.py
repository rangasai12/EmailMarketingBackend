# your_project/your_app/management/commands/send_latest_campaign.py

from django.core.management.base import BaseCommand
from emailserver.Scripts.email_utils import send_latest_campaign_email

class Command(BaseCommand):
    help = 'Send the latest campaign email'

    def handle(self, *args, **kwargs):
        try:
            send_latest_campaign_email()
            self.stdout.write(self.style.SUCCESS('Successfully sent the latest campaign email.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR("Couldn't send Emails Error:",e))
            raise e
        