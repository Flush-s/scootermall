from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import uuid
from shop.models import Product
from .models import Cart, CartItem, Order, OrderItem, PromoCode
from .forms import OrderForm


def get_or_create_cart(request):
    """Получить или создать корзину"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id, user=None)
    return cart


def cart_detail(request):
    """Страница корзины"""
    cart = get_or_create_cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@require_POST
def cart_add(request, product_slug):
    """Добавить товар в корзину"""
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, slug=product_slug, is_available=True)
    
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    messages.success(request, f'{product} добавлен в корзину')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total': cart.total_items,
            'message': f'{product} добавлен в корзину'
        })
    
    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, item_id):
    """Обновить количество товара"""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total': cart.total_items,
            'cart_price': cart.total_price,
            'item_total': cart_item.total_price if quantity > 0 else 0
        })
    
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, item_id):
    """Удалить товар из корзины"""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_name = str(cart_item.product)
    cart_item.delete()
    
    messages.success(request, f'{product_name} удалён из корзины')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total': cart.total_items,
            'cart_price': cart.total_price
        })
    
    return redirect('cart:cart_detail')


def cart_summary(request):
    """Краткая информация о корзине (для AJAX)"""
    cart = get_or_create_cart(request)
    return JsonResponse({
        'total_items': cart.total_items,
        'total_price': cart.total_price
    })


@login_required
def checkout(request):
    """Оформление заказа"""
    cart = get_or_create_cart(request)
    
    if not cart.items.exists():
        messages.warning(request, 'Ваша корзина пуста')
        return redirect('cart:cart_detail')
    
    # Предзаполняем форму данными пользователя
    initial_data = {}
    if request.user:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'phone': request.user.phone,
            'email': request.user.email,
            'city': request.user.city,
            'address': request.user.address,
        }
    
    discount = 0
    promo_code_obj = None
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Проверяем промокод
            promo_code_input = request.POST.get('promo_code', '').strip()
            if promo_code_input:
                try:
                    promo_code_obj = PromoCode.objects.get(code=promo_code_input, is_active=True)
                    if promo_code_obj.is_valid():
                        if promo_code_obj.discount_percent:
                            discount = cart.total_price * promo_code_obj.discount_percent // 100
                        else:
                            discount = promo_code_obj.discount_amount
                        promo_code_obj.used_count += 1
                        promo_code_obj.save()
                        messages.success(request, f'Промокод применён! Скидка: {discount} ₽')
                    else:
                        messages.warning(request, 'Промокод недействителен')
                except PromoCode.DoesNotExist:
                    messages.warning(request, 'Промокод не найден')
            
            # Создаём заказ
            order = form.save(commit=False)
            order.user = request.user
            order.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
            order.total_amount = cart.total_price - discount
            order.discount = discount
            if promo_code_obj:
                order.promo_code = promo_code_obj.code
            order.save()
            
            # Создаём элементы заказа
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
            
            # Очищаем корзину
            cart.items.all().delete()
            
            messages.success(request, f'Заказ #{order.order_number} успешно оформлен!')
            return redirect('shop:orders')
    else:
        form = OrderForm(initial=initial_data)
    
    return render(request, 'cart/checkout.html', {
        'cart': cart,
        'form': form,
        'discount': discount,
    })
