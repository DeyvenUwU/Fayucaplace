from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import ArticleForm, AdForm
from .models import Publicacion, Categoria


# Create your views here.
def mainPanel(request):
    posts = Publicacion.objects.filter(anuncio__isnull=False).select_related('anuncio')
    categorias = Categoria.objects.all()
    return render(request, 'mainPanel.html', {
        'posts': posts,
        'categorias': categorias
    })

def buy(request):
    posts = Publicacion.objects.filter(articulo__isnull=False).select_related('articulo')
    categorias = Categoria.objects.all()
    return render(request, 'buy.html', {
        'posts': posts,
        'categorias': categorias
    })

@login_required
def newArticle(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        return render(request, 'newArticle.html', {
            'form': ArticleForm,
            'categorias': categorias
        })
    else:
        # This part is now handled by the AJAX view, but kept as a fallback
        try:
            form = ArticleForm(request.POST, request.FILES)
            if form.is_valid():
                publicacion_instance = form.save(commit=False)
                publicacion_instance.idUsuario = request.user
                
                subcategoria_id = request.POST.get('subcategoria')
                if subcategoria_id:
                    publicacion_instance.subcategoria_id = subcategoria_id
                
                publicacion_instance.save()
                form.save_m2m()

                return redirect('mainPanel')
            else:
                categorias = Categoria.objects.all()
                return render(request, 'newArticle.html', {
                    'form': form,
                    'categorias': categorias
                })
        except ValueError as e:
            categorias = Categoria.objects.all()
            return render(request, 'newArticle.html', {
                'form': ArticleForm(),
                'categorias': categorias,
                'error': f'Datos no válidos: {e}'
            })

@login_required
def newAd(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        return render(request, 'newAd.html', {
            'form': AdForm,
            'categorias': categorias
        })
    else:
        # This part is now handled by the AJAX view, but kept as a fallback
        try:
            form = AdForm(request.POST, request.FILES)
            if form.is_valid():
                publicacion_instance = form.save(commit=False)
                publicacion_instance.idUsuario = request.user
                
                subcategoria_id = request.POST.get('subcategoria')
                if subcategoria_id:
                    publicacion_instance.subcategoria_id = subcategoria_id
                
                publicacion_instance.save()
                form.save_m2m()

                return redirect('mainPanel')
            else:
                categorias = Categoria.objects.all()
                return render(request, 'newAd.html', {
                    'form': form,
                    'categorias': categorias
                })
        except ValueError as e:
            categorias = Categoria.objects.all()
            return render(request, 'newAd.html', {
                'form': AdForm(),
                'categorias': categorias,
                'error': f'Datos no válidos: {e}'
            })


def articleDetails(request, id):
    post = get_object_or_404(Publicacion.objects.select_related('articulo', 'idUsuario'), pk=id)
    return render(request, 'articleDetails.html', {'post': post})

def adDetails(request, id):
    post = get_object_or_404(Publicacion.objects.select_related('anuncio', 'idUsuario'), pk=id)
    return render(request, 'adDetails.html', {'post': post})
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import ArticleForm, AdForm
from .models import Publicacion, Categoria


# Create your views here.
def mainPanel(request):
    posts = Publicacion.objects.filter(anuncio__isnull=False).select_related('anuncio')
    categorias = Categoria.objects.all()
    return render(request, 'mainPanel.html', {
        'posts': posts,
        'categorias': categorias
    })

def buy(request):
    posts = Publicacion.objects.filter(articulo__isnull=False).select_related('articulo')
    categorias = Categoria.objects.all()
    return render(request, 'buy.html', {
        'posts': posts,
        'categorias': categorias
    })

@login_required
def newArticle(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        return render(request, 'newArticle.html', {
            'form': ArticleForm,
            'categorias': categorias
        })
    else:
        # This part is now handled by the AJAX view, but kept as a fallback
        try:
            form = ArticleForm(request.POST, request.FILES)
            if form.is_valid():
                publicacion_instance = form.save(commit=False)
                publicacion_instance.idUsuario = request.user
                
                subcategoria_id = request.POST.get('subcategoria')
                if subcategoria_id:
                    publicacion_instance.subcategoria_id = subcategoria_id
                
                publicacion_instance.save()
                form.save_m2m()

                return redirect('mainPanel')
            else:
                categorias = Categoria.objects.all()
                return render(request, 'newArticle.html', {
                    'form': form,
                    'categorias': categorias
                })
        except ValueError as e:
            categorias = Categoria.objects.all()
            return render(request, 'newArticle.html', {
                'form': ArticleForm(),
                'categorias': categorias,
                'error': f'Datos no válidos: {e}'
            })

@login_required
def newAd(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        return render(request, 'newAd.html', {
            'form': AdForm,
            'categorias': categorias
        })
    else:
        # This part is now handled by the AJAX view, but kept as a fallback
        try:
            form = AdForm(request.POST, request.FILES)
            if form.is_valid():
                publicacion_instance = form.save(commit=False)
                publicacion_instance.idUsuario = request.user
                
                subcategoria_id = request.POST.get('subcategoria')
                if subcategoria_id:
                    publicacion_instance.subcategoria_id = subcategoria_id
                
                publicacion_instance.save()
                form.save_m2m()

                return redirect('mainPanel')
            else:
                categorias = Categoria.objects.all()
                return render(request, 'newAd.html', {
                    'form': form,
                    'categorias': categorias
                })
        except ValueError as e:
            categorias = Categoria.objects.all()
            return render(request, 'newAd.html', {
                'form': AdForm(),
                'categorias': categorias,
                'error': f'Datos no válidos: {e}'
            })


def articleDetails(request, id):
    post = get_object_or_404(Publicacion.objects.select_related('articulo', 'idUsuario'), pk=id)
    return render(request, 'articleDetails.html', {'post': post})

def adDetails(request, id):
    post = get_object_or_404(Publicacion.objects.select_related('anuncio', 'idUsuario'), pk=id)
    return render(request, 'adDetails.html', {'post': post})
