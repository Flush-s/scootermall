from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserFavorite, SupportTicket, SupportMessage


class SupportMessageInline(admin.TabularInline):
    model = SupportMessage
    extra = 0
    readonly_fields = ['created_at']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        'username', 'email', 'first_name', 'last_name',
        'phone', 'city', 'is_staff', 'email_verified', 'created_at'
    ]
    list_filter = ['is_staff', 'is_superuser', 'email_verified', 'phone_verified', 'newsletter_subscribed']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('phone', 'avatar', 'birth_date', 'city', 'address')
        }),
        ('Верификация', {
            'fields': ('email_verified', 'phone_verified', 'newsletter_subscribed')
        }),
    )


@admin.register(UserFavorite)
class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__username', 'product__name']


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = [
        'ticket_number', 'subject', 'category', 'user',
        'status', 'priority', 'created_at', 'updated_at'
    ]
    list_filter = ['status', 'priority', 'category', 'created_at']
    search_fields = ['ticket_number', 'subject', 'message', 'email', 'phone']
    list_editable = ['status', 'priority']
    inlines = [SupportMessageInline]
    readonly_fields = ['ticket_number', 'created_at', 'updated_at']


@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'user', 'is_staff', 'created_at']
    list_filter = ['is_staff', 'created_at']
    search_fields = ['ticket__ticket_number', 'message']
