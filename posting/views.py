from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import ArticleForm, AdForm
from .models import Publicacion


# Create your views here.
def mainPanel(request):
    return render(request, 'mainPanel.html')

def buy(request):
    posts = Publicacion.objects.filter(articulo__isnull=False).select_related('articulo')
    return render(request, 'buy.html', {
        'posts': posts
    })

def newArticle(request):
    if request.method == 'GET':
        return render(request, 'newArticle.html', {
            'form': ArticleForm
        })
    else:
        try:
            form = ArticleForm(request.POST, request.FILES)
            if form.is_valid():
                form.save(usuario=request.user)
                return redirect('mainPanel')  # redirige a donde desees
            else:
                form = ArticleForm()
            return redirect('mainPanel')  # redirige a donde desees
        except ValueError:
            return render(request, 'newArticle.html', {
            'form': ArticleForm,
            'error': 'Datos no validos'
        })


def newAd(request):
    return render(request, 'newAd.html')