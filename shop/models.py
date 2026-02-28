from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class Brand(models.Model):
    """Бренд электросамокатов"""
    name = models.CharField('Название', max_length=100, unique=True)
    slug = models.SlugField('Slug', unique=True)
    description = models.TextField('Описание', blank=True)
    logo = models.ImageField('Логотип', upload_to='brands/', blank=True)
    country = models.CharField('Страна', max_length=100, blank=True)
    website = models.URLField('Сайт', blank=True)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:brand_detail', kwargs={'slug': self.slug})


class Category(models.Model):
    """Категория товаров"""
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('Slug', unique=True)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Изображение', upload_to='categories/', blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родительская категория'
    )
    is_active = models.BooleanField('Активна', default=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
      return reverse('shop:category_detail', kwargs={'category_slug': self.slug})


class Product(models.Model):
    """Товар - электросамокат"""
    # Основная информация
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('Slug', unique=True)
    sku = models.CharField('Артикул', max_length=50, unique=True)
    description = models.TextField('Описание')
    short_description = models.TextField('Краткое описание', max_length=500, blank=True)
    
    # Связи
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Бренд'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категория'
    )
    
    # Цены
    price = models.DecimalField(
        'Цена',
        max_digits=12,
        decimal_places=0,
        validators=[MinValueValidator(0)]
    )
    old_price = models.DecimalField(
        'Старая цена',
        max_digits=12,
        decimal_places=0,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    
    # Наличие
    stock = models.PositiveIntegerField('В наличии', default=0)
    is_available = models.BooleanField('Доступен', default=True)
    is_featured = models.BooleanField('Рекомендуемый', default=False)
    is_new = models.BooleanField('Новинка', default=False)
    
    # Характеристики
    max_speed = models.PositiveIntegerField('Макс. скорость (км/ч)', null=True, blank=True)
    max_range = models.PositiveIntegerField('Запас хода (км)', null=True, blank=True)
    motor_power = models.PositiveIntegerField('Мощность мотора (Вт)', null=True, blank=True)
    battery_capacity = models.DecimalField(
        'Ёмкость батареи (Ач)',
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True
    )
    weight = models.DecimalField(
        'Вес (кг)',
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    max_load = models.PositiveIntegerField('Макс. нагрузка (кг)', null=True, blank=True)
    wheel_size = models.DecimalField(
        'Размер колёс (дюйм)',
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True
    )
    waterproof_rating = models.CharField(
        'Степень защиты',
        max_length=10,
        blank=True,
        choices=[
            ('IP54', 'IP54'),
            ('IP55', 'IP55'),
            ('IP56', 'IP56'),
            ('IP57', 'IP57'),
            ('IP65', 'IP65'),
            ('IP66', 'IP66'),
            ('IP67', 'IP67'),
            ('IP68', 'IP68'),
        ]
    )
    has_app = models.BooleanField('Приложение', default=False)
    has_cruise_control = models.BooleanField('Круиз-контроль', default=False)
    
    # SEO
    meta_title = models.CharField('Meta title', max_length=200, blank=True)
    meta_description = models.TextField('Meta description', blank=True)
    
    # Даты
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлён', auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['price']),
            models.Index(fields=['is_available']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['brand']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f"{self.brand.name} {self.name}"

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug': self.slug})

    @property
    def discount_percent(self):
        """Процент скидки"""
        if self.old_price and self.old_price > self.price:
            return int((self.old_price - self.price) / self.old_price * 100)
        return 0

    @property
    def average_rating(self):
        """Средний рейтинг"""
        reviews = self.reviews.filter(is_approved=True)
        if reviews.exists():
            return round(reviews.aggregate(models.Avg('rating'))['rating__avg'], 1)
        return 0

    @property
    def review_count(self):
        """Количество отзывов"""
        return self.reviews.filter(is_approved=True).count()


class ProductImage(models.Model):
    """Изображение товара"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Товар'
    )
    image = models.ImageField('Изображение', upload_to='products/')
    alt_text = models.CharField('Alt текст', max_length=200, blank=True)
    is_main = models.BooleanField('Главное изображение', default=False)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'
        ordering = ['order', 'id']

    def __str__(self):
        return f"Изображение {self.product}"


class Review(models.Model):
    """Отзыв о товаре"""
    RATING_CHOICES = [
        (1, '1 - Ужасно'),
        (2, '2 - Плохо'),
        (3, '3 - Нормально'),
        (4, '4 - Хорошо'),
        (5, '5 - Отлично'),
    ]
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Товар'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь'
    )
    rating = models.PositiveSmallIntegerField(
        'Оценка',
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField('Заголовок', max_length=200)
    text = models.TextField('Текст отзыва')
    pros = models.TextField('Достоинства', blank=True)
    cons = models.TextField('Недостатки', blank=True)
    is_approved = models.BooleanField('Одобрен', default=False)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлён', auto_now=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
        unique_together = ['product', 'user']

    def __str__(self):
        return f"Отзыв {self.user} о {self.product}"


class Banner(models.Model):
    """Баннер на главной"""
    title = models.CharField('Заголовок', max_length=200)
    subtitle = models.CharField('Подзаголовок', max_length=300, blank=True)
    image = models.ImageField('Изображение', upload_to='banners/')
    link = models.URLField('Ссылка', blank=True)
    button_text = models.CharField('Текст кнопки', max_length=50, default='Подробнее')
    is_active = models.BooleanField('Активен', default=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title
