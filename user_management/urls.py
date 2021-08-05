from django.urls import include, path
from . import views

urlpatterns = [
  path('add/', views.likearticle),
  path('view/', views.viewarticle),
   path('delete/',views.deleteuser),
  
]