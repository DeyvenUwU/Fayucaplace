<<<<<<< HEAD
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import ArticleForm, AdForm, EditArticleForm, EditAdForm
from .models import Publicacion, Categoria
from datetime import date


# Create your views here.
def mainPanel(request):
    hoy = date.today()
    posts = Publicacion.objects.filter(
        anuncio__isnull=False, 
        estado='ACTIVA',
        anuncio__fechaInicio__lte=hoy,
        anuncio__fechaFin__gte=hoy
    ).select_related('anuncio')
    return render(request, 'mainPanel.html', {
        'posts': posts
    })

def buy(request):
    posts = Publicacion.objects.filter(articulo__isnull=False, estado='ACTIVA').select_related('articulo')
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
                publicacion_instance = form.save(request.user)
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
        return render(request, 'newAd.html', {
            'form': AdForm
        })
    else:
        # This part is now handled by the AJAX view, but kept as a fallback
        try:
            form = AdForm(request.POST, request.FILES)
            if form.is_valid():
                publicacion_instance = form.save(request.user)
                return redirect('mainPanel')
            else:
                return render(request, 'newAd.html', {
                    'form': form
                })
        except ValueError as e:
            return render(request, 'newAd.html', {
                'form': AdForm(),
                'error': f'Datos no válidos: {e}'
            })


def articleDetails(request, id):
    post = get_object_or_404(Publicacion.objects.select_related('articulo', 'idUsuario'), pk=id)
    return render(request, 'articleDetails.html', {'post': post})

def adDetails(request, id):
    post = get_object_or_404(Publicacion.objects.select_related('anuncio', 'idUsuario'), pk=id)
    return render(request, 'adDetails.html', {'post': post})

@login_required
def myPublications(request):
    # Obtener publicaciones del usuario actual
    user_articles = Publicacion.objects.filter(idUsuario=request.user, articulo__isnull=False).select_related('articulo')
    user_ads = Publicacion.objects.filter(idUsuario=request.user, anuncio__isnull=False).select_related('anuncio')
    categorias = Categoria.objects.all()
    
    return render(request, 'myPublications.html', {
        'user_articles': user_articles,
        'user_ads': user_ads,
        'categorias': categorias
    })

@login_required
def editArticle(request, id):
    publicacion = get_object_or_404(Publicacion, pk=id, idUsuario=request.user)
    articulo = publicacion.articulo
    
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        form = EditArticleForm(
            instance=publicacion,
            articulo_instance=articulo
        )
        return render(request, 'editArticle.html', {
            'form': form,
            'categorias': categorias,
            'post': publicacion
        })
    else:
        form = EditArticleForm(
            request.POST,
            request.FILES,
            instance=publicacion,
            articulo_instance=articulo
        )
        if form.is_valid():
            form.save()
            return redirect('articleDetails', id=publicacion.id)
        else:
            categorias = Categoria.objects.all()
            return render(request, 'editArticle.html', {
                'form': form,
                'categorias': categorias,
                'post': publicacion,
                'error': 'Error al actualizar el artículo'
            })

@login_required
def editAd(request, id):
    publicacion = get_object_or_404(Publicacion, pk=id, idUsuario=request.user)
    anuncio = publicacion.anuncio
    
    if request.method == 'GET':
        form = EditAdForm(
            instance=publicacion,
            anuncio_instance=anuncio
        )
        return render(request, 'editAd.html', {
            'form': form,
            'post': publicacion
        })
    else:
        form = EditAdForm(
            request.POST,
            request.FILES,
            instance=publicacion,
            anuncio_instance=anuncio
        )
        if form.is_valid():
            form.save()
            return redirect('adDetails', id=publicacion.id)
        else:
            return render(request, 'editAd.html', {
                'form': form,
                'post': publicacion,
                'error': 'Error al actualizar el anuncio'
            })
=======
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
>>>>>>> f271bf24dfb35a8596c07af58ada957384fefd36
