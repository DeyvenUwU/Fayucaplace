from django.contrib import admin
from django.urls import path, include
from profiles import views as profileViews
from posting import views as postViews
from chat import views as chatViews
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #nuestras urls jsjs
    #PROFILES
    path('', profileViews.home, name='home'),
    path('signup/', profileViews.signUp, name='signUp'),
    path('login/', profileViews.signIn, name='signIn'),
    path('editprofile/', profileViews.editProfile, name='editprofile'),
    path('logout/', profileViews.signOut, name='signOut'),

    #POSTING
    path('mainpanel/', postViews.mainPanel, name='mainPanel'),
    path('buy/', postViews.buy, name='buy'),
    path('newarticle/', postViews.newArticle, name='newArticle'),
    path('newad/', postViews.newAd, name='newAd'),
    path('article/<int:id>/', postViews.articleDetails, name='articleDetails'),
    path('ad/<int:id>/', postViews.adDetails, name='adDetails'),

    #API
    path('api/', include('posting.urls')),
    path('api-token-auth/', views.obtain_auth_token),

    #CHAT
    path('chat/', chatViews.mensajes, name='mensajes'),
    path("sendMessage/<int:id>/", chatViews.sendMessage, name="sendMessage")
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)