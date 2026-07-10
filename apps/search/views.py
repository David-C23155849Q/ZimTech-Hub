from django.views.generic import TemplateView
from django.db.models import Count

from apps.posts.models import Post
from .models import SearchHistory, TrendingSearch


class SearchView(TemplateView):

    template_name = "search/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        if user.is_authenticated:
            context["recent_searches"] = (
                SearchHistory.objects.filter(user=user)[:8]
            )
        else:
            context["recent_searches"] = []

        context["trending_searches"] = (
            TrendingSearch.objects.all()[:10]
        )

        context["popular_tags"] = (
            Post.objects.values("language")
            .exclude(language="")
            .annotate(total=Count("id"))
            .order_by("-total")[:10]
        )

        context["suggestions"] = [
            "Flutter",
            "Django",
            "Python",
            "React",
            "AI",
            "Machine Learning",
            "Cybersecurity",
            "Java",
            "Firebase",
            "UI Design",
            "Linux",
            "DevOps",
        ]

        return context