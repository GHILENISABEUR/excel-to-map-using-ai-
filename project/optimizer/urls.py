# optimizer/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_excel, name='upload_excel'),
    # Add other URLs as needed
]
