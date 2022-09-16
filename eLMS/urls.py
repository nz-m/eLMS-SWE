"""eLMS URL Configuration

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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main import views
from froala_editor import views as froala_views


admin.site.site_header = "eLMS Administration"
admin.site.site_title = "eLMS Administration Portal"
admin.site.index_title = "Welcome to eLMS Administration Portal"


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('student/', views.guestStudent, name='guestStudent'),
    path('teacher/', views.guestFaculty, name='guestFaculty'),
    path('', include('main.urls')),
    path('', include('discussion.urls')),
    path('', include('attendance.urls')),
    path('', include('quiz.urls')),
    path('froala_editor/', include('froala_editor.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
