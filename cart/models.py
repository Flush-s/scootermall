from django.db import models
from django.contrib.auth import get_user_model
from shop.models import Product

User = get_user_model()


class Cart(models.Model):
    """Корзина пользователя"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь',
        null=True,
        blank=True
    )
    session_id = models.CharField('ID сессии', max_length=100, blank=True)
    created_at = models.DateTimeField('Создана', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлена', auto_now=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        if self.user:
            return f"Корзина {self.user}"
        return f"Корзина сессии {self.session_id[:10]}..."

    @property
    def total_items(self):
        """Общее количество товаров"""
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        """Общая стоимость"""
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    """Элемент корзины"""
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField('Количество', default=1)
    added_at = models.DateTimeField('Добавлен', auto_now_add=True)

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
        unique_together = ['cart', 'product']

    def __str__(self):
        return f"{self.product} x {self.quantity}"

    @property
    def total_price(self):
        """Стоимость позиции"""
        return self.product.price * self.quantity


class Order(models.Model):
    """Заказ"""
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь'
    )
    order_number = models.CharField('Номер заказа', max_length=20, unique=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    
    # Контактная информация
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Email')
    
    # Адрес доставки
    city = models.CharField('Город', max_length=100)
    address = models.TextField('Адрес')
    zip_code = models.CharField('Индекс', max_length=10, blank=True)
    
    # Стоимость
    total_amount = models.DecimalField('Сумма заказа', max_digits=12, decimal_places=0)
    delivery_cost = models.DecimalField('Стоимость доставки', max_digits=10, decimal_places=0, default=0)
    discount = models.DecimalField('Скидка', max_digits=10, decimal_places=0, default=0)
    
    # Промокод
    promo_code = models.CharField('Промокод', max_length=50, blank=True)
    
    # Комментарий
    comment = models.TextField('Комментарий', blank=True)
    
    # Даты
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлён', auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.order_number}"


class OrderItem(models.Model):
    """Элемент заказа"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField('Количество', default=1)
    price = models.DecimalField('Цена', max_digits=12, decimal_places=0)

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def __str__(self):
        return f"{self.product} x {self.quantity}"

    @property
    def total_price(self):
        return self.price * self.quantity


class PromoCode(models.Model):
    """Промокод"""
    code = models.CharField('Код', max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField('Скидка %', default=0)
    discount_amount = models.DecimalField('Скидка сумма', max_digits=10, decimal_places=0, default=0)
    valid_from = models.DateTimeField('Действует с')
    valid_to = models.DateTimeField('Действует до')
    is_active = models.BooleanField('Активен', default=True)
    max_uses = models.PositiveIntegerField('Максимум использований', null=True, blank=True)
    used_count = models.PositiveIntegerField('Использовано', default=0)

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def __str__(self):
        return self.code

    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        if not self.is_active:
            return False
        if now < self.valid_from or now > self.valid_to:
            return False
        if self.max_uses and self.used_count >= self.max_uses:
            return False
        return True
