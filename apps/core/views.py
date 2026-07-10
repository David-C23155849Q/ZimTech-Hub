"""
Core views for ZimTechHub
"""
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from apps.products.models import Product
from apps.projects.models import Project
from apps.posts.models import Post
from apps.jobs.models import Job
from apps.events.models import Event


class HomeView(TemplateView):
    """
    Landing page view showcasing featured content.
    """
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Featured products
        context['featured_products'] = Product.objects.filter(
            is_active=True,
            is_featured=True
        ).select_related('seller').prefetch_related('categories')[:8]

        # Trending projects
        context['trending_projects'] = Project.objects.filter(
            is_public=True
        ).annotate(
            star_count=Count('stars')
        ).order_by('-star_count')[:6]

        # Recent posts
        context['recent_posts'] = Post.objects.filter(
            is_published=True
        ).select_related('author').prefetch_related('likes')[:10]

        # Active jobs
        context['active_jobs'] = Job.objects.filter(
            is_active=True,
            deadline__gte=timezone.now()
        ).select_related('company')[:5]

        # Upcoming events
        context['upcoming_events'] = Event.objects.filter(
            is_published=True,
            start_date__gte=timezone.now()
        ).order_by('start_date')[:4]

        # Stats
        context['stats'] = {
            'developers': 1200,
            'products': 450,
            'projects': 890,
            'jobs': 67,
        }

        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'


class ContactView(TemplateView):
    template_name = 'core/contact.html'


class TermsView(TemplateView):
    template_name = 'core/terms.html'


class PrivacyView(TemplateView):
    template_name = 'core/privacy.html'


class SearchView(ListView):
    """
    Global search across all content types.
    """
    template_name = 'core/search.html'
    context_object_name = 'results'
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if not query:
            return []

        # This is a simplified search - integrate Elasticsearch/Meilisearch later
        results = []

        # Search products
        products = Product.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            is_active=True
        )[:10]
        for p in products:
            results.append({'type': 'product', 'object': p})

        # Search projects
        projects = Project.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            is_public=True
        )[:10]
        for p in projects:
            results.append({'type': 'project', 'object': p})

        # Search posts
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            is_published=True
        )[:10]
        for p in posts:
            results.append({'type': 'post', 'object': p})

        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

from django.shortcuts import render

def about(request):
    return render(request, "about/about.html")