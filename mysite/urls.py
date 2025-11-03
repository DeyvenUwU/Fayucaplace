from django.contrib import admin
from django.urls import path
from profiles import views as profileViews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    #nuestras urls jsjs
    #PROFILES
    path('', profileViews.home, name='home'),
    path('signup/', profileViews.signUp, name='signUp'),
    path('login/', profileViews.signIn, name='signIn'),
    path('editprofile/', profileViews.editProfile, name='editprofile'),
    path('logout/', profileViews.signOut, name='signOut'),

    path('mainpanel/', profileViews.mainPanel, name='mainPanel')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)