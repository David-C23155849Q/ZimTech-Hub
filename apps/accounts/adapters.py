from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    """
    Custom adapter for ZimTechHub.
    """

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)

        # Default role
        if not user.role:
            user.role = user.Role.USER

        # Social providers already verify email
        if request and hasattr(request, "sociallogin"):
            user.email_verified = True
            user.is_verified = True

        if commit:
            user.save()

        return user