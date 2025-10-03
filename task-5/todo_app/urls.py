from django.urls import path
from . import views

urlpatterns = [
    path('SignUp/', views.SignUp),
    path('SignIn/', views.SignIn),
    path('SignOut/', views.SignOut),
    path('create_todo/', views.create_todos),
    path('view_todos/', views.view_todos),
    path("<int:id>/del_todo/", views.del_todos),
    path("<int:id>/update_todo/", views.update_todos),
    path("<int:id>/completed/", views.completed)
]