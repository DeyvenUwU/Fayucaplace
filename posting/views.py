from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import ArticleForm, AdForm
from .models import Publicacion, Categoria
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.template.loader import render_to_string
# from weasyprint import HTML  # Comentado temporalmente - requiere dependencias de compilación
import openpyxl
from mysite.permissions import admin_required


# Create your views here.
def mainPanel(request):
    posts = Publicacion.objects.filter(anuncio__isnull=False).select_related('anuncio')
    categorias = Categoria.objects.all()
    return render(request, 'mainPanel.html', {
        'posts': posts,
        'categorias': categorias
    })

@login_required
def dashboard(request):
    """Dashboard con métricas básicas y datos para gráficas."""
    total_publicaciones = Publicacion.objects.count()
    total_articulos = Publicacion.objects.filter(articulo__isnull=False).count()
    total_anuncios = Publicacion.objects.filter(anuncio__isnull=False).count()

    # Conteo por subcategoría
    subcategoria_counts = Publicacion.objects.values('subcategoria__nombre').annotate(total=Count('id')).order_by('-total')
    # Conteo por día últimos 7 días
    from django.utils import timezone
    from datetime import timedelta
    hoy = timezone.now()
    dias = [hoy - timedelta(days=i) for i in range(6,-1,-1)]
    series_dias = []
    for d in dias:
        inicio = d.replace(hour=0, minute=0, second=0, microsecond=0)
        fin = inicio + timedelta(days=1)
        series_dias.append({
            'fecha': inicio.strftime('%Y-%m-%d'),
            'total': Publicacion.objects.filter(fechaPublicacion__gte=inicio, fechaPublicacion__lt=fin).count()
        })

    return render(request, 'dashboard.html', {
        'total_publicaciones': total_publicaciones,
        'total_articulos': total_articulos,
        'total_anuncios': total_anuncios,
        'subcategoria_counts': list(subcategoria_counts),
        'series_dias': series_dias,
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

@login_required
def editPublication(request, id):
    """Renderiza template de edición; la lógica CRUD se hace vía AJAX usando la API REST."""
    pub = get_object_or_404(Publicacion, pk=id)
    if pub.idUsuario != request.user:
        return redirect('mainPanel')
    return render(request, 'editPublication.html', {'pub_id': pub.id})

@login_required
@admin_required
def export_articles_to_excel(request):
    posts = Publicacion.objects.filter(articulo__isnull=False).select_related('articulo', 'idUsuario')
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Artículos"

    # Encabezados
    ws.append(['Título', 'Precio', 'Cantidad', 'Vendedor', 'Fecha de Publicación'])

    # Datos
    for post in posts:
        ws.append([
            post.titulo,
            post.articulo.precio,
            post.articulo.cantidad,
            post.idUsuario.username,
            post.fechaPublicacion.strftime('%Y-%m-%d %H:%M')
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=articulos.xlsx'
    wb.save(response)
    return response

# Función temporalmente deshabilitada - requiere weasyprint
# @login_required
# @admin_required
# def export_articles_to_pdf(request):
#     posts = Publicacion.objects.filter(articulo__isnull=False).select_related('articulo', 'idUsuario')
#     html_string = render_to_string('pdf_template.html', {'posts': posts})
# 
#     html = HTML(string=html_string)
#     pdf = html.write_pdf()
# 
#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename=reporte_articulos.pdf'
#     return response