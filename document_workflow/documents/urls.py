# documents/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.document_list, name='document_list'),
    path('document/<int:pk>/', views.document_detail, name='document_detail'),
    path('documents/', views.document_list, name='document_list'),
    path('documents/create/', views.document_create, name='document_create'),
    path('documents/edit/<int:pk>/', views.document_edit, name='document_edit'),
    path('documents/delete/<int:pk>/', views.document_delete, name='document_delete'),  # Add this line for delete
]
