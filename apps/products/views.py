from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q, Avg
from .models import Product

class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        queryset = Product.objects.filter(status=Product.Status.ACTIVE, is_active=True)

        # Search
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))

        # Category filter
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)

        # Price filter
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # Sorting
        sort = self.request.GET.get('sort', '-created_at')
        queryset = queryset.order_by(sort)

        return queryset.select_related('seller', 'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_products'] = Product.objects.filter(is_featured=True, is_active=True)[:6]
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Product.objects.select_related('seller', 'category').prefetch_related('seller__profile')

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Increment view count
        self.object.view_count += 1
        self.object.save(update_fields=['view_count'])
        return response

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'products/create.html'
    fields = ['title', 'description', 'short_description', 'category', 'tags',
              'thumbnail', 'screenshots', 'preview_video', 'price', 'original_price',
              'discount_percentage', 'file', 'license', 'documentation', 
              'release_notes', 'requirements', 'support_email']
    success_url = reverse_lazy('products:list')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

class SellerProductsView(LoginRequiredMixin, ListView):
    template_name = 'products/seller_list.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user).order_by('-created_at')
