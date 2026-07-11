from allauth.account.signals import user_logged_in
from django.dispatch import receiver


@receiver(user_logged_in)
def social_login(sender, request, user, **kwargs):
    user.is_online = True
    user.unlock()
    user.save(update_fields=[
        "is_online",
        "failed_login_attempts",
        "locked_until",
    ])