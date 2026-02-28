from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Аутентификация
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Профиль
    path('profile/', views.ProfileView.as_view(), name='profile'),
    
    # Избранное
    path('favorites/', views.favorites_view, name='favorites'),
    path('favorites/add/<slug:product_slug>/', views.add_to_favorites, name='add_favorite'),
    path('favorites/remove/<slug:product_slug>/', views.remove_from_favorites, name='remove_favorite'),
    
    # Поддержка
    path('support/', views.SupportTicketListView.as_view(), name='support_tickets'),
    path('support/create/', views.create_support_ticket, name='create_ticket'),
    path('support/<str:ticket_number>/', views.support_ticket_detail, name='ticket_detail'),
]
