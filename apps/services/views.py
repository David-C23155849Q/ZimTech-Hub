from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Service

class ServiceListView(ListView):
    model = Service
    template_name = 'services/list.html'
    context_object_name = 'services'
    paginate_by = 20

    def get_queryset(self):
        return Service.objects.filter(status=Service.Status.ACTIVE).select_related('freelancer__profile')

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/detail.html'
    slug_url_kwarg = 'slug'

class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service
    template_name = 'services/create.html'
    fields = ['title', 'description', 'price', 'currency', 'delivery_time', 'revisions',
              'gallery', 'tags', 'requirements', 'faq']
    success_url = reverse_lazy('services:list')

    def form_valid(self, form):
        form.instance.freelancer = self.request.user
        return super().form_valid(form)
