from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Role




class SignUpForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password"
            }
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm Password"
            }
        )
    )


    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all().order_by("name"),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="What describes you?"
    )


    class Meta:
        model = User

        fields = [
            "email",
            "username",
            "roles",
            "password",
            "confirm_password",
        ]


    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        roles = cleaned_data.get("roles")


        if password and confirm_password:

            if password != confirm_password:

                self.add_error(
                    "confirm_password",
                    "Passwords do not match."
                )


        if not roles:

            self.add_error(
                "roles",
                "Please choose at least one role."
            )


        return cleaned_data



    def save(self, commit=True):

        user = super().save(commit=False)

        user.set_password(
            self.cleaned_data["password"]
        )


        if commit:

            user.save()

            user.roles.set(
                self.cleaned_data["roles"]
            )


        return user



    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop(
            "request",
            None
        )

        super().__init__(
            *args,
            **kwargs
        )


class LoginForm(AuthenticationForm):

    remember_me = forms.BooleanField(
        required=False
    )


    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop(
            "request",
            None
        )

        super().__init__(
            *args,
            **kwargs
        )





class PasswordResetRequestForm(forms.Form):

    email = forms.EmailField()


    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop(
            "request",
            None
        )

        super().__init__(
            *args,
            **kwargs
        )





class ChangePasswordForm(forms.Form):

    current_password = forms.CharField(
        widget=forms.PasswordInput
    )


    new_password = forms.CharField(
        widget=forms.PasswordInput
    )


    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput
    )


    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop(
            "request",
            None
        )

        super().__init__(
            *args,
            **kwargs
        )