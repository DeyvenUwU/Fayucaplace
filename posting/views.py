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
    posts = Publicacion.objects.filter(anuncio__isnull=False).select_related('anuncio')
    return render(request, 'mainPanel.html', {
        'posts': posts
    })

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
    if request.method == 'GET':
        return render(request, 'newAd.html', {
            'form': AdForm
        })
    else:
        try:
            form = AdForm(request.POST, request.FILES)
            if form.is_valid():
                form.save(usuario=request.user)
                return redirect('mainPanel')  # redirige a donde desees
            else:
                form = AdForm()
            #return redirect('mainPanel')  # redirige a donde desees
        except ValueError:
            return render(request, 'newAd.html', {
            'form': AdForm,
            'error': 'Datos no validos'
        })

def articleDetails(request, id):
    post = get_object_or_404(Publicacion.objects.select_related('articulo', 'idUsuario'), pk=id)
    return render(request, 'articleDetails.html', {'post': post})

def adDetails(request, id):
    post = get_object_or_404(Publicacion.objects.select_related('anuncio', 'idUsuario'), pk=id)
    return render(request, 'adDetails.html', {'post': post})