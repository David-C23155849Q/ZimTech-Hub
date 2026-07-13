from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from .models import Profile, Follow
from .forms import ProfileUpdateForm


User = get_user_model()



class ProfileDetailView(DetailView):

    model = Profile

    template_name = "profiles/detail.html"

    context_object_name = "profile"



    def get_object(self, queryset=None):

        username = self.kwargs.get("username")

        return get_object_or_404(
            Profile.objects.select_related("user"),
            user__username=username
        )



    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)


        profile = self.object

        user = profile.user



        # Follow status

        if self.request.user.is_authenticated:

            context["is_following"] = Follow.objects.filter(
                follower=self.request.user,
                following=user
            ).exists()

        else:

            context["is_following"] = False



        # Roles

        context["roles"] = user.roles.all()



        # Optional related content

        context["projects"] = []

        context["products"] = []

        context["posts"] = []



        if hasattr(user, "projects"):

            context["projects"] = user.projects.filter(
                is_public=True
            )[:6]


        if hasattr(user, "products"):

            context["products"] = user.products.filter(
                is_active=True
            )[:6]


        if hasattr(user, "posts"):

            context["posts"] = user.posts.filter(
                is_published=True
            )[:5]



        return context





class ProfileUpdateView(LoginRequiredMixin, UpdateView):

    model = Profile

    form_class = ProfileUpdateForm

    template_name = "profiles/edit.html"



    def get_object(self, queryset=None):

        return self.request.user.profile



    def get_success_url(self):

        return reverse_lazy(
            "profiles:detail",
            kwargs={
                "username": self.request.user.username
            }
        )





class TopProfilesView(ListView):

    model = Profile

    template_name = "profiles/top.html"

    context_object_name = "profiles"

    paginate_by = 24



    def get_queryset(self):

        return Profile.objects.filter(

            is_public=True,

            user__is_active=True

        ).select_related(

            "user"

        ).prefetch_related(

            "user__roles"

        ).order_by(

            "-reputation_score"

        )