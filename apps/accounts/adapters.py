from allauth.account.adapter import DefaultAccountAdapter
from .models import Role


class AccountAdapter(DefaultAccountAdapter):
    """
    Custom adapter for ZimTechHub.
    """


    def save_user(self, request, user, form, commit=True):

        user = super().save_user(
            request,
            user,
            form,
            commit=False
        )


        # Social providers already verify email

        if request and hasattr(request, "sociallogin"):

            user.email_verified = True
            user.is_verified = True



        if commit:

            user.save()


            # Add default role if user has none

            if not user.roles.exists():

                default_role, created = Role.objects.get_or_create(
                    name=Role.STUDENT,
                    defaults={
                        "description": "Default role for new users"
                    }
                )

                user.roles.add(
                    default_role
                )


        return user