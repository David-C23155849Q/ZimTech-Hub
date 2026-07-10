from django.views.generic import (
    ListView,
    DetailView,
    CreateView
)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db import transaction

from .models import Post, PostImage, PollOption
from .forms import PostForm


class FeedView(ListView):
    model = Post
    template_name = "posts/feed.html"
    context_object_name = "posts"
    paginate_by = 20

    def get_queryset(self):
        return (
            Post.objects.filter(is_published=True)
            .select_related("author", "author__profile")
            .prefetch_related("images", "poll_options")
            .order_by("-created_at")
        )

class PostDetailView(DetailView):

    model = Post

    template_name = "posts/detail.html"

    context_object_name = "post"




class PostCreateView(LoginRequiredMixin, CreateView):

    model = Post

    form_class = PostForm

    template_name = "posts/create.html"

    success_url = reverse_lazy(
        "posts:feed"
    )


    @transaction.atomic
    def form_valid(self, form):

        # Attach logged-in user
        form.instance.author = self.request.user


        response = super().form_valid(form)


        post = self.object



        # Save uploaded images

        images = self.request.FILES.getlist(
            "images"
        )


        for image in images:

            PostImage.objects.create(
                post=post,
                image=image
            )



        # Save poll options

        if post.post_type == Post.PostType.POLL:


            options = self.request.POST.getlist(
                "poll_options"
            )


            for option in options:

                option = option.strip()


                if option:

                    PollOption.objects.create(
                        post=post,
                        text=option
                    )


        return response   
