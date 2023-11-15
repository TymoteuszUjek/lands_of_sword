"""
URL configuration for LoSaS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home.urls')),
    path('team/', include('Team.urls')),
    path('users/', include('Users.urls')),
    path('world/', include('World.urls')),
    path('bots_farm/', include('Bots_Farm.urls')),
    path('fight', include('Fight.urls')),
    path('items', include('Items.urls')),
    path('inventory', include('Inventory.urls')),
    path('cities/', include('Cities.urls')),
    path('blacksmith/', include('Blacksmith.urls')),
    path('arena/', include('Arena.urls')),
    path('tavern/', include('Tavern.urls')),
    path('jeweler/', include('Jeweler.urls')),
    path('carpentry_shop/', include('Carpentry_Shop.urls')),
    path('clothier/', include('Clothier.urls')),
    path('armorer/', include('Armorer.urls')),
    path('boss_fight/', include('Boss_Fight.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
