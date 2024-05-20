"""
URL configuration for Agenda_Project_Django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from core import views
from django.views.generic import RedirectView
from core import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('agenda/', views.lista_eventos, name='lista_eventos'),
    path('agenda/evento/', views.evento, name='evento'),
    path('agenda/evento/submit',  views.submit_evento, name='submit_evento'),
    path('agenda/evento/delete/<int:id>/', views.delete_evento, name='delete_evento'),
    path('', RedirectView.as_view(url='/agenda/')),
    path('login/', views.login_user, name='login'),
    path('login/submit', views.submit_login, name='submit_login'),
    path('logout/', views.logout_user, name='logout'),
]
