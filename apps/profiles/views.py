from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.http import JsonResponse

from .models import Profile, Follow
from .forms import ProfileUpdateForm

User = get_user_model()

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profiles/detail.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return get_object_or_404(Profile, user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        user = profile.user
        if self.request.user.is_authenticated:
            context['is_following'] = Follow.objects.filter(follower=self.request.user, following=user).exists()
        else:
            context['is_following'] = False
        context['projects'] = user.projects.filter(is_public=True)[:6]
        context['products'] = user.products.filter(is_active=True)[:6]
        context['posts'] = user.posts.filter(is_published=True)[:5]
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'profiles/edit.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_initial(self):
        """Pre-format list fields into strings for the UI."""
        initial = super().get_initial()
        profile = self.get_object()
        
        # Convert lists stored in database back to comma-separated strings
        list_fields = ['skills', 'programming_languages', 'frameworks']
        for field in list_fields:
            value = getattr(profile, field)
            if isinstance(value, list):
                initial[field] = ', '.join(value)
        return initial

    def get_success_url(self):
        return reverse_lazy('profiles:detail', kwargs={'username': self.request.user.username})
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Pass both POST and FILES data to the form
        form = ProfileUpdateForm(request.POST, request.FILES, instance=self.object)
        
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # This is where the files are actually saved
        return super().form_valid(form)


class TopProfilesView(ListView):
    template_name = 'profiles/top.html'
    context_object_name = 'profiles'
    paginate_by = 24

    def get_queryset(self):
        return Profile.objects.filter(is_public=True, user__is_active=True).select_related('user').order_by('-reputation_score')
