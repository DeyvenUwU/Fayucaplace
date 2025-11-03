from django.contrib import admin
from django.urls import path
from profiles import views as profileView

urlpatterns = [
    path('admin/', admin.site.urls),

    #nuestras urls jsjs
    #PROFILES
    path('', profileView.home, name='home'),
    path('singup/', profileView.singUp, name='singUp'),
    path('login/', profileView.singIn, name='singIn')
]
