# flowers/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Flower, Order

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

def flower_catalog(request):
    flowers = Flower.objects.all()
    return render(request, 'flowers/catalog.html', {'flowers': flowers})

def place_order(request, flower_id):
    flower = Flower.objects.get(id=flower_id)
    if request.method == 'POST':
        order = Order(user=request.user)
        order.save()
        order.flowers.add(flower)
        return redirect('flower_catalog')
    return render(request, 'flowers/place_order.html', {'flower': flower})


# Create your views here.
