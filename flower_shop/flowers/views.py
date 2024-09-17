from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .models import Flower, Order
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# flowers/views.py

from bot import send_order_to_telegram

# Функция регистрации
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('flower_catalog')
    else:
        form = UserCreationForm()
    return render(request, 'flowers/register.html', {'form': form})

# Функция входа
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('flower_catalog')
    else:
        form = AuthenticationForm()
    return render(request, 'flowers/login.html', {'form': form})

# Функция выхода
def logout_view(request):
    logout(request)
    return redirect('login')

# Функция отображения каталога цветов
def flower_catalog(request):
    flowers = Flower.objects.all()
    return render(request, 'flowers/catalog.html', {'flowers': flowers})

# Функция оформления заказа
@login_required
def place_order(request, flower_id):
    flower = Flower.objects.get(id=flower_id)
    if request.method == 'POST':
        delivery_address = request.POST['delivery_address']
        order = Order(user=request.user, total_price=flower.price, delivery_address=delivery_address)
        order.save()
        order.flowers.add(flower)

        # Отправка данных заказа в Telegram бота
        send_order_to_telegram(order)

        return HttpResponse("Ваш заказ был успешно оформлен!")
    return render(request, 'flowers/place_order.html', {'flower': flower})
