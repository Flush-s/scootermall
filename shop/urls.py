from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Главная
    path('', views.HomeView.as_view(), name='home'),
    
    # Товары
    path('catalog/', views.ProductListView.as_view(), name='product_list'),
    path('catalog/<slug:category_slug>/', views.ProductListView.as_view(), name='category_detail'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product/<slug:slug>/review/', views.add_review, name='add_review'),
    
    # Бренды
    path('brands/', views.BrandListView.as_view(), name='brand_list'),
    path('brand/<slug:slug>/', views.BrandDetailView.as_view(), name='brand_detail'),
    
    # Категории
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    
    # Поиск
    path('search/ajax/', views.search_ajax, name='search_ajax'),
    
    # Статические страницы
    path('sales/', views.SalesView.as_view(), name='sales'),
    path('delivery/', views.DeliveryView.as_view(), name='delivery'),
    path('warranty/', views.WarrantyView.as_view(), name='warranty'),
    path('compare/', views.CompareView.as_view(), name='compare'),
    path('compare/add/<int:product_id>/', views.add_to_compare, name='add_to_compare'),
    path('compare/remove/<int:product_id>/', views.remove_from_compare, name='remove_from_compare'),
    path('orders/', views.OrdersView.as_view(), name='orders'),
]
