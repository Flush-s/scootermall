from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """Форма для добавления отзыва"""
    class Meta:
        model = Review
        fields = ['rating', 'title', 'text', 'pros', 'cons']
        widgets = {
            'rating': forms.RadioSelect(choices=[
                (1, '1'),
                (2, '2'),
                (3, '3'),
                (4, '4'),
                (5, '5'),
            ]),
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Заголовок отзыва'
            }),
            'text': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 5,
                'placeholder': 'Расскажите о вашем опыте использования'
            }),
            'pros': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Что вам понравилось?'
            }),
            'cons': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Что можно улучшить?'
            }),
        }


class ProductFilterForm(forms.Form):
    """Форма фильтрации товаров"""
    price_min = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg text-sm',
            'placeholder': 'От'
        })
    )
    price_max = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg text-sm',
            'placeholder': 'До'
        })
    )
    brand = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-checkbox h-4 w-4 text-blue-600 rounded border-gray-300'
        })
    )
    motor_power_min = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg text-sm',
            'placeholder': 'Вт'
        })
    )
    max_speed_min = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg text-sm',
            'placeholder': 'км/ч'
        })
    )
    max_range_min = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg text-sm',
            'placeholder': 'км'
        })
    )
    wheel_size = forms.MultipleChoiceField(
        required=False,
        choices=[
            ('8', '8"'),
            ('8.5', '8.5"'),
            ('10', '10"'),
            ('11', '11"'),
            ('12', '12"'),
        ],
        widget=forms.CheckboxSelectMultiple()
    )
    has_app = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox h-4 w-4 text-blue-600 rounded border-gray-300'
        })
    )
    has_cruise_control = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox h-4 w-4 text-blue-600 rounded border-gray-300'
        })
    )
