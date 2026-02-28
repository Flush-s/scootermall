from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Avg
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Product, Category, Brand, Banner, Review
from .forms import ReviewForm, ProductFilterForm


class HomeView(TemplateView):
    """Главная страница"""
    template_name = 'shop/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['banners'] = Banner.objects.filter(is_active=True)[:3]
        context['featured_products'] = Product.objects.filter(
            is_available=True, is_featured=True
        ).select_related('brand')[:8]
        context['new_products'] = Product.objects.filter(
            is_available=True, is_new=True
        ).select_related('brand')[:8]
        context['top_rated'] = Product.objects.filter(
            is_available=True
        ).annotate(
            avg_rating=Avg('reviews__rating')
        ).filter(avg_rating__gte=4).select_related('brand')[:4]
        context['brands'] = Brand.objects.filter(is_active=True)[:8]
        return context


class ProductListView(ListView):
    """Список товаров с фильтрами"""
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True).select_related('brand', 'category')
        
        # Поиск
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(brand__name__icontains=search) |
                Q(sku__icontains=search)
            )
        
        # Фильтр по категории
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
            self.category = category
        
        # Фильтр по бренду
        brand_slug = self.kwargs.get('brand_slug')
        if brand_slug:
            brand = get_object_or_404(Brand, slug=brand_slug)
            queryset = queryset.filter(brand=brand)
            self.brand = brand
        
        # Фильтр по цене
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        
        # Фильтр по брендам (множественный)
        brands = self.request.GET.getlist('brand')
        if brands:
            queryset = queryset.filter(brand__id__in=brands)
        
        # Фильтр по мощности
        motor_power_min = self.request.GET.get('motor_power_min')
        if motor_power_min:
            queryset = queryset.filter(motor_power__gte=motor_power_min)
        
        # Фильтр по скорости
        max_speed_min = self.request.GET.get('max_speed_min')
        if max_speed_min:
            queryset = queryset.filter(max_speed__gte=max_speed_min)
        
        # Фильтр по запасу хода
        max_range_min = self.request.GET.get('max_range_min')
        if max_range_min:
            queryset = queryset.filter(max_range__gte=max_range_min)
        
        # Фильтр по размеру колёс
        wheel_sizes = self.request.GET.getlist('wheel_size')
        if wheel_sizes:
            queryset = queryset.filter(wheel_size__in=wheel_sizes)
        
        # Фильтр по приложению
        has_app = self.request.GET.get('has_app')
        if has_app:
            queryset = queryset.filter(has_app=True)
        
        # Фильтр по круиз-контролю
        has_cruise = self.request.GET.get('has_cruise_control')
        if has_cruise:
            queryset = queryset.filter(has_cruise_control=True)
        
        # Сортировка
        sort = self.request.GET.get('sort', '-created_at')
        sort_options = {
            'price_asc': 'price',
            'price_desc': '-price',
            'name_asc': 'name',
            'name_desc': '-name',
            'rating': '-reviews__rating',
            'newest': '-created_at',
        }
        queryset = queryset.order_by(sort_options.get(sort, '-created_at'))
        
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True, parent=None)
        context['brands'] = Brand.objects.filter(is_active=True)
        context['filter_form'] = ProductFilterForm(self.request.GET or None)
        context['filter_form'].fields['brand'].choices = [
            (b.id, b.name) for b in Brand.objects.filter(is_active=True)
        ]
        
        # Размеры колёс для фильтра
        context['wheel_sizes'] = ['8', '8.5', '10', '11', '12']
        
        # Добавляем выбранную категорию/бренд в контекст
        if hasattr(self, 'category'):
            context['current_category'] = self.category
        if hasattr(self, 'brand'):
            context['current_brand'] = self.brand
        
        # Параметры для сохранения состояния фильтров
        context['current_sort'] = self.request.GET.get('sort', 'newest')
        context['search_query'] = self.request.GET.get('search', '')
        
        return context


class ProductDetailView(DetailView):
    """Страница товара"""
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Product.objects.select_related('brand', 'category').prefetch_related('images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        # Похожие товары
        context['related_products'] = Product.objects.filter(
            category=product.category,
            is_available=True
        ).exclude(id=product.id).select_related('brand')[:4]
        
        # Отзывы
        context['reviews'] = product.reviews.filter(is_approved=True).select_related('user')
        context['review_count'] = context['reviews'].count()
        context['average_rating'] = product.average_rating
        
        # Форма отзыва
        if self.request.user.is_authenticated:
            context['review_form'] = ReviewForm()
            context['user_can_review'] = not product.reviews.filter(
                user=self.request.user
            ).exists()
        
        return context


@login_required
def add_review(request, slug):
    """Добавление отзыва"""
    product = get_object_or_404(Product, slug=slug)
    
    if product.reviews.filter(user=request.user).exists():
        messages.error(request, 'Вы уже оставляли отзыв об этом товаре')
        return redirect('shop:product_detail', slug=slug)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Спасибо за ваш отзыв! Он появится после модерации.')
            return redirect('shop:product_detail', slug=slug)
    else:
        form = ReviewForm()
    
    return render(request, 'shop/add_review.html', {
        'form': form,
        'product': product
    })


class BrandListView(ListView):
    """Список брендов"""
    model = Brand
    template_name = 'shop/brand_list.html'
    context_object_name = 'brands'

    def get_queryset(self):
        return Brand.objects.filter(is_active=True).prefetch_related('products')


class BrandDetailView(DetailView):
    """Страница бренда"""
    model = Brand
    template_name = 'shop/brand_detail.html'
    context_object_name = 'brand'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand = self.get_object()
        context['products'] = Product.objects.filter(
            brand=brand, is_available=True
        ).select_related('category')[:12]
        return context


class CategoryListView(ListView):
    """Список категорий"""
    model = Category
    template_name = 'shop/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(is_active=True, parent=None).prefetch_related('children')


def search_ajax(request):
    """AJAX поиск для автодополнения"""
    query = request.GET.get('q', '')
    results = []
    
    if len(query) >= 2:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(brand__name__icontains=query)
        ).filter(is_available=True).select_related('brand')[:5]
        
        results = [{
            'name': str(p),
            'slug': p.slug,
            'price': p.price,
            'image': p.images.filter(is_main=True).first().image.url if p.images.filter(is_main=True).exists() else None
        } for p in products]
    
    return render(request, 'shop/search_results.html', {'results': results})


class SalesView(TemplateView):
    """Страница акций"""
    template_name = 'shop/sales.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sale_products'] = Product.objects.filter(
            is_available=True,
            old_price__isnull=False
        ).select_related('brand')[:20]
        return context


class DeliveryView(TemplateView):
    """Страница доставки"""
    template_name = 'shop/delivery.html'


class WarrantyView(TemplateView):
    """Страница гарантии"""
    template_name = 'shop/warranty.html'


class CompareView(TemplateView):
    """Страница сравнения"""
    template_name = 'shop/compare.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        compare_list = self.request.session.get('compare_list', [])
        if compare_list:
            context['compare_products'] = Product.objects.filter(
                id__in=compare_list,
                is_available=True
            ).select_related('brand')
        else:
            context['compare_products'] = []
        context['compare_count'] = len(compare_list)
        return context


def add_to_compare(request, product_id):
    """Добавить в сравнение"""
    compare_list = request.session.get('compare_list', [])
    if product_id not in compare_list:
        if len(compare_list) >= 4:
            messages.warning(request, 'Можно сравнивать не более 4 товаров')
        else:
            compare_list.append(product_id)
            request.session['compare_list'] = compare_list
            messages.success(request, 'Товар добавлен в сравнение')
    else:
        messages.info(request, 'Товар уже в списке сравнения')
    return redirect(request.META.get('HTTP_REFERER', 'shop:home'))


def remove_from_compare(request, product_id):
    """Удалить из сравнения"""
    compare_list = request.session.get('compare_list', [])
    if product_id in compare_list:
        compare_list.remove(product_id)
        request.session['compare_list'] = compare_list
        messages.success(request, 'Товар удалён из сравнения')
    return redirect('shop:compare')


class OrdersView(LoginRequiredMixin, ListView):
    """Страница моих заказов"""
    template_name = 'shop/orders.html'
    context_object_name = 'orders'
    
    def get_queryset(self):
        from cart.models import Order
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')
