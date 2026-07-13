from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from apps.accounts.models import Role


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom behavior for social logins.
    """

    def populate_user(self, request, sociallogin, data):
        """
        Fill in fields on first signup.
        """
        user = super().populate_user(request, sociallogin, data)

        user.first_name = data.get("first_name", "")
        user.last_name = data.get("last_name", "")
        user.username = (
            data.get("username")
            or data.get("email").split("@")[0]
        )

        return user

    def save_user(self, request, sociallogin, form=None):
        """
        Called when a new social account is created.
        """
        user = super().save_user(request, sociallogin, form)

        user.email_verified = True
        user.is_verified = True
        user.is_online = True

        user.save()

        # Give a default role if none exists
        if not user.roles.exists():
            default_role, _ = Role.objects.get_or_create(
                name=Role.STUDENT,
                defaults={
                    "description": "Default role for social signups"
                }
            )
            user.roles.add(default_role)

        return user