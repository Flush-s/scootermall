from django.contrib import admin
from .models import Brand, Category, Product, ProductImage, Review, Banner


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'is_main', 'order']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'is_active', 'created_at']
    list_filter = ['is_active', 'country']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'order']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'brand', 'category', 'price', 'old_price',
        'stock', 'is_available', 'is_featured', 'is_new', 'created_at'
    ]
    list_filter = [
        'is_available', 'is_featured', 'is_new',
        'brand', 'category', 'waterproof_rating'
    ]
    search_fields = ['name', 'sku', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'old_price', 'stock', 'is_available', 'is_featured', 'is_new']
    inlines = [ProductImageInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'sku', 'description', 'short_description')
        }),
        ('Связи', {
            'fields': ('brand', 'category')
        }),
        ('Цены', {
            'fields': ('price', 'old_price')
        }),
        ('Наличие', {
            'fields': ('stock', 'is_available', 'is_featured', 'is_new')
        }),
        ('Характеристики', {
            'fields': (
                'max_speed', 'max_range', 'motor_power', 'battery_capacity',
                'weight', 'max_load', 'wheel_size', 'waterproof_rating',
                'has_app', 'has_cruise_control'
            )
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating', 'created_at']
    search_fields = ['product__name', 'user__username', 'text']
    list_editable = ['is_approved']
    actions = ['approve_reviews']

    @admin.action(description='Одобрить выбранные отзывы')
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order', 'created_at']
    list_filter = ['is_active']
    list_editable = ['is_active', 'order']
    search_fields = ['title', 'subtitle']
