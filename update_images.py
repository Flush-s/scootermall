#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scootermall.settings')
django.setup()

from shop.models import Product, ProductImage, Banner


def update_images():
    # Update banner image
    banner = Banner.objects.first()
    if banner:
        banner.image = 'banners/hero_banner.png'
        banner.save()
        print(f'Banner updated: {banner.title}')
    
    # Product images mapping
    product_images = {
        'mi-electric-scooter-pro-2': 'products/xiaomi_pro2.png',
        'ninebot-kickscooter-max-g30': 'products/ninebot_max.png',
        'kugoo-m4-pro': 'products/kugoo_m4.png',
        'dualtron-thunder': 'products/dualtron_thunder.png',
        'xiaomi-mi-electric-scooter-3': 'products/xiaomi_m3.png',
        'inokim-oxo': 'products/inokim_oxo.png',
    }
    
    for slug, image_path in product_images.items():
        try:
            product = Product.objects.get(slug=slug)
            # Create or update product image
            image, created = ProductImage.objects.get_or_create(
                product=product,
                is_main=True,
                defaults={
                    'image': image_path,
                    'alt_text': str(product)
                }
            )
            if not created:
                image.image = image_path
                image.save()
            print(f'Image updated for: {product.name}')
        except Product.DoesNotExist:
            print(f'Product not found: {slug}')
    
    print('\nImages updated successfully!')


if __name__ == '__main__':
    update_images()
