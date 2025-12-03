from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from .forms import MessageForm
from posting.models import Publicacion
from django.db import models
from django.urls import reverse



# Create your views here.
@login_required
def mensajes(request):
    usuario = request.user
    chats = Chat.objects.filter(models.Q(user1=usuario) | models.Q(user2=usuario)).order_by('-created_at')

    chat_id = request.GET.get("chat_id")
    selected_chat = None
    messages = []

    if chat_id:
        selected_chat = get_object_or_404(chats, id=chat_id)

        if request.method == "POST":
            content = request.POST.get("content")
            if content:
                Message.objects.create(chat=selected_chat, sender=usuario, content=content)
            return redirect(f"{reverse('mensajes')}?chat_id={selected_chat.id}")

        messages = selected_chat.messages.all().order_by("timestamp")

    return render(request, "messages.html", {
        "chats": chats,
        "selected_chat": selected_chat,
        "messages": messages,
    })


def chat(request):
    return render(request, 'messages.html')

def sendMessage(request, id):
    post = get_object_or_404(Publicacion, id=id)
    vendedor = post.idUsuario
    comprador = request.user

    # --- Detectar tipo de publicación ---
    if hasattr(post, "anuncio"):
        cancel_url = reverse("adDetails", args=[post.id])
    elif hasattr(post, "articulo"):
        cancel_url = reverse("articleDetails", args=[post.id])
    else:
        # Por si acaso, vuelve al home
        cancel_url = reverse("home")

    # --- Procesar el formulario ---
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            contenido = form.cleaned_data["content"]

            # Buscar o crear el chat
            chat = Chat.objects.filter(
                models.Q(user1=comprador, user2=vendedor) |
                models.Q(user1=vendedor, user2=comprador)
            ).first()

            if not chat:
                chat = Chat.objects.create(user1=comprador, user2=vendedor)

            Message.objects.create(chat=chat, sender=comprador, content=contenido)

            return redirect("mensajes")  # este es el nombre de tu ruta del chat
    else:
        form = MessageForm()

    # --- Renderizar plantilla ---
    return render(request, "sendMessage.html", {
        "form": form,
        "post": post,
        "cancel_url": cancel_url,
    })