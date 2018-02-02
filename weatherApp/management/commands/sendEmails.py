'''
Ref:
https://www.caktusgroup.com/blog/2011/10/24/django-without-web/
'''
from django.core.management.base import BaseCommand, CommandError

from weatherApp.utilities import send_emails
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        send_emails()
