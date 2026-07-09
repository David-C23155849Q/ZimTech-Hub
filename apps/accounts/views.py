"""
Accounts views for ZimTechHub
"""
from django.shortcuts import render, redirect
from django.views.generic import CreateView, View, TemplateView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator

from .forms import SignUpForm, LoginForm, PasswordResetRequestForm, ChangePasswordForm
from .models import User


class SignUpView(CreateView):
    """
    User registration view.
    """
    model = User
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Send verification email
        user = form.instance
        user.email_verification_token = default_token_generator.make_token(user)
        user.email_verification_sent_at = timezone.now()
        user.save()

        # Send welcome email
        self.send_verification_email(user)

        messages.success(
            self.request,
            'Account created successfully! Please check your email to verify your account.'
        )
        return response

    def send_verification_email(self, user):
        """Send email verification link."""
        subject = 'Welcome to ZimTechHub - Verify Your Email'
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = user.email_verification_token
        verification_url = self.request.build_absolute_uri(
            f"/accounts/verify/{uid}/{token}/"
        )

        message = render_to_string('accounts/emails/verify_email.html', {
            'user': user,
            'verification_url': verification_url,
        })

        send_mail(
            subject=subject,
            message='',
            html_message=message,
            from_email='noreply@zimtechhub.co.zw',
            recipient_list=[user.email],
            fail_silently=True,
        )


class CustomLoginView(BaseLoginView):
    """
    Custom login view with enhanced security.
    """
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()

        # Check if account is locked
        if user.is_locked():
            messages.error(
                self.request,
                'Your account is temporarily locked due to too many failed login attempts. '
                'Please try again later.'
            )
            return self.form_invalid(form)

        # Reset failed attempts on successful login
        user.unlock()
        user.is_online = True
        user.save(update_fields=['failed_login_attempts', 'locked_until', 'is_online'])

        response = super().form_valid(form)

        # Handle remember me
        if not form.cleaned_data.get('remember_me'):
            self.request.session.set_expiry(0)

        messages.success(self.request, f'Welcome back, {user.display_name}!')
        return response

    def form_invalid(self, form):
        # Track failed login attempts
        username = form.cleaned_data.get('username')
        if username:
            try:
                user = User.objects.get(email=username) if '@' in username else User.objects.get(username=username)
                user.failed_login_attempts += 1

                # Lock account after 5 failed attempts
                if user.failed_login_attempts >= 5:
                    user.locked_until = timezone.now() + timezone.timedelta(minutes=30)
                    messages.error(
                        self.request,
                        'Account locked for 30 minutes due to too many failed attempts.'
                    )

                user.save(update_fields=['failed_login_attempts', 'locked_until'])
            except User.DoesNotExist:
                pass

        return super().form_invalid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request # This passes it to __init__
        return kwargs


class CustomLogoutView(LoginRequiredMixin, BaseLogoutView):
    """
    Custom logout view that updates online status.
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.is_online = False
            request.user.save(update_fields=['is_online'])
        return super().dispatch(request, *args, **kwargs)


class EmailVerificationView(View):
    """
    Verify user email address.
    """
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and user.email_verification_token == token:
            user.email_verified = True
            user.is_verified = True
            user.email_verification_token = ''
            user.save()
            messages.success(request, 'Your email has been verified! You can now log in.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'The verification link is invalid or has expired.')
            return redirect('accounts:login')


class ProfileRedirectView(LoginRequiredMixin, View):
    """
    Redirect to user's profile.
    """
    def get(self, request):
        return redirect('profiles:detail', username=request.user.username)


class SettingsView(LoginRequiredMixin, TemplateView):
    """
    User settings page.
    """
    template_name = 'accounts/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_form'] = ChangePasswordForm()
        return context


class ChangePasswordView(LoginRequiredMixin, View):
    """
    Handle password change.
    """
    def post(self, request):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']

            if not request.user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
                return redirect('accounts:settings')

            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, 'Your password has been updated successfully.')
            return redirect('accounts:settings')

        for error in form.errors.values():
            messages.error(request, error[0])
        return redirect('accounts:settings')
