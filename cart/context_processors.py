from .models import Cart


def cart_context(request):
    """Добавляет информацию о корзине в контекст всех шаблонов"""
    cart = None
    cart_items_count = 0
    cart_total = 0
    
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.prefetch_related('items__product').get(user=request.user)
        except Cart.DoesNotExist:
            pass
    else:
        session_id = request.session.session_key
        if session_id:
            try:
                cart = Cart.objects.prefetch_related('items__product').get(session_id=session_id, user=None)
            except Cart.DoesNotExist:
                pass
    
    if cart:
        cart_items_count = cart.total_items
        cart_total = cart.total_price
    
    return {
        'cart': cart,
        'cart_items_count': cart_items_count,
        'cart_total': cart_total,
    }
