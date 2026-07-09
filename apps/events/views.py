from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Event

class EventListView(ListView):
    model = Event
    template_name = 'events/list.html'
    context_object_name = 'events'
    paginate_by = 12

    def get_queryset(self):
        queryset = Event.objects.filter(is_published=True, start_date__gte=timezone.now())
        event_type = self.request.GET.get('type')
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        return queryset.order_by('start_date')

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/detail.html'
    slug_url_kwarg = 'slug'

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    template_name = 'events/create.html'
    fields = ['title', 'description', 'event_type', 'banner', 'venue', 'address',
              'map_url', 'start_date', 'end_date', 'max_attendees', 'speakers',
              'ticket_price', 'currency', 'registration_url']
    success_url = reverse_lazy('events:list')

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        return super().form_valid(form)
