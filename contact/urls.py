from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact),
    path('new_contact/', views.new_contact),
]