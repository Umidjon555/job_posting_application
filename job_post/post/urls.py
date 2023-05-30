from . import views
from django.urls import path

urlpatterns = [
    path('', views.Careers_list, name='blog'),
    path('<int:pk>/', views.blog_single, name='blog_single'),
]