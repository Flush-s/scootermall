from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """Форма оформления заказа"""
    promo_code = forms.CharField(
        label='Промокод',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'flex-1 px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent',
            'placeholder': 'Введите код'
        })
    )
    
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'city', 'address', 'zip_code', 'comment']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent',
                'placeholder': 'Имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent',
                'placeholder': 'Фамилия'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent',
                'placeholder': '+7 (999) 999-99-99'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent',
                'placeholder': 'email@example.com'
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent',
                'placeholder': 'Город'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent',
                'placeholder': 'Улица, дом, квартира',
                'rows': 3
            }),
            'zip_code': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent',
                'placeholder': '123456'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent',
                'placeholder': 'Комментарий к заказу (необязательно)',
                'rows': 3
            }),
        }
