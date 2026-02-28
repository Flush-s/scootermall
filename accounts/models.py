from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    """Пользователь с расширенным профилем"""
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть в формате: '+999999999'. До 15 цифр."
    )
    
    phone = models.CharField(
        'Телефон',
        validators=[phone_regex],
        max_length=17,
        blank=True
    )
    avatar = models.ImageField('Аватар', upload_to='avatars/', blank=True)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    city = models.CharField('Город', max_length=100, blank=True)
    address = models.TextField('Адрес доставки', blank=True)
    email_verified = models.BooleanField('Email подтверждён', default=False)
    phone_verified = models.BooleanField('Телефон подтверждён', default=False)
    newsletter_subscribed = models.BooleanField('Подписка на рассылку', default=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.get_full_name() or self.username


class UserFavorite(models.Model):
    """Избранные товары пользователя"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        'shop.Product',
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='Товар'
    )
    added_at = models.DateTimeField('Добавлен', auto_now_add=True)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        unique_together = ['user', 'product']

    def __str__(self):
        return f"{self.user} - {self.product}"


class SupportTicket(models.Model):
    """Обращение в поддержку"""
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('in_progress', 'В работе'),
        ('waiting', 'Ожидает ответа'),
        ('resolved', 'Решено'),
        ('closed', 'Закрыто'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
        ('urgent', 'Срочный'),
    ]
    
    CATEGORY_CHOICES = [
        ('general', 'Общий вопрос'),
        ('order', 'Заказ'),
        ('delivery', 'Доставка'),
        ('payment', 'Оплата'),
        ('return', 'Возврат'),
        ('warranty', 'Гарантия'),
        ('repair', 'Ремонт'),
        ('technical', 'Техническая поддержка'),
        ('other', 'Другое'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='support_tickets',
        verbose_name='Пользователь',
        null=True,
        blank=True
    )
    ticket_number = models.CharField('Номер обращения', max_length=20, unique=True)
    category = models.CharField('Категория', max_length=20, choices=CATEGORY_CHOICES, default='general')
    subject = models.CharField('Тема', max_length=200)
    message = models.TextField('Сообщение')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField('Приоритет', max_length=20, choices=PRIORITY_CHOICES, default='medium')
    email = models.EmailField('Email для связи', blank=True)
    phone = models.CharField('Телефон для связи', max_length=20, blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Обращение в поддержку'
        verbose_name_plural = 'Обращения в поддержку'
        ordering = ['-created_at']

    def __str__(self):
        return f"#{self.ticket_number} - {self.subject}"


class SupportMessage(models.Model):
    """Сообщение в обращении"""
    ticket = models.ForeignKey(
        SupportTicket,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Обращение'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='support_messages',
        verbose_name='Пользователь',
        null=True,
        blank=True
    )
    message = models.TextField('Сообщение')
    is_staff = models.BooleanField('От сотрудника', default=False)
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Сообщение поддержки'
        verbose_name_plural = 'Сообщения поддержки'
        ordering = ['created_at']

    def __str__(self):
        return f"Сообщение к {self.ticket}"
