from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q, Count
from .models import Project

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/list.html'
    context_object_name = 'projects'
    paginate_by = 20

    def get_queryset(self):
        queryset = Project.objects.filter(is_public=True)
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        tech = self.request.GET.get('tech')
        if tech:
            queryset = queryset.filter(technologies__contains=[tech])
        sort = self.request.GET.get('sort', '-created_at')
        return queryset.select_related('owner').annotate(star_count=Count('starred_by')).order_by(sort)

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/detail.html'
    slug_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.views += 1
        self.object.save(update_fields=['views'])
        return response

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'projects/create.html'
    fields = ['title', 'description', 'content', 'status', 'github_url', 'live_demo_url',
              'thumbnail', 'screenshots', 'technologies', 'programming_languages', 
              'frameworks', 'version', 'license', 'is_public']
    success_url = reverse_lazy('projects:list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
