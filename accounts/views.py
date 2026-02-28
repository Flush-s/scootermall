from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, UserFavorite, SupportTicket, SupportMessage
from .forms import (
    UserRegistrationForm, UserLoginForm, UserProfileForm,
    SupportTicketForm, SupportMessageForm
)


class RegisterView(CreateView):
    """Регистрация пользователя"""
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('shop:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Добро пожаловать! Регистрация прошла успешно.')
        return response


def login_view(request):
    """Вход пользователя"""
    if request.user.is_authenticated:
        return redirect('shop:home')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'С возвращением, {user.get_full_name() or user.username}!')
            next_url = request.GET.get('next', 'shop:home')
            return redirect(next_url)
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Выход пользователя"""
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('shop:home')


class ProfileView(LoginRequiredMixin, UpdateView):
    """Профиль пользователя"""
    model = User
    form_class = UserProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлён!')
        return super().form_valid(form)


@login_required
def favorites_view(request):
    """Избранные товары"""
    favorites = UserFavorite.objects.filter(
        user=request.user
    ).select_related('product__brand').prefetch_related('product__images')
    return render(request, 'accounts/favorites.html', {'favorites': favorites})


@login_required
def add_to_favorites(request, product_slug):
    """Добавить в избранное"""
    from shop.models import Product
    product = get_object_or_404(Product, slug=product_slug)
    
    favorite, created = UserFavorite.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if created:
        messages.success(request, f'{product} добавлен в избранное')
    else:
        messages.info(request, f'{product} уже в избранном')
    
    return redirect('shop:product_detail', slug=product_slug)


@login_required
def remove_from_favorites(request, product_slug):
    """Удалить из избранного"""
    from shop.models import Product
    product = get_object_or_404(Product, slug=product_slug)
    
    UserFavorite.objects.filter(user=request.user, product=product).delete()
    messages.success(request, f'{product} удалён из избранного')
    
    return redirect('accounts:favorites')


class SupportTicketListView(LoginRequiredMixin, ListView):
    """Список обращений в поддержку"""
    model = SupportTicket
    template_name = 'accounts/support_tickets.html'
    context_object_name = 'tickets'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_staff:
            return SupportTicket.objects.all()
        return SupportTicket.objects.filter(user=self.request.user)


@login_required
def create_support_ticket(request):
    """Создать обращение в поддержку"""
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.email = request.user.email
            ticket.phone = request.user.phone
            # Генерируем номер тикета
            import uuid
            ticket.ticket_number = f"TKT-{uuid.uuid4().hex[:8].upper()}"
            ticket.save()
            messages.success(request, f'Обращение #{ticket.ticket_number} создано!')
            return redirect('accounts:support_tickets')
    else:
        form = SupportTicketForm()
    
    return render(request, 'accounts/create_ticket.html', {'form': form})


@login_required
def support_ticket_detail(request, ticket_number):
    """Детали обращения"""
    ticket = get_object_or_404(SupportTicket, ticket_number=ticket_number)
    
    # Проверка прав доступа
    if not request.user.is_staff and ticket.user != request.user:
        messages.error(request, 'У вас нет доступа к этому обращению')
        return redirect('accounts:support_tickets')
    
    if request.method == 'POST':
        form = SupportMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.ticket = ticket
            message.user = request.user
            message.is_staff = request.user.is_staff
            message.save()
            
            # Обновляем статус тикета
            if request.user.is_staff:
                ticket.status = 'waiting'
            else:
                ticket.status = 'in_progress'
            ticket.save()
            
            return redirect('accounts:ticket_detail', ticket_number=ticket_number)
    else:
        form = SupportMessageForm()
    
    messages_list = ticket.messages.select_related('user').all()
    
    return render(request, 'accounts/ticket_detail.html', {
        'ticket': ticket,
        'messages': messages_list,
        'form': form
    })
