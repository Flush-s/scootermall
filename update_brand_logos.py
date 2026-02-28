#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scootermall.settings')
django.setup()

from shop.models import Brand


def update_brand_logos():
    brand_logos = {
        'xiaomi': 'brands/xiaomi_logo.png',
        'ninebot': 'brands/ninebot_logo.png',
        'kugoo': 'brands/kugoo_logo.png',
        'dualtron': 'brands/dualtron_logo.png',
        'speedway': 'brands/speedway_logo.png',
        'inokim': 'brands/inokim_logo.png',
    }
    
    for slug, logo_path in brand_logos.items():
        try:
            brand = Brand.objects.get(slug=slug)
            brand.logo = logo_path
            brand.save()
            print(f'Logo updated for: {brand.name}')
        except Brand.DoesNotExist:
            print(f'Brand not found: {slug}')
    
    print('\nBrand logos updated successfully!')


if __name__ == '__main__':
    update_brand_logos()
