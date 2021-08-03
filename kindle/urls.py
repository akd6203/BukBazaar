"""kindle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from myapp import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls,),
    path('', views.index, name="index"),
    path('contact/', views.contact_view, name="contact"),
    path('single_author/', views.single_author, name="single_author"),
    path('books/', views.all_books, name="all_books"),
    path('register/', views.register, name="register"),
    path('login/', views.signIn, name="login"),
    path('single_book/<int:id>/', views.single_book, name="single_book"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('logout/', views.user_logout, name="logout"),

    path('paypal/', include("paypal.standard.ipn.urls")),
    path('payment_done/', views.payment_done, name="payment_done"),
    path('payment_cancel/', views.payment_cancel, name="payment_cancel"),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
