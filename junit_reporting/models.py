# pylint: disable=missing-docstring
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import permalink
from rest_framework.authtoken.models import Token


# pylint: disable=unused-argument
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# pylint: disable=too-few-public-methods
class JUnitReport(models.Model):
    build_number = models.IntegerField(unique=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    @permalink
    def get_absolute_url(self):
        return ('report', [self.build_number])
