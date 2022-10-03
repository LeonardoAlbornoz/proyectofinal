"""Python_final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from aplicacion import views 
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include

 # from django.contrib.auth.urls 
urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('single_view/<id>', views.single_view, name="single_view"),
    path('perfil/<perfil>', views.perfil, name="perfil"),
    path('create', views.create, name="create"),
    path('edit/<id>', views.edit_blog, name="edit_blog"),
    path('delete/<id>', views.delete_blog, name="delete_blog"),
    path('accounts/', include('django.contrib.auth.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
