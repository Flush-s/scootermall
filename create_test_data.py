#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scootermall.settings')
django.setup()

from shop.models import Brand, Category, Product, Banner
from accounts.models import User


def create_test_data():
    # Create brands
    brands_data = [
        {'name': 'Xiaomi', 'slug': 'xiaomi', 'country': 'Китай'},
        {'name': 'Ninebot', 'slug': 'ninebot', 'country': 'Китай'},
        {'name': 'Kugoo', 'slug': 'kugoo', 'country': 'Китай'},
        {'name': 'Dualtron', 'slug': 'dualtron', 'country': 'Южная Корея'},
        {'name': 'Speedway', 'slug': 'speedway', 'country': 'Южная Корея'},
        {'name': 'Inokim', 'slug': 'inokim', 'country': 'Израиль'},
    ]
    
    brands = {}
    for data in brands_data:
        brand, _ = Brand.objects.get_or_create(slug=data['slug'], defaults=data)
        brands[data['slug']] = brand
        print(f'Brand: {brand.name}')
    
    # Create categories
    categories_data = [
        {'name': 'Городские самокаты', 'slug': 'gorodskie-samokaty'},
        {'name': 'Внедорожные', 'slug': 'vnedorozhnye'},
        {'name': 'Лёгкие и компактные', 'slug': 'legkie-kompaktnye'},
        {'name': 'Мощные', 'slug': 'moshchnye'},
    ]
    
    categories = {}
    for data in categories_data:
        cat, _ = Category.objects.get_or_create(slug=data['slug'], defaults={**data, 'is_active': True})
        categories[data['slug']] = cat
        print(f'Category: {cat.name}')
    
    # Create products
    products_data = [
        {
            'name': 'Mi Electric Scooter Pro 2',
            'slug': 'mi-electric-scooter-pro-2',
            'sku': 'XIAOMI-PRO2-001',
            'brand': 'xiaomi',
            'category': 'gorodskie-samokaty',
            'price': 39990,
            'old_price': 45990,
            'stock': 15,
            'is_available': True,
            'is_featured': True,
            'is_new': False,
            'max_speed': 25,
            'max_range': 45,
            'motor_power': 300,
            'battery_capacity': 12.8,
            'weight': 14.2,
            'max_load': 100,
            'wheel_size': 8.5,
            'waterproof_rating': 'IP54',
            'has_app': True,
            'has_cruise_control': True,
            'description': 'Популярный городской электросамокат с отличным запасом хода. Лёгкий и компактный, идеально подходит для городских поездок.',
            'short_description': 'Городской электросамокат с запасом хода 45 км',
        },
        {
            'name': 'Ninebot KickScooter MAX G30',
            'slug': 'ninebot-kickscooter-max-g30',
            'sku': 'NINEBOT-G30-001',
            'brand': 'ninebot',
            'category': 'gorodskie-samokaty',
            'price': 54990,
            'old_price': None,
            'stock': 10,
            'is_available': True,
            'is_featured': True,
            'is_new': True,
            'max_speed': 30,
            'max_range': 65,
            'motor_power': 350,
            'battery_capacity': 15.3,
            'weight': 19.1,
            'max_load': 100,
            'wheel_size': 10,
            'waterproof_rating': 'IPX5',
            'has_app': True,
            'has_cruise_control': True,
            'description': 'Флагманская модель Ninebot с рекордным запасом хода. Большие 10-дюймовые колёса обеспечивают комфортную езду.',
            'short_description': 'Премиум самокат с запасом хода 65 км',
        },
        {
            'name': 'Kugoo M4 Pro',
            'slug': 'kugoo-m4-pro',
            'sku': 'KUGOO-M4PRO-001',
            'brand': 'kugoo',
            'category': 'vnedorozhnye',
            'price': 42990,
            'old_price': 49990,
            'stock': 8,
            'is_available': True,
            'is_featured': True,
            'is_new': False,
            'max_speed': 45,
            'max_range': 50,
            'motor_power': 500,
            'battery_capacity': 16.0,
            'weight': 22.0,
            'max_load': 150,
            'wheel_size': 10,
            'waterproof_rating': 'IP54',
            'has_app': False,
            'has_cruise_control': True,
            'description': 'Мощный внедорожный самокат с сиденьем. Отлично справляется с бездорожьем благодаря мощному мотору и большим колёсам.',
            'short_description': 'Внедорожный самокат с сиденьем',
        },
        {
            'name': 'Dualtron Thunder',
            'slug': 'dualtron-thunder',
            'sku': 'DUALTRON-THUNDER-001',
            'brand': 'dualtron',
            'category': 'moshchnye',
            'price': 189990,
            'old_price': None,
            'stock': 3,
            'is_available': True,
            'is_featured': True,
            'is_new': True,
            'max_speed': 80,
            'max_range': 120,
            'motor_power': 5400,
            'battery_capacity': 35.0,
            'weight': 43.0,
            'max_load': 150,
            'wheel_size': 11,
            'waterproof_rating': 'IP54',
            'has_app': True,
            'has_cruise_control': True,
            'description': 'Экстремальный самокат для настоящих энтузиастов. Два мотора по 2700 Вт каждый обеспечивают невероятную динамику.',
            'short_description': 'Экстремальный самокат 5400W',
        },
        {
            'name': 'Xiaomi Mi Electric Scooter 3',
            'slug': 'xiaomi-mi-electric-scooter-3',
            'sku': 'XIAOMI-M3-001',
            'brand': 'xiaomi',
            'category': 'legkie-kompaktnye',
            'price': 29990,
            'old_price': 34990,
            'stock': 20,
            'is_available': True,
            'is_featured': False,
            'is_new': True,
            'max_speed': 25,
            'max_range': 30,
            'motor_power': 300,
            'battery_capacity': 7.6,
            'weight': 13.0,
            'max_load': 100,
            'wheel_size': 8.5,
            'waterproof_rating': 'IP54',
            'has_app': True,
            'has_cruise_control': True,
            'description': 'Компактный и лёгкий самокат для коротких поездок. Легко складывается и переносится.',
            'short_description': 'Лёгкий городской самокат',
        },
        {
            'name': 'Inokim OXO',
            'slug': 'inokim-oxo',
            'sku': 'INOKIM-OXO-001',
            'brand': 'inokim',
            'category': 'moshchnye',
            'price': 159990,
            'old_price': None,
            'stock': 5,
            'is_available': True,
            'is_featured': True,
            'is_new': False,
            'max_speed': 65,
            'max_range': 110,
            'motor_power': 2600,
            'battery_capacity': 25.6,
            'weight': 33.0,
            'max_load': 120,
            'wheel_size': 10,
            'waterproof_rating': 'IP55',
            'has_app': True,
            'has_cruise_control': True,
            'description': 'Премиальный самокат израильского производителя. Отличное соотношение мощности, веса и запаса хода.',
            'short_description': 'Премиум самокат 2600W',
        },
    ]
    
    for data in products_data:
        brand_slug = data.pop('brand')
        cat_slug = data.pop('category')
        data['brand'] = brands[brand_slug]
        data['category'] = categories[cat_slug]
        
        product, created = Product.objects.get_or_create(slug=data['slug'], defaults=data)
        if created:
            print(f'Product created: {product.name}')
        else:
            print(f'Product exists: {product.name}')
    
    # Create banner
    banner_data = {
        'title': 'Новый Ninebot KickScooter MAX G30',
        'subtitle': 'Запас хода до 65 км, 10-дюймовые колёса, встроенная зарядка. Скидка 10% на первый заказ!',
        'button_text': 'Купить сейчас',
        'is_active': True,
        'order': 0,
    }
    banner, _ = Banner.objects.get_or_create(title=banner_data['title'], defaults=banner_data)
    print(f'Banner: {banner.title}')
    
    print('\nTest data created successfully!')


if __name__ == '__main__':
    create_test_data()
